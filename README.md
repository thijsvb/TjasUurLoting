# TjasUurLoting
Een loting voor wie er naar het TjasUur mag ivm het maximum aantal mensen op de ijsbaan.

### Wat en waarom?
Op het moment van schrijven is het 15 oktober 2020, wat betekent dat door coronamaatregelen het schaatsseizoen er dit jaar een stuk anders uitziet.
Er mag slechts een maximum aantal mensen op de baan van 30, daarom gaan we loten welke Tjassers wanneer mogen schaatsen. Om de loting transparant, eerlijk en zonder fouten te laten verlopen kan je hier de code waarmee de loting gedaan wordt inzien en controleren. In verband met privacy zal er natuurlijk geen data van echte Tjassers op GitHub geplaatst worden, er staan enkel bestanden met testdata hier.

**Issues en pull request om fouten te melden/verbeteren zijn welkom!**

### Procedure
De loting is niet compleet willekeurig, vandaar ook deze repository, er zijn twee uitzonderingen:

1. Leden die minder vaak geschaatst hebben dit seizoen hebben voorang.
2. Maar hierbij tellen 3 trainingen voor hardrijders als 2 trainingen voor recreanten.

De eerste uitzondering lijkt mij vrij logisch, we streven er naar iedereen even vaak te laten schaatsen. De tweede uitzondering is omdat hardrijders onder normale omstandigheden 3 trainingen per week hebben en recreanten 2. Omdat er natuurlijk betaald wordt voor een baankaart willen we deze verhouding in stand houden.

**Dit is niet de plek om deze procedure te bespreken, het gaat hier enkel om de implementatie.** Vragen of opmerkingen over deze procedure kunnen naar de voorzitter gemaild worden.

### Handleiding
Het programma `TjasUurLoting.py` voert de loting uit en heeft daarbij maar liefst 2 input bestanden en 2 output bestandsnamen nodig.
* Het eerste input bestand is de huidige telling in een `.json` bestand, hierin staat hoe vaak iedereen geschaatst heeft en wie hardrijder is. In plaats van namen worden email adressen gebruikt, die zijn namelijk altijd uniek. Testbestand: `telling_week_n.json`
* Het tweede input bestand is een `.csv` met mensen hun voorkeur voor welke dagen ze kunnen schaatsen. Hierin is een kolom voor voornaam, achternaam, email en vervolgens een kolom voor elke dag (maandag, donderdag, zondag). Er staat een `1` of `0` om de beschikbaarheid van de Tjasser aan te geven. Testbestand: `voorkeur_week_n.csv`
* Het eerste output bestand is de nieuwe telling. Testbestand: `telling_week_n+1.json`
* Het tweede tekstbestand is de uitslag van de loting. Testbestand: `selectie_week_n.csv`

Om het programma te testen met de testdata run:
```
./TjasUurLoting.py telling_week_n.json voorkeur.csv telling_week_n+1.json selectie_week_n.csv
```
