# Validering av Los

Valideringen er kjørt på nytt for Release Candidate 1 den 24. august 2026 etter kvalitetssikringen av foretrukne etiketter, alternative etiketter og inklusjonsmerknader på bokmål, nynorsk og engelsk.

## RDF-syntaks

`data/los.ttl` er lest som Turtle med RDFLib uten parserfeil.

## SHACL

Kravene i `validation/los-shapes.ttl` er kontrollert med en lokal, tilsvarende validering. Kontrollen dekker de samme kravene til begreper, språkmerkede etiketter, tilhørighet til begrepsskjema, hierarkiske relasjoner, toppbegreper og samlinger. Den kontrollerer også de obligatoriske etikettene og beskrivelsene for `xkos:inclusionNote` og `xkos:exclusionNote`. pySHACL var ikke tilgjengelig i arbeidsmiljøet ved denne regenereringen.

Resultat:

```text
Validation Report
Conforms: True
```

Rapporten angir også hvilken valideringsmetode som er brukt.

Når pySHACL er tilgjengelig, kan kontrollen i tillegg kjøres slik:

```bash
pyshacl -s validation/los-shapes.ttl -f human data/los.ttl
```

## Skosify

Skosify fullførte og produserte en graf som er isomorf med publiseringsfilen. Begge grafene inneholder 7 022 tripler.

```bash
skosify -o validation/los-skosified.ttl \
  -O validation/skosify.log data/los.ttl
```

Loggen inneholder bare informative meldinger om egenskaper Skosify ikke har egne transformasjonsregler for:

- `xkos:exclusionNote`
- `xkos:inclusionNote`
- `euvoc:comment`
- `euvoc:status`

Egenskapene er beholdt i resultatet.

## Supplerende kontroller

Følgende er kontrollert programmatisk:

- symmetri mellom `skos:broader` og `skos:narrower`
- fravær av hierarkiske sykler
- nøyaktig samsvar mellom publiseringsfilen og grafen generert fra Excel-kilden og den statiske RDF-filen
- bokmåls- og nynorsketikett på alle begreper
- fravær av kollisjoner mellom `skos:prefLabel` og `skos:altLabel` på samme språk
- at inklusjons- og eksklusjonsmerknader har parallelltekst på bokmål og nynorsk
- `skos:prefLabel` på begrepsskjemaet på `nb`, `nn` og `en`
- at alle medlemmer av samlinger er Los-begreper
- at `los:150022` og `los:150026` er aktive med oppdatert betydning, og at de erstattede RC-URI-ene `los:150023`, `los:150059` og `los:150060` ikke forekommer
- at obligatoriske `rdfs:label` og `rdfs:comment` for XKOS-egenskapene er med og har riktig ordlyd og språkmerking
- at `los:010005`, `los:010006`, `los:010007`, `los:010009` og `los:010012` har samordnet begrepsidentitet på bokmål, nynorsk og engelsk
- at «Kvalifiseringsprogram» og «Arbeidsrettet oppfølging» fortsatt er direkte underordnet «Arbeidsmarkedstiltak»
- at verdien `3235` ikke forekommer i `euvoc:comment` i tema 14

## SKOS Play

Filen er struktur- og syntaksmessig klargjort for import i SKOS Play. En ekstern interaktiv opplasting er ikke en del av denne lokale publiseringspakken.
