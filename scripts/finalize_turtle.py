"""Validate generated Los data and merge mandatory static RDF metadata."""

from collections import defaultdict
from pathlib import Path
import posixpath
import re
from xml.etree import ElementTree
from zipfile import ZipFile

from rdflib import Graph, Literal, Namespace, RDFS


PACKAGE = Path(__file__).resolve().parents[1]
DATA = PACKAGE / "data" / "los.ttl"
SOURCE_XLSX = PACKAGE / "source" / "los-source.xlsx"
STATIC_RDF = PACKAGE / "source" / "xkos-property-labels.ttl"
LOS = Namespace("https://id.norge.no/los/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
XKOS = Namespace("http://rdf-vocabulary.ddialliance.org/xkos#")

MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
ALT_LABEL_HEADERS = {
    "skos:altLabel@nb": "nb",
    "skos:altLabel@nn": "nn",
    "skos:altLabel@en": "en",
}

REQUIRED = {
    XKOS.inclusionNote: {
        RDFS.label: {
            Literal("Omfatter", lang="nb"),
            Literal("Omfattar", lang="nn"),
            Literal("Includes", lang="en"),
        },
        RDFS.comment: {
            Literal("Eksempler og presiseringer av hva begrepet omfatter.", lang="nb"),
            Literal("Døme og presiseringar av kva omgrepet omfattar.", lang="nn"),
        },
    },
    XKOS.exclusionNote: {
        RDFS.label: {
            Literal("Omfatter ikke", lang="nb"),
            Literal("Omfattar ikkje", lang="nn"),
            Literal("Excludes", lang="en"),
        },
        RDFS.comment: {
            Literal("Eksempler og presiseringer av hva begrepet ikke omfatter.", lang="nb"),
            Literal("Døme og presiseringar av kva omgrepet ikkje omfattar.", lang="nn"),
        },
    },
}


def _xml(archive, member):
    return ElementTree.fromstring(archive.read(member))


def _shared_strings(archive):
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = _xml(archive, "xl/sharedStrings.xml")
    return ["".join(node.text or "" for node in item.iter(f"{{{MAIN_NS}}}t")) for item in root]


def _column_index(reference):
    match = re.match(r"([A-Z]+)", reference)
    if not match:
        raise SystemExit(f"Ugyldig cellereferanse i Excel-kilden: {reference}")
    result = 0
    for character in match.group(1):
        result = result * 26 + ord(character) - ord("A") + 1
    return result - 1


def _cell_value(cell, shared_strings):
    cell_type = cell.get("t")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.iter(f"{{{MAIN_NS}}}t"))
    value = cell.find(f"{{{MAIN_NS}}}v")
    if value is None or value.text is None:
        return ""
    if cell_type == "s":
        return shared_strings[int(value.text)]
    return value.text


def _worksheet_rows(archive):
    shared_strings = _shared_strings(archive)
    workbook = _xml(archive, "xl/workbook.xml")
    relationships = _xml(archive, "xl/_rels/workbook.xml.rels")
    targets = {
        relation.get("Id"): relation.get("Target")
        for relation in relationships.findall(f"{{{PACKAGE_REL_NS}}}Relationship")
    }
    for sheet in workbook.findall(f".//{{{MAIN_NS}}}sheet"):
        relationship_id = sheet.get(f"{{{OFFICE_REL_NS}}}id")
        target = targets.get(relationship_id)
        if not target:
            raise SystemExit(f"Fant ikke regnearkdata for arket {sheet.get('name')}.")
        member = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))
        root = _xml(archive, member)
        rows = []
        for row in root.findall(f".//{{{MAIN_NS}}}sheetData/{{{MAIN_NS}}}row"):
            values = {}
            for cell in row.findall(f"{{{MAIN_NS}}}c"):
                values[_column_index(cell.get("r", ""))] = _cell_value(cell, shared_strings)
            rows.append((int(row.get("r", len(rows) + 1)), values))
        yield sheet.get("name"), rows


def expected_alt_labels(source_xlsx=SOURCE_XLSX):
    """Read canonical altLabel lists, using semicolon as the only delimiter."""
    expected = defaultdict(set)
    source_errors = []
    with ZipFile(source_xlsx) as archive:
        for sheet_name, rows in _worksheet_rows(archive):
            if not rows:
                continue
            _, header_row = rows[0]
            headers = {str(value).strip(): column for column, value in header_row.items()}
            uri_column = headers.get("URI")
            alt_columns = {
                language: headers[header]
                for header, language in ALT_LABEL_HEADERS.items()
                if header in headers
            }
            if uri_column is None or not alt_columns:
                continue
            for row_number, row in rows[1:]:
                compact_uri = str(row.get(uri_column, "")).strip()
                if not compact_uri:
                    continue
                if not compact_uri.startswith("los:"):
                    source_errors.append(f"{sheet_name}!rad {row_number}: ugyldig URI {compact_uri!r}")
                    continue
                subject = LOS[compact_uri.removeprefix("los:")]
                expected[subject]
                for language, column in alt_columns.items():
                    raw_value = str(row.get(column, ""))
                    if not raw_value:
                        continue
                    labels = [label.strip() for label in raw_value.split(";")]
                    canonical_value = "; ".join(labels)
                    if any(not label for label in labels):
                        source_errors.append(
                            f"{sheet_name}!rad {row_number} ({compact_uri}, {language}): tom alternativ term"
                        )
                        continue
                    if raw_value != canonical_value:
                        source_errors.append(
                            f"{sheet_name}!rad {row_number} ({compact_uri}, {language}): "
                            "bruk semikolon etterfulgt av ett mellomrom som skilletegn"
                        )
                    normalized = [label.casefold() for label in labels]
                    if len(normalized) != len(set(normalized)):
                        source_errors.append(
                            f"{sheet_name}!rad {row_number} ({compact_uri}, {language}): duplisert alternativ term"
                        )
                    expected[subject].update(Literal(label, lang=language) for label in labels)
    if source_errors:
        details = "\n".join(f"- {error}" for error in source_errors)
        raise SystemExit(f"Ugyldige skos:altLabel-verdier i Excel-kilden:\n{details}")
    return expected


def _literal_text(literal):
    language = f"@{literal.language}" if literal.language else ""
    return f"{str(literal)!r}{language}"


def validate_generated_alt_labels(graph, expected):
    """Require a one-to-one match between source cells and generated RDF."""
    actual_subjects = {
        subject
        for subject in graph.subjects(SKOS.altLabel, None)
        if str(subject).startswith(str(LOS))
    }
    mismatches = []
    for subject in sorted(set(expected) | actual_subjects, key=str):
        expected_values = expected.get(subject, set())
        actual_values = set(graph.objects(subject, SKOS.altLabel))
        missing = sorted(expected_values - actual_values, key=lambda value: (value.language or "", str(value)))
        unexpected = sorted(actual_values - expected_values, key=lambda value: (value.language or "", str(value)))
        if missing or unexpected:
            compact_uri = f"los:{str(subject).removeprefix(str(LOS))}"
            details = []
            if missing:
                details.append("mangler " + ", ".join(_literal_text(value) for value in missing))
            if unexpected:
                details.append("har uventet " + ", ".join(_literal_text(value) for value in unexpected))
            mismatches.append(f"{compact_uri}: {'; '.join(details)}")
    if mismatches:
        details = "\n".join(f"- {mismatch}" for mismatch in mismatches)
        raise SystemExit(
            "Generert skos:altLabel samsvarer ikke med Excel-kilden. "
            "Semikolon skal skille alternative termer; komma skal bevares i termen.\n"
            f"{details}"
        )


def main():
    graph = Graph().parse(DATA, format="turtle")
    expected = expected_alt_labels()
    validate_generated_alt_labels(graph, expected)

    graph.parse(STATIC_RDF, format="turtle")
    graph.bind("rdfs", RDFS, replace=True)
    graph.bind("xkos", XKOS, replace=True)

    for subject, predicates in REQUIRED.items():
        for predicate, expected_values in predicates.items():
            missing = expected_values - set(graph.objects(subject, predicate))
            if missing:
                raise SystemExit(
                    f"Mangler obligatorisk XKOS-metadata: {subject} {predicate} {sorted(map(str, missing))}"
                )

    temporary = DATA.with_suffix(".ttl.tmp")
    temporary.write_bytes(graph.serialize(format="turtle", encoding="utf-8"))
    temporary.replace(DATA)
    alt_label_count = sum(len(values) for values in expected.values())
    print(
        f"Validert {alt_label_count} alternative termer mot Excel-kilden og oppdatert {DATA} "
        f"med obligatorisk XKOS-metadata; {len(graph)} RDF-tripler."
    )


if __name__ == "__main__":
    main()
