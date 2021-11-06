# T-granskning av tjänstedomäner

## Beskrivning:
Tjänsten är utvecklad för att underlätta teknikgranskning av tjänstedomäner.
Underlag för implementationen är checklista för T-granskning samt krav från T-granskare, där fokus har varit att i första hand automatisera 
sådana krav som ger stor nytta och som kan implementeras med en rimlig arbetsinsats.
Utmaningar i implementationsarbetet är att det dels förekokmmmer olika mallversioner av dokumenten och dels att det framförallt i TKB-dokument
kan ha skett förändringar som exempelvis att nya kapitel har lagts till eller att det har tillkommit eller tagits bort tabellkolumner.

Tjänsten anropas från en webbläsare med ett GET-anrop med URL-parametrar från webbläsare till tjänstens endpoint
- Anrop:
  - Webbläsare gör ett anrop till tjänstens endpoint (/granskningsinfo)
  - Tjänstens endpoint exekverar granskningsflödet
    - Per dokument i granskningsflödet: 
      - Nerladdning av dokumentet från domänens repo 
      - Ganskningsfunktioner exekveras
      - Krav och granskningsresultat sparas i sessionen
- Svar:
  - Efter avslutat granskningsflöde
    - Uppbyggnad av struktur i html-dashboarden, inklusive länkar till detaljavsnitten
    - Innehåll i html-dashboarden fylls med hjälp av information som sparats i sessionen
      - Sammanställning och summering i sammanfattningsrutor
      - Detaljerad information i detaljrutor i form av krav, granskningsstöd och granskningsresultat
    - Uppbyggd html skickas från tjänstens endpoint till webbläsaren som svar på anropet

### Implementationen i korthet

### Inför överlämning till förvaltning
Tjänsten förbereds för att kunna lämnas över till förvaltning och vidareutveckling inför julledigheten 2021.
Det kommer att finnas en restlista med utveckling som inte hinner bli klart. Detta kommer att vara dokumenterat i denna readme-fil.

### Restlista vid överlämning till förvaltning
- experiment.py innehåller påbörjad kod för att ladda ner tjänstedomänens samtliga filer från Bitbucket-repo till ett virtuellt filsystem.
- Funktionalitet som gärna skulle vara med i tjänsten, men som av tidsbrist inte kommer med. Workaround har påbörjats för att kunna erbjuda detta på annat vis
  - Anrop av verifyRivtaDomain.py är inte med i tjänsten
  - Anrop av createRivtaArchive.py är inte med i tjänsten
  - Anrop till Apache CXF för Kontroll att tjänstekontraktens XML validerar är inte med i tjänsten
  - Anrop till XML-compatibility.jar är inte med i tjänsten

## Målbild för kodstruktur:
Samma struktur som I-granskningstjänsten, vilket underlättar förvaltning och utveckling av de bägge tjänsterna

### Python-filer som används i förbättrad struktur:
```
- app.py
  - Exponerar REST-endpoint: ('/granskningsinfo')
  - Läser in GET-parametrar från URL-strängen
 
 Beskriv mer...
```

## Driftsättning, konfiguration, beroenden:

## Information riktad till utvecklare:

### Lokal utveckling och test

### Komplettera med ytterligare granskningspukt:

### Listning av dokumentinnehåll under en viss rubrik:

### Tabellnummer för tabell under en viss rubrik

### Kontroll av förekomst av tomma tabellceller

### DOCX-biblioteket