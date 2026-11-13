# Los 4 – design- og modelleringsprinsipper

> **Status:** Redaktørens utkast<br>
> **Grunnlag:** Los 4.0 RC1<br>
> **Merknad:** Dokumentet er gjeldende arbeidsgrunnlag, men kan endres etter behandling av høringssvar.

*Styrende redaksjonelle og arkitektoniske prinsipper for utvikling og forvaltning av Los 4.*


## 1. Formål og arkitektur

Los er et felles tematisk vokabular for offentlig sektor. Hierarkiet i Los skal gi en stabil tematisk klassifisering av offentlige tjenester, informasjon, datasett og andre ressurser på tvers av virksomheter, forvaltningsnivåer og anvendelser.

En sentral funksjon for Los er å være en felles tematisk overbygning for standarder, vokabularer og klassifikasjoner som brukes i ulike deler av offentlig sektor. Sektorene kan beholde sin faglige struktur og detaljeringsgrad, mens koblinger til Los gjør det mulig å finne og sammenstille tjenester, data og informasjon på tvers.

Strukturen skal bygge på stabile tema- og fagområder, ikke på hvordan den enkelte virksomhet er organisert. Offentlige virksomheter, og særlig kommunene, tilbyr mange av de samme tjenestene, men kan organisere ansvaret for dem ulikt. Los skal gi et felles tematisk lag på tvers av slike organisatoriske forskjeller.

Innbyggerperspektivet er fortsatt viktig, men er ikke alene styrende for begrepsstrukturen. I Los 4 skal semantisk presisjon, stabilitet, gjenbruk og anvendbarhet på tvers av virksomheter og formål veie tungt.

Dette skal blant annet gjøre Los egnet til tematisk oversikt over en virksomhets tjeneste-, informasjons- og ressursportefølje og til samhandling mellom virksomheter. En mer ensartet tematisk klassifisering kan på sikt også gi bedre grunnlag for sammenstilling og rapportering, men dette er ikke et selvstendig formål med Los 4.

Organisasjonsstruktur, livshendelser, målgrupper, nettsteder, plattformer og andre konkrete anvendelser skal som hovedregel ikke være styrende for hierarkiet i Los.


## 2. Entydig plassering i hierarkiet

Et begrep skal ha én entydig plassering i hierarkiet i Los.

Alle begreper i hierarkiet, med unntak av toppbegrepene, skal ha nøyaktig ett direkte overordnet begrep. Toppbegrepene skal ikke ha skos:broader til et annet Los-begrep.

Dette er en grunnleggende regel i Los 4.

Entydig plassering gjør det mulig å bruke hierarkiet begge veier:


- ovenfra og ned, for å se hvilke underområder som inngår i et overordnet tema
- nedenfra og opp, for å fastslå hvilket overordnet tema et mer detaljert begrep tilhører

Dette gjør strukturen bedre egnet til klassifisering, analyse, sammenstilling og tematisk oversikt.

Behovet for å uttrykke at en tjeneste, informasjonsside, et datasett eller en annen ressurs berører flere tema, skal ikke løses ved å gi Los-begreper flere foreldre. Ressursen kan i stedet klassifiseres med flere relevante Los-begreper.

Skillet er grunnleggende:

**Et begrep skal ha én plass i vokabularet. En ressurs kan handle om flere tema.**

Alternative innganger til vokabularet håndteres gjennom andre mekanismer, som SKOS Collections, alternative termer, søk eller supplerende metadata.


## 3. Hierarkiske relasjoner

Hierarkiet i Los uttrykkes med skos:broader og skos:narrower.

Los skiller ikke mellom generiske, partitive eller andre typer hierarkiske relasjoner i hovedmodellen. Den hierarkiske relasjonen uttrykker først og fremst begrepets entydige plass i den tematiske klassifikasjonen.

Partitive relasjoner som xkos:isPartOf og xkos:hasPart inngår derfor ikke i hovedmodellen for Los 4.

Mer spesifikke hierarkiske relasjoner skal bare innføres dersom framtidige og dokumenterte bruksbehov viser at det er nødvendig å kunne skille ulike relasjonstyper maskinelt.

Semantisk presisjon skal ikke økes dersom den først og fremst øker kompleksiteten uten å gi tilsvarende verdi i anvendelsen.


## 4. Bruk hierarkiet aktivt

Bruk eksisterende hierarki før nye begreper eller mellomnivåer opprettes.

Hierarkiet kan ha flere nivåer når dette:


- tilfører semantisk verdi
- representerer en naturlig faglig struktur
- gjør etablerte begreper lettere å plassere
- reduserer behovet for begreper som først og fremst har en strukturerende funksjon

Dybde er ikke et mål i seg selv. Los skal ikke utvikles til et finmasket klassifikasjonssystem.

Nye nivåer bør bare innføres når de representerer stabile og gjenkjennelige tema- eller fagområder og gir dokumentert nytte.


## 5. Modeller tema, ikke organisering

Los skal beskrive hva en tjeneste eller ressurs handler om, ikke hvilken virksomhet, etat, avdeling eller organisatorisk enhet som har ansvaret.

Et tema skal kunne brukes uavhengig av hvordan ansvaret er organisert.

Når flere virksomheter tilbyr sammenlignbare tjenester, skal Los så langt som mulig gi en felles tematisk klassifisering på tvers av organisatoriske forskjeller.

Organisatorisk tilhørighet skal håndteres i andre metadata når dette er relevant.


## 6. Granularitet

Modeller begreper som representerer stabile og gjenbrukbare tema- eller fagområder.

Prosesser, hendelser, enkeltordninger, konkrete tjenester, produkter og plattformer skal normalt ikke modelleres som egne Los-begreper når behovet kan dekkes gjennom et mer stabilt tema.

Behov for høyere detaljeringsgrad skal ikke automatisk føre til nye begreper. Inklusjonsmerknader, alternative termer, samlinger, flere klassifiseringer eller supplerende metadata kan være bedre virkemidler.

Behov for større detaljgrad skal heller ikke automatisk betraktes som virksomhetsinterne. Dersom behovet er felles for flere virksomheter eller en sektor, skal det vurderes om det bør løses gjennom videreutvikling av Los eller gjennom et felles sektorvokabular som kan kobles til Los. Behov som er spesifikke for én virksomhet, kan i større grad håndteres lokalt.

Dagens detaljeringsnivå i Los skal derfor ikke alene være styrende for grensen mellom felles og lokale klassifiseringsbehov. Felles behov bør så langt som mulig løses felles.

Behov for tverrtematisk klassifisering skal normalt løses ved å klassifisere ressursen med flere relevante Los-begreper, ikke ved å endre hierarkiet i Los.


## 7. Begrepsnavn

skos:prefLabel skal være entydig innen hele vokabularet.

Begrepsnavn skal være:


- faglig presise
- gjenkjennelige
- så langt som mulig forståelige uten å kjenne den overordnede konteksten
- basert på etablert språkbruk når dette gir tilstrekkelig presisjon

Etablerte og gjenkjennelige fagbegreper skal normalt foretrekkes framfor nye betegnelser som primært er etablert for å oppnå en mer systematisk struktur.

Semantisk presisjon skal balanseres mot gjenkjennelighet og praktisk anvendbarhet.


## 8. Faglig forankring

Når et temaområde har etablert terminologi, fagstandarder eller relevant regelverk, skal disse brukes som viktige kilder ved vurdering av begreper og struktur.

Lovverk, sektorens terminologi eller etablerte klassifikasjoner skal likevel ikke automatisk kopieres inn i Los. Løsningen må også fungere som del av et sektorovergripende tematisk vokabular og være konsistent med de øvrige modelleringsprinsippene.

Fagpersoner og relevante fagmiljøer bør involveres ved større revisjoner av etablerte temaområder.

Andre vokabularer og klassifikasjoner kan brukes som referanser og sammenligningsgrunnlag, men er ikke i seg selv styrende for Los.


## 9. Los som tematisk overbygning

Los skal fungere som en felles tematisk overbygning for vokabularer og klassifikasjoner som brukes i ulike deler av offentlig sektor.

Virksomhetsinterne og sektorspesifikke vokabularer kan gi større detaljgrad, dekke et avgrenset fagområde eller være utviklet for andre formål. Slike vokabularer og klassifikasjoner kan kobles til Los når det finnes en faglig begrunnet semantisk sammenheng.

Mapping skal bare etableres når det finnes reelt semantisk samsvar, og skal ikke uttrykke sterkere samsvar enn det er faglig grunnlag for.

Los skal ikke utvides med begreper eller strukturer bare for å gjenskape et annet vokabular eller en annen klassifikasjon.

Når slike koblinger er etablert, kan tjenester, data og informasjon finnes og sammenstilles tematisk på tvers av sektorer. Virksomheter og sektorer beholder samtidig den detaljgraden og faglige strukturen de har behov for.


## 10. Krysstematiske vurderinger

Et begrep skal plasseres der det tematisk hører hjemme.

En svak eller feilaktig plassering skal ikke opprettholdes ved hjelp av dokumentasjon, flere foreldre eller andre strukturelle omveier.

Begrepet flyttes i stedet til den plasseringen som best uttrykker det primære temaet.

Når en ressurs berører flere tema, klassifiseres ressursen med flere relevante begreper.


## 11. Alternative termer

skos:altLabel brukes for relevante alternative betegnelser, blant annet:


- synonymer
- dagligtale
- historiske betegnelser
- alternative skrivemåter
- relevante lov- og sektortermer

Alternative termer skal støtte søk, gjenfinning og gjenkjennelighet.

skos:altLabel skal ikke brukes til å skjule uklarhet i valg av foretrukket begrep eller til å representere selvstendige fagbegreper som burde vært vurdert som egne Los-begreper.

Når flere alternative termer registreres i samme celle i Excel-masteren, skal de skilles med semikolon etterfulgt av mellomrom. Komma kan inngå i en alternativ term og skal ikke tolkes som skilletegn.


## 12. Inklusjonsmerknader

Inklusjonsmerknader brukes når de tilfører semantisk informasjon som ikke framgår tydelig av skos:prefLabel eller hierarkiet.

De kan blant annet brukes til å:


- vise eksempler på hva begrepet omfatter
- tydeliggjøre avgrensningen av et tema
- synliggjøre mer detaljerte fenomener som ikke trenger egne begreper
- støtte klassifisering uten å øke detaljeringsgraden i hierarkiet i Los

Inklusjonsmerknader er ikke obligatoriske og skal ikke gjenta informasjon som allerede framgår av begrepsnavnet eller hierarkiet.


## 13. Eksklusjonsmerknader

Eksklusjonsmerknader brukes ved reelle semantiske grenseflater der det er fare for feilklassifisering.

De skal så langt som mulig peke til konkrete Los-begreper eller forklare hvor ressursen i stedet bør klassifiseres.

Eksklusjonsmerknader skal brukes restriktivt og ikke kompensere for en uklar begrepsstruktur.


## 14. Konsistens

Samme type modelleringsproblem skal så langt som mulig løses på samme måte på tvers av temaområdene.

Nye løsninger skal vurderes opp mot eksisterende struktur og tidligere redaksjonelle beslutninger før det etableres nye mønstre.

Konsistens er et viktig hensyn, men skal ikke føre til at det etableres kunstige begreper, mellomnivåer eller strukturer bare for å oppnå symmetri.

Faglige forskjeller mellom temaområder kan begrunne ulike løsninger når dette er dokumentert.


## 15. SKOS Collections

SKOS Collections gir alternative innganger til vokabularet og skal ikke påvirke hierarkiet i Los.

Samlinger grupperer Los-begreper uten å endre begrepenes entydige plassering i hierarkiet. Los bruker i dag samlinger blant annet for livshendelser og forvaltningsnivåer.

Samlinger kan også brukes for andre tverrgående perspektiver eller bestemte anvendelser når det finnes et tydelig behov.

Et begrep kan inngå i flere samlinger uten at dette påvirker plasseringen i hierarkiet.

Samlinger modelleres etter at hierarkiet i Los er etablert.


## 16. Stabil identitet og endringshistorikk

URI-en identifiserer begrepet og skal så langt som mulig være stabil over tid.

Flytting av et begrep i hierarkiet skal normalt ikke føre til ny URI dersom begrepets identitet og betydning er uendret.

Endring av begrepsnavn skal heller ikke i seg selv føre til ny URI dersom det fortsatt er det samme begrepet.

Begreper som tas ut av aktiv bruk, skal ikke slettes uten at konsekvensene for eksisterende bruk er vurdert.

Endringer som påvirker betydning, struktur eller bruk, skal dokumenteres slik at utviklingen kan forstås og etterprøves over tid.


## 17. Prinsipper for endringer

Los skal utvikles gradvis og på grunnlag av dokumenterte behov.

Innspill fra brukerne og erfaringer fra praktisk bruk av Los er sentrale kilder til endringsbehov. Nye versjoner og større endringer skal bygge på behov som er meldt inn, dokumentert eller på annen måte synliggjort gjennom bruk.

Nye begreper, nye nivåer eller større strukturelle endringer skal ha en tydelig begrunnelse og vurderes opp mot eksisterende struktur.

Et klassifiseringsproblem innebærer likevel ikke nødvendigvis at vokabularet må endres.

Før strukturen endres, skal det vurderes om behovet heller kan løses gjennom:


- klassifisering med flere Los-begreper
- alternative termer
- inklusjons- eller eksklusjonsmerknader
- SKOS Collections
- søk
- supplerende metadata
- kobling til et annet vokabular eller en annen klassifikasjon

Behov som går igjen på tvers av flere virksomheter eller innen en sektor, skal vurderes som mulige felles behov. Det skal da vurderes om behovet bør løses i Los eller gjennom en annen felles løsning.

Stabilitet og forutsigbarhet skal veie tungt ved vurdering av endringer.


## 18. Forvaltning av prinsippene

Design- og modelleringsprinsippene skal støtte redaksjonelle beslutninger og bidra til konsistent utvikling av Los.

De erstatter ikke faglig skjønn.

Prinsippene skal kunne videreutvikles når innspill fra brukerne og erfaringer fra praktisk bruk gir grunnlag for det. Endringer i prinsippene skal dokumenteres og begrunnes.

Den viktigste testen på både prinsippene og vokabularet er om Los oppleves som relevant, kan anvendes på en konsistent måte og faktisk tas i bruk.


## Redaksjonell arbeidsprosess

Arbeidsprosessen er skilt fra de varige design- og modelleringsprinsippene. Prosessen kan derfor videreutvikles uten at selve prinsippene må endres.


### Anbefalt arbeidsrekkefølge


1. Avklar behovet og hvilket klassifiseringsproblem som skal løses.
2. Vurder om behovet kan løses innenfor eksisterende struktur eller gjennom andre mekanismer.
3. Vurder om behovet er virksomhetsspesifikt eller felles for flere virksomheter eller en sektor.
4. Vurder behov for kobling eller mapping til andre vokabularer og klassifikasjoner.
5. Avklar arkitektur og plassering i hierarkiet i Los.
6. Kontroller at alle begreper unntatt toppbegrepene har ett og bare ett direkte overordnet begrep.
7. Vurder begrepsnavn og faglig forankring.
8. Legg til alternative termer der dette gir verdi.
9. Utarbeid inklusjonsmerknader der de bidrar til avgrensning eller klassifisering.
10. Utarbeid eksklusjonsmerknader ved reelle semantiske grenseflater.
11. Gjennomfør språklig kvalitetssikring på bokmål og nynorsk.
12. Etabler eller oppdater SKOS Collections.
13. Gjennomfør teknisk validering.
14. Dokumenter vesentlige endringer og begrunnelser.
15. Publiser ny versjon eller Release Candidate.

Strukturen bør være tilstrekkelig avklart før dokumentasjonen perfeksjoneres.

Etter arkitekturfrys bør strukturendringer bare gjennomføres når det er identifisert en dokumentert feil eller et behov som ikke kan løses tilfredsstillende innenfor den etablerte modellen.


## Teknisk kvalitetssikring

Den tekniske valideringen bør som minimum kontrollere at:


- hvert aktivt begrep har en stabil URI
- hvert begrep har nødvendige foretrukne termer
- skos:prefLabel er entydige i henhold til modellreglene
- genererte skos:altLabel samsvarer én-til-én med alternative termer i Excel-masteren, og at komma i termen er bevart
- alle aktive begreper unntatt toppbegrepene har nøyaktig ett direkte skos:broader
- toppbegrepene ikke har skos:broader til andre Los-begreper
- hierarkiet ikke inneholder sirkulære relasjoner
- skos:broader og skos:narrower brukes konsistent
- partitive XKOS-relasjoner ikke brukes i hierarkiet i Los
- referanser til begreper og samlinger peker til eksisterende ressurser
- SKOS Collections ikke påvirker hierarkiet i Los
- eventuelle mappingrelasjoner peker til gyldige ressurser og bruker riktig relasjonstype
- begrepsstrukturen er konsistent før publisering

## Åpne saker som kan påvirke dokumentet

Sakene nedenfor beskriver forslag og avklaringer. De er ikke vedtatte endringer i dokumentet.

- [#415 – Utarbeide språklege retningslinjer og kvalitetssikre Los 4](https://github.com/Informasjonsforvaltning/los/issues/415)
- [#479 – Avklare bruk av tema og begrep i dokumentasjonen for Los 4](https://github.com/Informasjonsforvaltning/los/issues/479)
- [#474 – Etablere Digdir-forvaltet mapping mellom Los 4 og EUs Data Theme](https://github.com/Informasjonsforvaltning/los/issues/474)
