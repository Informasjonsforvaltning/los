# Endringslogg

## Release Candidate 1 – språk- og etikettkvalitet, 2026-08-24

- Kvalitetssikret foretrukne etiketter på bokmål, nynorsk og engelsk tema for tema og samordnet den semantiske betydningen der det var behov.
- Normalisert alternative etiketter slik at semikolon skiller flere termer, mens komma bevares som del av termen.
- Revidert alternative etiketter og flyttet eksempler og presiseringer til inklusjonsmerknader der de ikke fungerer som reelle synonymer.
- Samordnet inklusjonsmerknader på bokmål og nynorsk.
- Fjernet `3235` fra `los:140011` og fra alle `euvoc:comment`-verdier i tema 14.
- Lagt til en reproduserbar generator for Turtle-filen og et samlet valideringsskript som oppdaterer valideringsartefaktene.
- Regenerert Turtle, Skosify-artefakt, valideringsrapporter og kontrollsummer.

## Release Candidate 1 – revidert infrastruktur og temaet Arbeid, 2026-08-20

- Etablert sidestilte grener for drikkevannsinfrastruktur, spillvannsinfrastruktur og overvannsinfrastruktur.
- Utvidet drikkevannsinfrastruktur med trykkreguleringsanlegg for drikkevann og drikkevannsstasjon.
- Avgrenset spillvannsinfrastruktur fra overvann og lagt til pumpestasjon for spillvann, fordrøyningsanlegg i avløpsnett, overløp i avløpsnett, slamavskiller og tømmestasjon for sanitært avløpsvann.
- Lagt til overvannsinfrastruktur med overvannsnett, flomvei, pumpestasjon, fordrøyningsanlegg, overløp, infiltrasjonsanlegg og renseanlegg.
- Utvidet samlingen «Kommune» (`los:001`) med direkte medlemskap for alle begrepene i de tre grenene. Samlingsinngangen er dermed fullstendig uten at hovedhierarkiet er endret.
- Beholdt eksisterende URI-er for begreper som i hovedsak har samme identitet, selv om de er flyttet eller har fått oppdaterte merknader.
- Gjenbrukt `los:150022` for Spillvannsinfrastruktur og `los:150026` for Pumpestasjon for spillvann. `los:150023` er tatt ut fordi det tidligere mellomnivået Avløpsnett ikke har en direkte etterfølger. Nye begreper bruker `los:150057`–`los:150058` og `los:150061`–`los:150071`.
- Ikke tatt inn resipient for avløpsvann eller resipient for overvann under Infrastruktur, fordi resipient beskriver mottaksområdet og ikke et infrastrukturanlegg.
- Oppdatert bokmåls-, nynorsk- og engelsketiketter samt inklusjons- og eksklusjonsmerknader.
- Lagt inn flerspråklige `rdfs:label` og norske `rdfs:comment` for `xkos:inclusionNote` og `xkos:exclusionNote`. Metadataene ligger i en fast RDF-kildefil, flettes inn ved regenerering og kontrolleres av SHACL.
- Normalisert produktnavnet til «Los» i begrepsskjemaets metadata.
- Samordnet begrepsidentiteten på bokmål, nynorsk og engelsk for `los:010005` Arbeidsmiljø, `los:010006` Arbeidssøking, `los:010007` Arbeidsmarkedstiltak, `los:010009` Tilrettelegging i arbeidslivet og `los:010012` Arbeidsledighet og permittering.
- Beholdt URI-er og hierarki i temaet «Arbeid». «Kvalifiseringsprogram» og «Arbeidsrettet oppfølging» er fortsatt underordnet «Arbeidsmarkedstiltak», «Tilrettelagt arbeid» er fortsatt alternativ term, og CV er fortsatt dekket av inklusjonsmerknaden til «Arbeidssøking».
- Regenerert Turtle, Skosify-artefakt, valideringsrapporter og kontrollsummer.

## Release Candidate 1, 2026-08-06

- Standardisert `dct:hasVersion` til `4.0.0-rc.1`.
- Oppdatert `dct:issued` til publiseringsdatoen 2026-08-06.
- Endret statusbeskrivelsen fra betaversjon til publiseringskandidat på bokmål, utgivingskandidat på nynorsk og release candidate på engelsk.
- Samordnet metadataene i Excel-kilden, den autoritative Turtle-filen og valideringsartefaktet.
- Regenerert valideringsrapporter og SHA-256-kontrollsummer.

## Publiseringspakke 2026-07-10

- Generert Turtle fra Excel-kilden.
- Generert inverse `skos:narrower` for alle direkte `skos:broader`-relasjoner.
- Utelatt `xkos:belongsTo` etter avtale.
- Lagt til `skos:prefLabel "Los"` på `skos:ConceptScheme` for språkene `nb`, `nn` og `en`.
- Validert Turtle-syntaks med RDFLib.
- Validert Los-regler med pySHACL.
- Kjørt Skosify og kontrollert at antall RDF-tripler er uendret.
- Kontrollert hierarkiet for sykler og manglende inverse relasjoner.
- Opprettet publiseringsdokumentasjon og kontrollsummer.

## Merknad

Den opprinnelige publiseringspakken fra 10. juli 2026 beholdt eksisterende versjons- og utgivelsesmetadata. Disse metadataene er oppdatert i Release Candidate 1.
