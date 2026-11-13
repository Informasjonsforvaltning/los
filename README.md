# Los publiseringspakke

Denne pakken inneholder en publiseringsklar kandidat av Los som SKOS-vokabular, kildegrunnlag og valideringsressurser.

## Versjon

Metadata i vokabularet angir:

- `dct:hasVersion`: `4.0.0-rc.1`
- `owl:versionInfo`: `Los 4.0 RC1`
- `dct:issued`: `2026-08-06`

Publiseringspakken ble satt sammen 6. august 2026 og sist oppdatert 24. august 2026. Oppdateringen omfatter revidert struktur for drikkevanns-, spillvanns- og overvannsinfrastruktur, utvidet medlemskap i samlingen «Kommune» og en samlet kvalitetssikring av etiketter og inklusjonsmerknader på bokmål, nynorsk og engelsk. Versjonsnummer og utgivelsesdato er beholdt.

## Innhold

- `data/los.ttl`: autoritativ Turtle-fil for publisering
- `source/los-source.xlsx`: Excel-kilden som Turtle-filen er basert på
- `source/xkos-property-labels.ttl`: obligatoriske etiketter og beskrivelser for XKOS-egenskaper i brukergrensesnittet
- `scripts/generate_turtle.py`: genererer Los-grafen fra Excel-kilden
- `scripts/finalize_turtle.py`: fletter obligatorisk statisk RDF inn i en regenerert Turtle-fil
- `scripts/validate_release.py`: validerer publiseringsfilen og oppdaterer valideringsartefaktene
- `validation/los-shapes.ttl`: komplette SHACL-regler for Los
- `validation/los-shapes-core.ttl`: kjerneutgave av SHACL-reglene
- `validation/shacl-report.txt`: resultat fra SHACL-kontrollen
- `validation/skosify.log`: meldinger fra Skosify
- `validation/los-skosified.ttl`: Turtle skrevet ut av Skosify
- `validation/custom-quality-report.txt`: supplerende kvalitetskontroller
- `docs/`: redigerbare Markdown-mastere og inngang til dokumentasjonen
- `documentation/CHANGELOG.md`: endringslogg for pakken
- `documentation/VALIDATION.md`: valideringsmetode og resultater
- `documentation/LICENSE.txt`: lisensinformasjon
- `documentation/source/`: Word-kilder fra RC1 og det uendrede høringsnotatet
- `SHA256SUMS.txt`: kontrollsummer for alle filer i pakken

## Gjeldende dokumentgrunnlag

Følgende dokumenter er redigerbare mastere og gjeldende arbeidsgrunnlag:

- [`docs/formal-og-bruksomrader.md`](docs/formal-og-bruksomrader.md)
- [`docs/design-og-modelleringsprinsipper.md`](docs/design-og-modelleringsprinsipper.md)

De er merket «Redaktørens utkast» og kan endres etter behandling av høringssvar. Word-utgavene i `documentation/source/` beholdes som kildekopier fra RC1, men skal ikke redigeres parallelt med Markdown-filene.

Høringsnotatet beholdes uendret og kun som Word-fil: [`documentation/source/horingsnotat-los-4-0.docx`](documentation/source/horingsnotat-los-4-0.docx). En samlet inngang til dokumentasjonen finnes i [`docs/`](docs/index.md).

Historiske dokumentutkast er ikke lagt inn i arbeidsgrenen for Los 4.

## Nøkkeltall

- 638 `skos:Concept`
- 10 `skos:Collection`
- 15 toppbegreper
- 623 `skos:broader`
- 623 inverse `skos:narrower`
- 7 022 RDF-tripler

`xkos:belongsTo` er ikke tatt med i denne utgaven.

## Valideringsstatus

- RDF/Turtle-parsing: bestått
- SHACL: `Conforms: True`
- Hierarkiske sykler: ingen funnet
- Manglende inverse `skos:narrower`: ingen
- Manglende bokmåls- eller nynorsketiketter på begreper: ingen
- Obligatoriske etiketter og beskrivelser for `xkos:inclusionNote` og `xkos:exclusionNote`: til stede
- Begrepsidentiteten for de reviderte begrepene under «Arbeid» er samordnet på bokmål, nynorsk og engelsk
- Samsvar med Excel-kilden og statisk RDF: identisk graf
- `skos:prefLabel`/`skos:altLabel`-kollisjoner: ingen
- Inklusjons- og eksklusjonsmerknader uten parallelltekst på bokmål og nynorsk: ingen
- Skosify: fullført, 7 022 tripler inn og ut; resultatet er isomorft med publiseringsfilen

Skosify-loggen inneholder informative meldinger om at verktøyet ikke transformerer enkelte XKOS- og EUVoc-egenskaper. Egenskapene er beholdt.

## Bruk

Autoritativ publiseringsfil er `data/los.ttl`. `validation/los-skosified.ttl` er et valideringsartefakt og skal ikke erstatte den autoritative filen uten en eksplisitt beslutning.

Hele byggingen og valideringen kjøres slik:

```bash
python3 scripts/generate_turtle.py
python3 scripts/finalize_turtle.py
python3 scripts/validate_release.py
```

Faglige endringer gjøres i `source/los-source.xlsx`. Deretter regenereres `data/los.ttl`, statisk RDF flettes inn og hele pakken valideres. Pull requests skal inneholde både kildeendringen og de regenererte artefaktene.

## Arbeidsflyt i GitHub

1. Opprett eller bruk et issue som beskriver behovet og ønsket resultat.
2. Gjør endringen i en egen gren.
3. Kjør generering og validering lokalt.
4. Opprett en pull request til `master` og knytt den til issuet.
5. Slå sammen etter faglig kontroll og bestått automatisk validering.

Grenen `gh-pages` forvaltes separat. Den inneholder avviklingssiden for Los 3 og oppdateres ikke automatisk fra `master`.

Sluttføringen kontrollerer først at genererte `skos:altLabel` samsvarer én-til-én med Excel-kilden. Flere alternative termer i samme celle skal være skilt med semikolon, mens komma bevares som en del av termen. Ved avvik stoppes steget før Turtle-filen overskrives. Deretter flettes `source/xkos-property-labels.ttl` inn. Valideringen kontrollerer blant annet RDF-syntaks, reglene i SHACL-formene, nøyaktig samsvar med kildegrunnlaget, hierarkiet, språkparallellitet, etikettkollisjoner og Skosify-isomorfi.

## Lisens

Vokabularet angir Creative Commons Navngivelse 4.0 internasjonal, CC BY 4.0, i `dct:license`.
