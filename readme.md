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
- Tjänsten är utvecklad i Python som använder Flask för att exponera två endpoints och svara på anrop. De endpoints som exponeras är:
  - / (URL utan parametrar. Returnerar information som förklarar vilka parametrar som ska användas)
  - /granskningsinfo (tar emot parametrar, anropar granskningsmodulerna samt returnerar en dashboard i html-format som svar på anropet)
- Det finns en granskningsfil per dokument, vilken efter att ha konstruerat URL till dokumentet läser in TKB eller AB från Bitbucket-repo
- Granskningsfilerna innehåller allt som är unikt för granskning av respektive dokument
  - ATT GÖRA: säkerställ att det inte finns några dokumentspecifika funktioner eller variabler utanför granskningsfilerna
- Dokumenten läses in ett i taget i en instans av typen DOCX Document-klass
- Granskningsflödet exekveras i sekvens per dokument genom anrop från app.py till granskningsfilerna 
- Gemensamma granskningsfunktioenr finns i DOCX_display_document_contents.py 
- Krav som är specifika för ett visst dokument är implementerade genom granskningsfunktioner i respektive dokuments granskningsfil (granskning_*.py)


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
- Samma struktur som I-granskningstjänsten, vilket underlättar förvaltning och utveckling av de bägge tjänsterna
- Hela domänstrukturen ska laddas ner till ett virtuellt filsystem, varifrån det används för granskningskontroller
- Om/när dokumenten byter format från Word till annat format så ska granskningsfunktioner anpassas så att de kan hantera bägge formaten, vilket kan vara aktuellt under en övergångsperiod


### Python-filer som används i förbättrad struktur:
```
- app.py
  - Exponerar REST-endpoint: ('/granskningsinfo')
  - Läser in GET-parametrar från URL-strängen
  - AB-dokumentet: Anropar funktion i granskning_AB.py för att förbereda och genomföra granskning av AB-dokumentet
  - TKB: Anropar funktion i granskning_TKB.py för att förbereda och genomföra granskning av TKB
  - Anropar html_dashboard.get_page_html() för att få en ifylld dashboard i htmlformat

- document_management.py
  - Funktioner för att beräkna URL till angivet dokument
    
- DOCX_display_document_contents.py
  - Funktioner som används vid granskning av docx-dokument

- globals.py
  - Globala variabler och konstanter samt en funktion för att initiera dem

- granskning_AB.py
  - Funktion som förbereder granskning av AB-dokumentet
  - Funktioner som genomför granskning av AB-dokumentet
    - För varje granskningspunkt
      - Presenterar granskningskrav och ev. granskningsstöd
      - Anropar funktion som genomför granskning (eller listning av granskningsstöd)
        - Beroende på granskningspunkt så är det olika funktioner som anropas 
      - Presenterar resultat av granskningen

- granskning_TKB.py
  - Funktion som förbereder granskning av TKB
  - Funktioner som genomför granskning av TKB
    - För varje granskningspunkt
      - Presenterar granskningskrav och ev. granskningsstöd
      - Anropar funktion som genomför granskning (eller listning av granskningsstöd)
        - Beroende på granskningspunkt så är det olika funktioner som anropas 
      - Presenterar resultat av granskningen

- html_dashboard.py
  - Funktioner för att bygga den dashboard i html-format som lämnas ut som svar på GET-anropet
  - Returnerad html innehåller:
    - All layout, inklusive css
    - Navigeringslänkar i lista till vänster om huvudinnehållet
    - Två boxar med summeringsinformation
    - Detaljboxar per granskat dokument

- repo.py
  - Innehåller funktionen REPO_get_domain_docs_link
    
- uilities.py
  - Några funktioner som används både vid granskning av Infospec och TKB

UNDER UTVECKLING, ANVÄNDS EJ 
- experiment.py
  - Har använts för att utveckla kod som laddar ner samtliga domänfiler till virtuellt filsystem och som använder filerna därifrån
  - Lösningen är inte färdig än (2021-11-07), och kanske inte hinner bli klar innan överlämning. I så fall får förvaltningen vidareutveckla detta
  
```

## Driftsättning, konfiguration, beroenden:
- Push till GitHub-repo
  - Från lokalt repo
- Deploy till Heroku-app
  - Deploy sker med Herokus CLI (git push heroku master)
  - runtime.txt används av Heroku för att se till att önskat Python-version är installerat i appen
  - requirements.txt används av Heroku för att se till att angivna versioner av dependencies är installerade i appen

## Information riktad till utvecklare:
Dokumenten som granskas laddas ner till virtuella dokumentinstanser (DOCX Document), vilka i sin tur är de som granskas.

### Lokal utveckling och test
- PyCharm har använts som IDE vid utveckling av tjänsten
- Lokala tester har gjorts genom att starta app.py från PyCharm och sedan anropa tjänsten via webbläsare med adress http://127.0.0.1:4001/granskningsinfo?domain=[domännamn]&tag=[tagnummer]
- Dependencies (installed packages)
  - 2do: lista packages som används...

### Komplettera med ytterligare granskningspukt:
Både granskningsflöde och dokumentspecifika funktioner finns i 
respektive dokuments granskningsfil (granskning_*.py). 
Funktioner som används vid granskning av flera dokument finns i gemensam pyhon-fil. 
Exempel på det är DOCX_display_document_contents.py

- Lägg till kod i granskning_*.py (granskningsfilen för berört dokument)
  - Presentation av granskningskrav
  - Anrop till funktion som genomför granskningen
    - Använd befintlig funktion eller lägg till en ny funktion i lämplig python-fil
  - Presentation av granskningens resultat
- Ifall granskningskrav som är gemensamt för flera dokument ska läggas till:
  - Skapa funktionen i lämplig gemensam python-fil
  - Lägg till anrop till funktionen i de granskningsfiler som ska använda samma granskningskontroll
- Uppdatera sammanfattningsruta i html_dashboard.py om resultat av den nya granskningspunkten ska visas i summeringsruta

### Listning av dokumentinnehåll under en viss rubrik:
- Introduktion
  - Funktionen DOCX_display_paragraph_text_and_tables används för att visa innehåll i sökt paragraf
- Lösning
  - Parametrar avgör vilket paragrafinnehåll som ska visas
  - Funktionen returnerar True eller False som anger om sökt paragraf hittades
- Användning
  - Funktionen används av ett flertal TKB- och AB-granskningspunkter

### Tabellnummer för tabell under en viss rubrik
- Introduktion
  - Instanser av Document innehåller attributet tables som håller reda på alla tabeller som finns i dokumentet
  - document.tables[tabellnummer] refererar till en viss tabell i dokumentet, men utan koppling till var i dokumentet den finns
- Lösning
  - Dictionaryt paragraph_title_tableno_dict sparar tabellnummer med rubrik som nyckel
  - Funktionen DOCX_get_tableno_for_paragraph_title används för att få det tabellnummer som hör till en viss rubrik
  - I vissa fall innehåller dokumentet flera likadana rubriker. I de fallen läggs tabellnummer till i nyckeln för att 
  skapa unika nycklar så att alla förekomster lagras i dictionaryt
- Användning
  - Dictionaryt används av implementation av vissa granskningskrav i TKB och AB-dokumentet

### Kontroll av förekomst av tomma tabellceller
- Introduktion
  - Funktionen DOCX_empty_table_cells_exists används för att kontrollera om angiven tabell innehåller tomma celler
  - Det är ganska många kodrader, vilket gör funktionen onödigt komplex att förvalta och vidareutveckla
  - Förenkling av koden ska ske innan överlämning till förvaltning
- Lösning
- Användning

### DOCX-biblioteket
- Biblioteket tillhandahåller funktioner som döljer strukturen i Wordfiler i docx-format
- Worddokument läses in i en instans av DOCX_bibliotekts klass Document(), vilket sker i document_management.py
- Wordfiler består av en struktur av ett antal XML-filer. I de fall där DOCX-biblioteket inte tillhandahåller önskad funktion så har Pythonkoden läst in berörd XML-fil och sökt i den

### Optimering av exekveringstid
Det visade sig att funktionen som kollar om det finns tomma tabellceller tog oväntat lång tid för kontroll av cellinnehållet. 
Detta märktes tydligt för en domän som hade en ovanligt stor revisionshistorik (> 90 tabellrader).
Funktionen skrevs om så att den läser in varje tabellrad i en Tuple, som sedan kontrolleras element för element. 
Tidsåtgången för den berörda domänen sänktes från 17 till 3 sekunder. 
Tuple känner inte igen hyperlänkar i tabeller, utan betraktar hyperlänkar som tomt innehåll. 
En extra kontroll görs därför av tomma tabellcellers underliggande XML-innehåll.

### Ett Worddokuments beståndsdelar
Worddokument består av ett antal filer (främst XML) som tillsammans beskriver dokumentets innehåll och dess formatering.
I fall där DOCX-biblioteket saknar stöd för att tillhandahålla önskad information från dokumentet så söker Pythonkoden i en XML-fils innehåll
Läs mer om docx-formatet på: http://officeopenxml.com/anatomyofOOXML.php

Nedan listas ett exempel på vilka filer som ingår i ett dokument (TKB_clinicalprocess_healthcond_actoutcome.docx)
- [Content_Types].xml
- _rels/.rels 
- word/_rels/document.xml.rels
- word/document.xml
- word/footnotes.xml
- word/endnotes.xml
- word/header1.xml
- word/footer1.xml
- word/header2.xml
- word/footer2.xml
- word/_rels/header1.xml.rels
- word/_rels/header2.xml.rels
- word/media/image1.png
- word/media/image2.png
- word/media/image3.png
- word/media/image4.png
- word/media/image5.jpeg
- word/media/image7.png
- word/media/image8.png
- word/media/image9.png
- word/media/image10.png
- word/theme/theme1.xml
- word/media/image6.png
- word/settings.xml
- word/_rels/settings.xml.rels
- customXml/item1.xml
- customXml/itemProps1.xml
- word/numbering.xml
- word/styles.xml
- word/webSettings.xml
- word/fontTable.xml
- docProps/core.xml
- docProps/app.xml
- docProps/custom.xml
- customXml/_rels/item1.xml.rels