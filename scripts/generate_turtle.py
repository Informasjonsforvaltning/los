"""Generate the Los SKOS graph from the authoritative Excel source."""

from collections import defaultdict
from datetime import date
from pathlib import Path
import re
from zipfile import ZipFile

from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import DCTERMS, OWL, SKOS, XSD

from finalize_turtle import _worksheet_rows


PACKAGE = Path(__file__).resolve().parents[1]
SOURCE_XLSX = PACKAGE / "source" / "los-source.xlsx"
DATA = PACKAGE / "data" / "los.ttl"

DEFAULT_PREFIXES = {
    "los": "https://id.norge.no/los/",
    "skos": str(SKOS),
    "xkos": "http://rdf-vocabulary.ddialliance.org/xkos#",
    "dct": str(DCTERMS),
    "euvoc": "https://publications.europa.eu/ontology/euvoc#",
    "concept-status": "http://publications.europa.eu/resource/authority/concept-status/",
    "owl": str(OWL),
    "rdf": str(RDF),
}

LANGUAGE_FIELD = re.compile(r"^(?P<predicate>[^@]+)@(?P<language>[A-Za-z-]+)$")


def _nonempty_rows(source_xlsx=SOURCE_XLSX):
    with ZipFile(source_xlsx) as archive:
        for sheet_name, rows in _worksheet_rows(archive):
            yield sheet_name, [
                (row_number, values)
                for row_number, values in rows
                if any(str(value).strip() for value in values.values())
            ]


def _header_and_sheets(source_xlsx=SOURCE_XLSX):
    header = {}
    sheets = []
    for sheet_name, rows in _nonempty_rows(source_xlsx):
        if sheet_name == "Header":
            for row_number, values in rows[1:]:
                key = str(values.get(0, "")).strip()
                value = str(values.get(1, "")).strip()
                if not key:
                    continue
                if key in header and header[key] != value:
                    raise SystemExit(
                        f"Motstridende verdier for {key!r} i Header-arket, senest på rad {row_number}."
                    )
                header[key] = value
        else:
            sheets.append((sheet_name, rows))
    return header, sheets


def _prefixes(header):
    result = dict(DEFAULT_PREFIXES)
    for key, value in header.items():
        if key.startswith("prefix:"):
            result[key.removeprefix("prefix:")] = value
    return result


def _resource(value, prefixes):
    value = str(value).strip()
    if not value:
        raise ValueError("Tom ressursverdi")
    if value.startswith(("http://", "https://")):
        return URIRef(value)
    if ":" not in value:
        raise ValueError(f"Ressursen {value!r} mangler prefiks")
    prefix, local_name = value.split(":", 1)
    if prefix not in prefixes:
        raise ValueError(f"Ukjent prefiks {prefix!r} i {value!r}")
    return URIRef(prefixes[prefix] + local_name)


def _predicate(value, prefixes):
    return _resource(value, prefixes)


def _split_references(value):
    return [item.strip() for item in re.split(r"[,;]", str(value)) if item.strip()]


def _add_scheme_metadata(graph, header, prefixes):
    scheme_value = header.get("conceptscheme.uri")
    if not scheme_value:
        raise SystemExit("Header-arket mangler conceptscheme.uri.")
    scheme = URIRef(scheme_value)
    graph.add((scheme, RDF.type, SKOS.ConceptScheme))

    for key, value in header.items():
        if not value or key.startswith("prefix:") or key == "conceptscheme.uri":
            continue
        match = LANGUAGE_FIELD.match(key)
        if match:
            predicate = _predicate(match.group("predicate"), prefixes)
            language = match.group("language")
            graph.add((scheme, predicate, Literal(value, lang=language)))
            if predicate == DCTERMS.title:
                graph.add((scheme, SKOS.prefLabel, Literal(value, lang=language)))
            continue
        predicate = _predicate(key, prefixes)
        if predicate == DCTERMS.issued:
            try:
                parsed = date.fromisoformat(value)
            except ValueError as error:
                raise SystemExit(f"Ugyldig dct:issued-dato {value!r}.") from error
            graph.add((scheme, predicate, Literal(parsed.isoformat(), datatype=XSD.date)))
        elif predicate == DCTERMS.license:
            graph.add((scheme, predicate, URIRef(value)))
        else:
            graph.add((scheme, predicate, Literal(value)))
    return scheme


def _add_source_rows(graph, sheets, scheme, prefixes):
    seen = {}
    concept_broader = defaultdict(set)
    collection_members = defaultdict(set)
    concepts = set()
    collections = set()

    for sheet_name, rows in sheets:
        if not rows:
            continue
        _, header_values = rows[0]
        headers = {column: str(value).strip() for column, value in header_values.items()}
        uri_column = next((column for column, header in headers.items() if header == "URI"), None)
        if uri_column is None:
            continue
        for row_number, values in rows[1:]:
            compact_uri = str(values.get(uri_column, "")).strip()
            if not compact_uri:
                continue
            subject = _resource(compact_uri, prefixes)
            if subject in seen:
                previous_sheet, previous_row = seen[subject]
                raise SystemExit(
                    f"Duplisert URI {compact_uri}: {previous_sheet}!{previous_row} og {sheet_name}!{row_number}."
                )
            seen[subject] = (sheet_name, row_number)

            row_type = None
            broader_values = []
            for column, header_name in headers.items():
                raw_value = str(values.get(column, "")).strip()
                if not raw_value or header_name in {"URI", "xkos:belongsTo"}:
                    continue
                if header_name == "rdf:type":
                    row_type = _resource(raw_value, prefixes)
                    graph.add((subject, RDF.type, row_type))
                elif header_name == "skos:broader":
                    broader_values = _split_references(raw_value)
                    for reference in broader_values:
                        broader = _resource(reference, prefixes)
                        graph.add((subject, SKOS.broader, broader))
                        graph.add((broader, SKOS.narrower, subject))
                        concept_broader[subject].add(broader)
                elif header_name == "^skos:member":
                    for reference in _split_references(raw_value):
                        collection = _resource(reference, prefixes)
                        graph.add((collection, SKOS.member, subject))
                        collection_members[collection].add(subject)
                elif header_name == "euvoc:status":
                    status = raw_value if ":" in raw_value else f"concept-status:{raw_value}"
                    graph.add((subject, _predicate("euvoc:status", prefixes), _resource(status, prefixes)))
                elif header_name == "euvoc:comment":
                    graph.add((subject, _predicate(header_name, prefixes), Literal(raw_value)))
                else:
                    match = LANGUAGE_FIELD.match(header_name)
                    if not match:
                        raise SystemExit(
                            f"Ukjent kolonne med verdi i {sheet_name}!rad {row_number}: {header_name!r}."
                        )
                    predicate = _predicate(match.group("predicate"), prefixes)
                    language = match.group("language")
                    values_to_add = [raw_value]
                    if predicate == SKOS.altLabel:
                        values_to_add = [item.strip() for item in raw_value.split(";")]
                        if any(not item for item in values_to_add):
                            raise SystemExit(
                                f"Tom alternativ term i {sheet_name}!rad {row_number}, {header_name}."
                            )
                    for literal_value in values_to_add:
                        graph.add((subject, predicate, Literal(literal_value, lang=language)))

            if row_type == SKOS.Concept:
                concepts.add(subject)
                graph.add((subject, SKOS.inScheme, scheme))
            elif row_type == SKOS.Collection:
                collections.add(subject)
            else:
                raise SystemExit(
                    f"Ugyldig eller manglende rdf:type for {compact_uri} i {sheet_name}!rad {row_number}."
                )

    for concept in concepts:
        if not concept_broader.get(concept):
            graph.add((concept, SKOS.topConceptOf, scheme))
            graph.add((scheme, SKOS.hasTopConcept, concept))

    missing_broader = sorted(
        {broader for values in concept_broader.values() for broader in values} - concepts,
        key=str,
    )
    missing_collections = sorted(set(collection_members) - collections, key=str)
    invalid_members = sorted(
        {member for members in collection_members.values() for member in members} - concepts,
        key=str,
    )
    if missing_broader or missing_collections or invalid_members:
        details = []
        if missing_broader:
            details.append("ukjente overbegreper: " + ", ".join(map(str, missing_broader)))
        if missing_collections:
            details.append("ukjente samlinger: " + ", ".join(map(str, missing_collections)))
        if invalid_members:
            details.append("ukjente samlingsmedlemmer: " + ", ".join(map(str, invalid_members)))
        raise SystemExit("Ugyldige referanser i Excel-kilden: " + "; ".join(details))

    return concepts, collections


def generate_graph(source_xlsx=SOURCE_XLSX):
    header, sheets = _header_and_sheets(source_xlsx)
    prefixes = _prefixes(header)
    graph = Graph()
    for prefix, namespace in prefixes.items():
        graph.bind(prefix, Namespace(namespace), replace=True)
    scheme = _add_scheme_metadata(graph, header, prefixes)
    concepts, collections = _add_source_rows(graph, sheets, scheme, prefixes)
    return graph, scheme, concepts, collections


def main():
    graph, _, concepts, collections = generate_graph()
    temporary = DATA.with_suffix(".ttl.generated.tmp")
    temporary.write_bytes(graph.serialize(format="turtle", encoding="utf-8"))
    temporary.replace(DATA)
    print(
        f"Genererte {DATA} fra {SOURCE_XLSX}: {len(concepts)} begreper, "
        f"{len(collections)} samlinger og {len(graph)} RDF-tripler før sluttføring."
    )


if __name__ == "__main__":
    main()
