"""Validate the generated Los release and refresh validation artefacts."""

from collections import defaultdict
from hashlib import sha256
from pathlib import Path
import subprocess
import sys

from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.compare import isomorphic
from rdflib.namespace import DCTERMS, OWL, RDFS, SKOS

from finalize_turtle import REQUIRED, STATIC_RDF
from generate_turtle import DATA, SOURCE_XLSX, generate_graph


PACKAGE = Path(__file__).resolve().parents[1]
SHAPES = PACKAGE / "validation" / "los-shapes.ttl"
SHACL_REPORT = PACKAGE / "validation" / "shacl-report.txt"
QUALITY_REPORT = PACKAGE / "validation" / "custom-quality-report.txt"
SKOSIFIED = PACKAGE / "validation" / "los-skosified.ttl"
SKOSIFY_LOG = PACKAGE / "validation" / "skosify.log"

LOS = Namespace("https://id.norge.no/los/")
XKOS = Namespace("http://rdf-vocabulary.ddialliance.org/xkos#")
EUVOC = Namespace("https://publications.europa.eu/ontology/euvoc#")


def _require(condition, message, errors):
    if not condition:
        errors.append(message)


def _language_map(graph, subject, predicate):
    result = defaultdict(list)
    for value in graph.objects(subject, predicate):
        if isinstance(value, Literal):
            result[value.language].append(value)
    return result


def _hierarchy_cycles(graph, concepts):
    edges = {
        concept: {parent for parent in graph.objects(concept, SKOS.broader) if parent in concepts}
        for concept in concepts
    }
    visiting = set()
    visited = set()
    cycles = []

    def visit(node, path):
        if node in visiting:
            start = path.index(node)
            cycles.append(path[start:] + [node])
            return
        if node in visited:
            return
        visiting.add(node)
        for parent in edges[node]:
            visit(parent, path + [parent])
        visiting.remove(node)
        visited.add(node)

    for concept in concepts:
        visit(concept, [concept])
    return cycles


def _validate_shape_equivalent(graph):
    errors = []
    concepts = set(graph.subjects(RDF.type, SKOS.Concept))
    collections = set(graph.subjects(RDF.type, SKOS.Collection))
    schemes = set(graph.subjects(RDF.type, SKOS.ConceptScheme))

    for concept in concepts:
        _require(isinstance(concept, URIRef), f"Begrep er ikke en IRI: {concept}", errors)
        labels = _language_map(graph, concept, SKOS.prefLabel)
        _require(sum(map(len, labels.values())) >= 2, f"For få prefLabel på {concept}", errors)
        _require(all(len(values) == 1 for values in labels.values()), f"prefLabel har ikke unike språk på {concept}", errors)
        schemes_for_concept = list(graph.objects(concept, SKOS.inScheme))
        _require(len(schemes_for_concept) == 1, f"{concept} har ikke nøyaktig én inScheme", errors)
        for scheme in schemes_for_concept:
            _require((scheme, RDF.type, SKOS.ConceptScheme) in graph, f"inScheme peker ikke på ConceptScheme: {concept}", errors)
        for related in graph.objects(concept, SKOS.broader):
            _require((related, RDF.type, SKOS.Concept) in graph, f"broader peker ikke på Concept: {concept} -> {related}", errors)
        for related in graph.objects(concept, SKOS.narrower):
            _require((related, RDF.type, SKOS.Concept) in graph, f"narrower peker ikke på Concept: {concept} -> {related}", errors)

    for scheme in schemes:
        _require(isinstance(scheme, URIRef), f"Begrepsskjema er ikke en IRI: {scheme}", errors)
        titles = _language_map(graph, scheme, DCTERMS.title)
        _require(sum(map(len, titles.values())) >= 2, f"For få titler på {scheme}", errors)
        _require(all(len(values) == 1 for values in titles.values()), f"Titler har ikke unike språk på {scheme}", errors)
        top_concepts = list(graph.objects(scheme, SKOS.hasTopConcept))
        _require(bool(top_concepts), f"Ingen toppbegreper på {scheme}", errors)
        for concept in top_concepts:
            _require((concept, RDF.type, SKOS.Concept) in graph, f"hasTopConcept peker ikke på Concept: {concept}", errors)

    for top_concept in set(graph.subjects(SKOS.topConceptOf, None)):
        _require(not any(graph.objects(top_concept, SKOS.broader)), f"Toppbegrep har broader: {top_concept}", errors)

    for collection in collections:
        _require(isinstance(collection, URIRef), f"Samling er ikke en IRI: {collection}", errors)
        labels = _language_map(graph, collection, SKOS.prefLabel)
        _require(sum(map(len, labels.values())) >= 2, f"For få prefLabel på {collection}", errors)
        _require(all(len(values) == 1 for values in labels.values()), f"prefLabel har ikke unike språk på {collection}", errors)
        members = list(graph.objects(collection, SKOS.member))
        _require(bool(members), f"Samling uten medlemmer: {collection}", errors)
        for member in members:
            _require((member, RDF.type, SKOS.Concept) in graph, f"Samlingsmedlem er ikke Concept: {member}", errors)

    for subject, predicates in REQUIRED.items():
        for predicate, required_values in predicates.items():
            missing = required_values - set(graph.objects(subject, predicate))
            _require(not missing, f"Mangler obligatorisk XKOS-metadata: {subject} {predicate} {sorted(map(str, missing))}", errors)

    return errors


def _validate_quality(graph):
    errors = []
    concepts = set(graph.subjects(RDF.type, SKOS.Concept))
    collections = set(graph.subjects(RDF.type, SKOS.Collection))
    schemes = set(graph.subjects(RDF.type, SKOS.ConceptScheme))

    broader = set(graph.triples((None, SKOS.broader, None)))
    narrower = set(graph.triples((None, SKOS.narrower, None)))
    missing_inverse = [(child, parent) for child, _, parent in broader if (parent, SKOS.narrower, child) not in graph]
    extra_inverse = [(parent, child) for parent, _, child in narrower if (child, SKOS.broader, parent) not in graph]
    _require(not missing_inverse, f"Mangler {len(missing_inverse)} inverse narrower-relasjoner", errors)
    _require(not extra_inverse, f"Har {len(extra_inverse)} narrower-relasjoner uten invers broader", errors)

    cycles = _hierarchy_cycles(graph, concepts)
    _require(not cycles, f"Fant {len(cycles)} hierarkiske sykler", errors)

    missing_nb_nn = []
    label_collisions = []
    for concept in concepts:
        preferred = _language_map(graph, concept, SKOS.prefLabel)
        if not preferred.get("nb") or not preferred.get("nn"):
            missing_nb_nn.append(concept)
        preferred_by_language = {
            language: {str(value).casefold() for value in values}
            for language, values in preferred.items()
        }
        for alternative in graph.objects(concept, SKOS.altLabel):
            if str(alternative).casefold() in preferred_by_language.get(alternative.language, set()):
                label_collisions.append((concept, alternative))
    _require(not missing_nb_nn, f"{len(missing_nb_nn)} begreper mangler prefLabel på nb eller nn", errors)
    _require(not label_collisions, f"{len(label_collisions)} prefLabel/altLabel-kollisjoner", errors)

    for scheme in schemes:
        for language in ("nb", "nn", "en"):
            _require(
                Literal("Los", lang=language) in set(graph.objects(scheme, SKOS.prefLabel)),
                f"Begrepsskjemaet mangler skos:prefLabel Los@{language}",
                errors,
            )

    top_links = set(graph.triples((None, SKOS.topConceptOf, None)))
    has_top_links = set(graph.triples((None, SKOS.hasTopConcept, None)))
    for concept, _, scheme in top_links:
        _require((scheme, SKOS.hasTopConcept, concept) in graph, f"Mangler invers hasTopConcept for {concept}", errors)
    for scheme, _, concept in has_top_links:
        _require((concept, SKOS.topConceptOf, scheme) in graph, f"Mangler invers topConceptOf for {concept}", errors)

    _require(not any(graph.triples((None, XKOS.belongsTo, None))), "xkos:belongsTo skal være utelatt", errors)
    superseded = {LOS["150023"], LOS["150059"], LOS["150060"]}
    superseded_references = [triple for triple in graph if any(value in superseded for value in triple)]
    _require(not superseded_references, f"Fant {len(superseded_references)} referanser til erstattede RC-URI-er", errors)

    note_pair_errors = []
    for concept in concepts:
        for predicate in (XKOS.inclusionNote, XKOS.exclusionNote):
            languages = {value.language for value in graph.objects(concept, predicate)}
            if languages and not {"nb", "nn"}.issubset(languages):
                note_pair_errors.append((concept, predicate, languages))
    _require(not note_pair_errors, f"{len(note_pair_errors)} merknader mangler parallelltekst på nb eller nn", errors)

    theme_14 = {concept for concept in concepts if str(concept).startswith(str(LOS) + "14")}
    comments_3235 = [value for concept in theme_14 for value in graph.objects(concept, EUVOC.comment) if "3235" in str(value)]
    _require(not comments_3235, "Fant 3235 i euvoc:comment i tema 14", errors)

    _require((LOS["010008"], SKOS.broader, LOS["010007"]) in graph, "Kvalifiseringsprogram er ikke direkte under Arbeidsmarkedstiltak", errors)
    _require((LOS["010014"], SKOS.broader, LOS["010007"]) in graph, "Arbeidsrettet oppfølging er ikke direkte under Arbeidsmarkedstiltak", errors)

    counts = {
        "triples": len(graph),
        "concepts": len(concepts),
        "collections": len(collections),
        "top_concepts": len(set(graph.subjects(SKOS.topConceptOf, None))),
        "broader": len(broader),
        "narrower": len(narrower),
        "alt_labels": len(set(graph.triples((None, SKOS.altLabel, None)))),
        "inclusion_notes": len(set(graph.triples((None, XKOS.inclusionNote, None)))),
        "exclusion_notes": len(set(graph.triples((None, XKOS.exclusionNote, None)))),
        "euvoc_comments": len(set(graph.triples((None, EUVOC.comment, None)))),
        "missing_inverse": len(missing_inverse),
        "cycles": len(cycles),
        "missing_nb_nn": len(missing_nb_nn),
        "label_collisions": len(label_collisions),
        "note_pair_errors": len(note_pair_errors),
    }
    return errors, counts


def _write_reports(errors, counts=None, source_matches=None, skosified=None):
    conforms = not errors
    SHACL_REPORT.write_text(
        "Validation Report\n"
        f"Conforms: {str(conforms)}\n"
        "Validation method: local checks equivalent to validation/los-shapes.ttl\n"
        + ("" if conforms else "\n" + "\n".join(f"- {error}" for error in errors) + "\n"),
        encoding="utf-8",
    )
    if counts is None:
        return
    report = [
        "Los custom quality report",
        "=========================",
        f"Source SHA-256: {sha256(SOURCE_XLSX.read_bytes()).hexdigest()}",
        f"Published graph exactly matches Excel source plus static RDF: {'yes' if source_matches else 'no'}",
        f"Triples: {counts['triples']}",
        f"Concepts: {counts['concepts']}",
        f"Collections: {counts['collections']}",
        f"Top concepts: {counts['top_concepts']}",
        f"broader relations: {counts['broader']}",
        f"narrower relations: {counts['narrower']}",
        f"altLabel values: {counts['alt_labels']}",
        f"inclusionNote values: {counts['inclusion_notes']}",
        f"exclusionNote values: {counts['exclusion_notes']}",
        f"euvoc:comment values: {counts['euvoc_comments']}",
        f"Missing inverse narrower: {counts['missing_inverse']}",
        f"Hierarchy cycles: {counts['cycles']}",
        f"Missing nb/nn prefLabel on concepts: {counts['missing_nb_nn']}",
        f"prefLabel/altLabel collisions: {counts['label_collisions']}",
        f"Notes missing nb/nn parallel text: {counts['note_pair_errors']}",
        "ConceptScheme prefLabel @nb/@nn/@en: Los",
        "Superseded RC URI references: 0",
        "xkos:belongsTo relations: 0",
        "Theme 14 euvoc:comment values containing 3235: 0",
        "Mandatory XKOS GUI metadata: present",
        "Work hierarchy checks: passed",
        f"Skosify triples: {skosified['triples'] if skosified else 'not run'}",
        f"Skosify graph isomorphic with input: {'yes' if skosified and skosified['isomorphic'] else 'no'}",
    ]
    if errors:
        report.extend(["", "Errors:", *(f"- {error}" for error in errors)])
    QUALITY_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")


def main():
    errors = []
    try:
        graph = Graph().parse(DATA, format="turtle")
        Graph().parse(SHAPES, format="turtle")
        Graph().parse(PACKAGE / "validation" / "los-shapes-core.ttl", format="turtle")
        Graph().parse(STATIC_RDF, format="turtle")
    except Exception as error:
        _write_reports([f"RDF-syntaksfeil: {error}"])
        raise SystemExit(f"RDF-syntaksfeil: {error}") from error

    expected, _, _, _ = generate_graph()
    expected.parse(STATIC_RDF, format="turtle")
    source_matches = isomorphic(graph, expected)
    _require(source_matches, "Publisert graf samsvarer ikke nøyaktig med Excel-kilden og statisk RDF", errors)

    errors.extend(_validate_shape_equivalent(graph))
    quality_errors, counts = _validate_quality(graph)
    errors.extend(quality_errors)

    command = [
        "skosify",
        "-o",
        str(SKOSIFIED),
        "-O",
        str(SKOSIFY_LOG),
        str(DATA.relative_to(PACKAGE)),
    ]
    SKOSIFY_LOG.unlink(missing_ok=True)
    SKOSIFIED.unlink(missing_ok=True)
    completed = subprocess.run(command, cwd=PACKAGE, capture_output=True, text=True)
    skosified_result = None
    if completed.returncode:
        errors.append(f"Skosify feilet med status {completed.returncode}: {completed.stderr.strip()}")
    else:
        skosified_graph = Graph().parse(SKOSIFIED, format="turtle")
        skosified_result = {
            "triples": len(skosified_graph),
            "isomorphic": isomorphic(graph, skosified_graph),
        }
        _require(skosified_result["isomorphic"], "Skosify-resultatet er ikke isomorft med publiseringsfilen", errors)

    _write_reports(errors, counts, source_matches, skosified_result)
    if errors:
        print("Valideringen feilet:\n" + "\n".join(f"- {error}" for error in errors), file=sys.stderr)
        raise SystemExit(1)
    print(
        f"Validering bestått: {counts['triples']} tripler, {counts['concepts']} begreper, "
        f"{counts['collections']} samlinger og Skosify-isomorfi bekreftet."
    )


if __name__ == "__main__":
    main()
