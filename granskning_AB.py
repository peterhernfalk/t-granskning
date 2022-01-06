
import datetime
import DOCX_display_document_contents
from DOCX_display_document_contents import *
from docx.api import Document  # noqa
import document_mangagement
from utilities import *

AB_antal_brister_referenslänkar = 0
AB_antal_brister_revisionshistorik = 0
AB_antal_brister_tomma_referenstabellceller = 0
AB_antal_brister_tomma_revisionshistoriktabellceller = 0
AB_antal_brister_tomma_tabellceller = 0
AB_detail_box_contents = ""
AB_document_exists = False
AB_exists = False

TITLE = True
NO_TITLE = False
INITIAL_NEWLINE = True
NO_INITIAL_NEWLINE = False
TEXT = True
NO_TEXT = False
TABLES = True
NO_TABLES = False


def prepare_AB_inspection(domain, tag, alt_document_name):
    """
    Beräknar url till AB-dokumentet för angiven domain och tag.

    Laddar ner dokumentet till en virtuell fil som läses in i ett docx-Document.

    Anropar därefter metoden "INFO_inspect_document" som genomför granskning av dokumentet.
    """
    """
    2do: Förenkla och snygga till koden
    """
    print("AB-init påbörjas",datetime.datetime.now().replace(microsecond=0))

    global AB_page_link

    global AB_antal_brister_referenslänkar
    global AB_antal_brister_revisionshistorik
    global AB_antal_brister_tomma_referenstabellceller
    global AB_antal_brister_tomma_revisionshistoriktabellceller
    global AB_antal_brister_tomma_tabellceller
    global AB_detail_box_contents
    global AB_document_exists
    global AB_exists
    AB_antal_brister_referenslänkar = 0
    AB_antal_brister_revisionshistorik = 0
    AB_antal_brister_tomma_referenstabellceller = 0
    AB_antal_brister_tomma_revisionshistoriktabellceller = 0
    AB_antal_brister_tomma_tabellceller = 0
    AB_detail_box_contents = ""
    AB_document_exists = False
    AB_exists = False

    AB_page_link = document_mangagement.DOC_get_document_page_link(domain, tag, globals.AB)
    downloaded_AB_page = document_mangagement.DOC_get_downloaded_document(AB_page_link)

    AB_head_hash = document_mangagement.DOC_get_head_hash(downloaded_AB_page)
    AB_document_link = document_mangagement.DOC_get_document_link(domain, tag, globals.AB, AB_head_hash, alt_document_name)
    downloaded_AB_document = document_mangagement.DOC_get_downloaded_document(AB_document_link)
    if downloaded_AB_document.status_code == 404:
        AB_exists = False
    else:
        globals.docx_AB_document = document_mangagement.DOC_get_docx_document(downloaded_AB_document)
        AB_document_exists = True
        AB_exists = True

        DOCX_prepare_inspection("AB_*.doc*")

def perform_AB_inspection(domain, tag, alt_document_name):
    prepare_AB_inspection(domain, tag, alt_document_name)
    print("AB-granskning påbörjas",datetime.datetime.now().replace(microsecond=0))

    global AB_antal_brister_referenslänkar
    global AB_antal_brister_revisionshistorik
    global AB_antal_brister_tomma_referenstabellceller
    global AB_antal_brister_tomma_revisionshistoriktabellceller
    global AB_antal_brister_tomma_tabellceller
    global AB_detail_box_contents
    global AB_document_exists
    global AB_exists

    if AB_exists == False:
        return

    write_detail_box_content("<br>")
    write_detail_box_content("<b>Krav:</b> om dokumentegenskaper finns ska version och ändringsdatum stämma överens med granskad version")

    write_detail_box_content("<br>")
    write_detail_box_content("<b>Krav:</b> revisionshistoriken ska vara uppdaterad för samma version som domänen")
    write_detail_box_content("<b>Granskningsstöd:</b> om revisionshistoriken inte är uppdaterad, kontakta beställaren eller skriv en granskningskommentar")
    used_table_no = DOCX_display_document_contents.DOCX_get_tableno_for_paragraph_title("revisionshistorik")
    if used_table_no > 0:
        AB_antal_brister_revisionshistorik = DOCX_inspect_revision_history(globals.AB, used_table_no)
    else:
        AB_antal_brister_revisionshistorik = DOCX_inspect_revision_history(globals.AB,globals.TABLE_NUM_REVISION)

    write_detail_box_content("<br>")
    write_detail_box_content("<b>Krav:</b> revisionshistorikens alla tabellceller ska ha innehåll")
    if used_table_no > 0:
        result, AB_antal_brister_tomma_revisionshistoriktabellceller = DOCX_display_document_contents.DOCX_empty_table_cells_exists(used_table_no, True, globals.DISPLAY_TYPE_TABLE)
    else:
        result, AB_antal_brister_tomma_revisionshistoriktabellceller = DOCX_display_document_contents.DOCX_empty_table_cells_exists(globals.TABLE_NUM_REVISION, True, globals.DISPLAY_TYPE_TABLE)

    write_detail_box_content("<br>")
    write_detail_box_content("<b>Krav:</b> länkarna i referenstabellen ska fungera")
    used_table_no = DOCX_display_document_contents.DOCX_get_tableno_for_paragraph_title("referenser")
    links_excist = False
    if used_table_no > 0:
        links_excist, AB_antal_brister_referenslänkar = DOCX_inspect_reference_links(used_table_no)
    else:
        links_excist, AB_antal_brister_referenslänkar = DOCX_inspect_reference_links(globals.TABLE_NUM_REF)
    if AB_antal_brister_referenslänkar > 0:
        write_detail_box_content("&#10060; <b>Resultat:</b> en eller flera länkar är felaktiga, eller kan inte tolkas korrekt av granskningsfunktionen.")
        write_detail_box_content("<b>Granskningsstöd:</b> gör manuell kontroll i dokumentet av de länkar som rapporteras som felaktiga")
    else:
        if links_excist == True:
            write_detail_box_content("<b>Resultat:</b> alla kontrollerade länkar fungerar")
        else:
            write_detail_box_content("&#10060; <b>Resultat:</b> inga länkar har kontrollerats")

    write_detail_box_content("<br>")
    write_detail_box_content("<b>Krav:</b> referenstabellens alla tabellceller ska ha innehåll")
    if used_table_no > 0:
        result, AB_antal_brister_tomma_referenstabellceller = DOCX_display_document_contents.DOCX_empty_table_cells_exists(used_table_no, True, globals.DISPLAY_TYPE_TEXT)
    else:
        result, AB_antal_brister_tomma_referenstabellceller = DOCX_display_document_contents.DOCX_empty_table_cells_exists(globals.TABLE_NUM_REF, True, globals.DISPLAY_TYPE_TEXT)

    write_detail_box_content("<br>")
    write_detail_box_content("<b>Krav:</b> alla AB ska ha minst två alternativ och motivering till det valda alternativet. Kontrolleras manuellt")
    write_detail_box_content("<b>Krav:</b> om dokumentegenskaper finns ska version och ändringsdatum stämma överens med granskad version")

    write_detail_box_content("<br>")
    write_detail_box_content("<b>Krav:</b> dokumentet ska innehålla rimliga arkitekturbeslut")
    DOCX_display_paragraph_text_and_tables("arkitekturella beslut",TITLE,NO_INITIAL_NEWLINE,NO_TEXT,NO_TABLES)
    write_detail_box_content("<b>Resultat:</b> för närvarande sker kontrollen manuellt, med ovanstående listning som underlag")
    print("AB-granskning klar",datetime.datetime.now().replace(microsecond=0))
