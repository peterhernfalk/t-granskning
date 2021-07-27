from docx import Document
import glob
import globals
import os
from utilities import *
#from utilities import write_output, write_output_without_newline, __extract_urls_from_table, verify_url_exists

from docx.document import Document as _Document
from docx.table import _Cell, Table, _Row
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.text.paragraph import Paragraph


NOT_FOUND = "Not found"
STYLE_FAMILY_HEADING = "Heading"
STYLE_FAMILY_RUBRIK = "Rubrik"
STYLE_FAMILY_SUBTLE_EMPHASIS = "Subtle Emphasis"
local_test = False


def __style_family(document_search_phrase):
    if "IS_*" in document_search_phrase:
        return STYLE_FAMILY_RUBRIK
    else:
        return STYLE_FAMILY_HEADING


def DOCX_prepare_inspection(document_search_phrase):
    """
    Anropar metoder för att förbereda för granskning av ett Worddokument
    """
    __set_document_name(document_search_phrase)
    __document_structure_2_dict(__style_family(document_search_phrase))

def DOCX_inspect_revision_history():
    """
    Kollar att dokumentets tabell med revisionshistorik har en rad för aktuell tag.
    """
    table = document.tables[1]
    # 2do: Display version number from page 1 in the document

    if table.cell(0,0).text == "Revisionshistorik mall":
        table = document.tables[2]

    for i, row in enumerate(table.rows):
        text = tuple(cell.text for cell in row.cells)

    if str(table.cell(i, 0).text) != globals.tag:
        write_output("OBS! Revisionshistoriken behöver uppdateras. (hittade: "+str(table.cell(i, 0).text)+" men förväntade: "+globals.tag+")")
        write_detail_box_content("<b>Resultat:</b> Revisionshistoriken behöver uppdateras. (hittade: "+str(table.cell(i, 0).text)+" men förväntade: "+globals.tag+")")
        if globals.docx_document == globals.IS:
            globals.IS_antal_brister_revisionshistorik = 1
        elif globals.docx_document == globals.TKB:
            globals.TKB_antal_brister_revisionshistorik = 1
    else:
        write_output("Revisionshistoriken är uppdaterad för denna version av domänen")
        write_detail_box_content("<b>Resultat:</b> Revisionshistoriken är uppdaterad för denna version av domänen")
    write_output("Revisionshistorikens sista rad: " + str(text))
    write_detail_box_content("Revisionshistorikens sista rad: " + str(text))

def DOCX_display_paragraph_text_and_tables(searched_paragraph_title, display_paragraph_title, display_initial_newline, display_keylevel_text, display_tables):
    """
    Skriver ut titlar och innehåll i paragrafer och tabeller i enlighet med angivna parametrar.

    Utskrift sker via metoden: write_output
    """
    searched_paragraph_level = DOCX_document_structure_get_levelvalue(searched_paragraph_title)
    searched_paragraph_found = False

    if display_paragraph_title == True and display_tables == False:
        if display_initial_newline == True:
            write_output("<br>")
            write_detail_box_html("<br>")
        __display_paragraph_text_by_paragraph_level(searched_paragraph_level, display_keylevel_text)
    else:
        for block in __iter_block_items(document,searched_paragraph_level):
            if isinstance(block, Paragraph):
                this_paragraph_title = block.text.strip().lower()
                if this_paragraph_title == searched_paragraph_title.strip().lower():
                    searched_paragraph_found = True
                    if display_paragraph_title == True:
                        #write_output("\n")
                        __display_paragraph_text_by_paragraph_level(searched_paragraph_level, display_keylevel_text)

            elif isinstance(block, Table):
                if searched_paragraph_found == True:
                    if display_tables == True:
                        if display_paragraph_title == False:
                            write_output("<br>")
                            write_detail_box_html("<br>")
                        __table_print(block)
                    searched_paragraph_found = False     # Bug: supports only one table per paragraph


def DOCX_inspect_reference_links(table_num):
    """
    Kollar om länkarna i dokumentets referenstabell fungerar eller ej.
    """
    links = extract_urls_from_table(document, table_num)
    if len(links) == 0:
        write_output("Det finns inga länkar i referenstabellen. Obs att det ändå kan förekomma länkar med annat format (text istället för hyperlänk).")
        write_detail_box_content("Det finns inga länkar i referenstabellen. Obs att det ändå kan förekomma länkar med annat format (text istället för hyperlänk).")
    for link in links:
        status_code = verify_url_exists(link)
        if status_code == 400:
            write_output("<b>Länken är felaktig eller kan inte tolkas!</b> (statuskod: " + str(status_code) + ") för: " + link)
            write_detail_box_content("<b>Länken är felaktig eller kan inte tolkas!</b> (statuskod: " + str(status_code) + ") för: " + link)
            if globals.docx_document == globals.IS:
                globals.IS_antal_brister_referenslänkar += 1
            elif globals.docx_document == globals.TKB:
                globals.TKB_antal_brister_referenslänkar += 1
        elif status_code < 404:
            write_output("<b>OK</b> (statuskod: " + str(status_code) + ") för: <a href='" + link + "' target = '_blank'>" + link + "</a>")
            write_detail_box_content("<b>OK</b> (statuskod: " + str(status_code) + ") för: <a href='" + link + "' target = '_blank'>" + link + "</a>")
        else:
            if globals.docx_document == globals.IS:
                globals.IS_antal_brister_referenslänkar += 1
            elif globals.docx_document == globals.TKB:
                globals.TKB_antal_brister_referenslänkar += 1
            write_output("Sidan saknas! (statuskod: " + str(status_code) + ") för: " + link)
            write_detail_box_content("<b>Sidan saknas!</b> (statuskod: " + str(status_code) + ") för: " + link)


def DOCX_display_paragragh_title(searched_title_name):
    """
    Söker efter angiven paragraf i lagrad dokumentstruktur. Skriver ut paragrafens titel.

    Returnerar: True om sökt paragraf hittades och False om paragrafen inte hittades
    """
    result = True
    searched_paragraph_level = DOCX_document_structure_get_exact_levelvalue(searched_title_name)
    if searched_paragraph_level != "":
        #write_output("OK. (" + searched_title_name + ") avsnitt " + searched_paragraph_level + " i TKB")
        write_output("OK. Dokument-rubrik (" + searched_paragraph_level + "):  \t" + searched_title_name)
    else:
        write_output("FEL! " + searched_title_name + " verkar inte vara beskrivet i dokumentet!")
        result = False
    return result


def __set_document_name(search_phrase):
    """
    Sätter den globala variabeln 'document' till namnet på angivet dokument
    """
    global document
    global document_name

    """os.chdir(globals.document_path)
    for word_document in glob.glob(search_phrase):
        document_name = r""+globals.document_path+"/"+word_document
    document = Document(document_name)"""
    if "IS_*" in search_phrase:
        document = globals.docx_IS_document
    elif "TKB_*" in search_phrase:
        document = globals.docx_TKB_document


def __document_structure_2_dict(style_family):
    """
    Lagrar dokumentet struktur i ett globalt dictionary.

    Lagrar även index till dokumentets paragrafer i ett globalt dictionary.
    """
    if style_family == STYLE_FAMILY_HEADING:
        level_from_style_name = {f'Heading {i}': i for i in range(10)}
    elif style_family == STYLE_FAMILY_RUBRIK:
        level_from_style_name = {f'Rubrik {i} Nr': i for i in range(10)}
    elif style_family == STYLE_FAMILY_SUBTLE_EMPHASIS:
        #2do: try other alternatives to make this style work as title
        level_from_style_name = {i for i in range(2)}
    current_levels = [0] * 10
    global document_structure_dict  #key = kapitelnamn, value = kapitelnummer
    document_structure_dict = {}
    global document_paragraph_index_dict
    document_paragraph_index_dict = {}

    index = 1
    for paragraph in document.paragraphs:
        if paragraph.style.name in level_from_style_name:
            level = level_from_style_name[paragraph.style.name]
            current_levels[level] += 1
            for level in range(level + 1, 10):
                current_levels[level] = 0
            document_structure_dict[paragraph.text.strip().lower()] = __format_levels(current_levels)
        document_paragraph_index_dict[__format_levels(current_levels) + " " + paragraph.text] = index
        index +=1

    if local_test == True:
        for value in document_structure_dict:
            print("value in document_structure_dict:",value)
        for i in document_paragraph_index_dict:
            print("i in document_paragraph_index_dict:",i)


def DOCX_document_structure_get_levelvalue(searched_key):
    """
    Söker efter angivet rubrikvärde i dictionaryt med dokumentstruktur.

    Returnerar: Om rubrikvärdet hittades så returneras dess nyckel (rubrikens titel), annars returneras NOT_FOUND
    """
    for key, value in document_structure_dict.items():
        if searched_key.strip().lower() == key:     #in key
            return value
    return NOT_FOUND

def DOCX_document_structure_get_exact_levelvalue(searched_key):
    """
    Söker efter angivet rubriktitel (nyckel) i dictionaryt med dokumentstruktur.

    Returnerar: Om rubriktiteln hittades så returneras dess rubrikvärde, annars returneras NOT_FOUND
    """
    for key, value in document_structure_dict.items():
        if searched_key.strip().lower() == key:
            return value
    return NOT_FOUND

def __display_paragraph_text_by_paragraph_level(searched_paragraph_level,display_keylevel_text):
    """
    Hämtar paragraftext från dokumentstruktur-dictionaryt med rubriknivå som nyckel, och visar den funna texten
    """
    previous_key = ""
    for key, value in document_paragraph_index_dict.items():
        if key[0:len(searched_paragraph_level)] == searched_paragraph_level:
            key_level_length = key.find(" ")
            if len(key.strip()) > key_level_length:
                this_key_level = key.strip()[0:key_level_length]
                if this_key_level == previous_key:
                    if display_keylevel_text == True:
                        write_output(globals.HTML_3_SPACES + key.strip()[key_level_length+1:])
                        write_detail_box_content(globals.HTML_3_SPACES + key.strip()[key_level_length+1:])
                else:
                    key = key.replace("\n"," ")
                    write_output(globals.HTML_3_SPACES + key)
                    write_detail_box_content(globals.HTML_3_SPACES + key)
                previous_key = key.strip()[0:key_level_length]

def DOCX_display_paragraph_text_by_paragraph_level(searched_paragraph_level,display_keylevel_text):
    """
    Hämtar paragraftext från dokumentstruktur-dictionaryt med rubriknivå som nyckel, och visar den funna texten.

    Sökning sker efter tjänstekontraktsversion, angiven i den funna paragraftexten.
    """
    #key_level = ""
    key_text = ""
    previous_key = ""
    tk_version = ""
    for key, value in document_paragraph_index_dict.items():
        this_key_level_length = key.find(" ")
        searched_level_sublevels = searched_paragraph_level+"."
        if searched_level_sublevels in key[0:this_key_level_length]:
            key_level_length = key.find(" ")
            if len(key.strip()) > key_level_length:
                this_key_level = key.strip()[0:key_level_length]
                if this_key_level == previous_key:
                    if key_text == "version":
                        tk_version = key.strip()[key_level_length + 1:]
                else:
                    key_level = key.strip()[0:key_level_length]
                    key_text = key.lower()[key_level_length:].strip()
                previous_key = key.strip()[0:key_level_length]

    return tk_version


def __format_levels(current_level):
    """
    Formaterar angiven rubriknivå. 2do: beskriv detta bättre...

    Returnerar: formaterad rubriknivå
    """
    levels = [str(level) for level in current_level if level != 0]
    return '.'.join(levels)

def DOCX_document_structure_get_key(searched_value):
    for key, value in document_structure_dict.items():
        if searched_value == value:
            return key
    return NOT_FOUND

##### code test #####
def remove_hyperlink_tags(xml):
    import re
    #text = xml.decode('utf-8')
    text = xml
    text = text.replace("</w:hyperlink>","")
    text = re.sub('<w:hyperlink[^>]*>', "", text)
    #return text.encode('utf-8')
    return text
#####################

def __table_print(table):
    #table = block
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                output_text = paragraph.text
                #print("paragraph",paragraph.style)
                #output_text = remove_hyperlink_tags(paragraph.text)
                write_output_without_newline(globals.HTML_3_SPACES + output_text)
                write_detail_box_html(globals.HTML_3_SPACES + output_text)
        #write_output_without_newline("\t" + output_text)
        write_output("")
        write_detail_box_html("<br>")

def __iter_block_items(parent,searched_paragraph_level):
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    """elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    elif isinstance(parent, _Row):
        parent_elm = parent._tr
    else:
        raise ValueError("something's not right")"""

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)



if local_test == True:
    TITLE = True
    NO_TITLE = False
    INITIAL_NEWLINE = True
    NO_INITIAL_NEWLINE = False
    TEXT = True
    NO_TEXT = False
    TABLES = True
    NO_TABLES = False

    #globals.document_path = "/Users/peterhernfalk/Desktop/Aktuellt/_T-granskningar/git-Repo/riv.clinicalprocess.healthcond.certificate/docs"
    #globals.document_path = "/Users/peterhernfalk/Desktop/Aktuellt/_T-granskningar/git-Repo/riv.clinicalprocess.healthcond.actoutcome/docs"
    #globals.document_path = "/Users/peterhernfalk/Desktop/Aktuellt/_T-granskningar/git-Repo/riv.clinicalprocess.activity.actions/docs"

    #print("\n*** TKB ***")
    #DOCX_prepare_inspection("TKB_*.doc*")
    #DOCX_inspect_revision_history()
    #DOCX_display_paragraph_text_and_tables("versionsinformation",TITLE,INITIAL_NEWLINE,TEXT,NO_TABLES)
    #DOCX_display_paragraph_text_and_tables("adressering",TITLE,INITIAL_NEWLINE,TEXT,NO_TABLES)
    #DOCX_display_paragraph_text_and_tables("aggregering",TITLE,INITIAL_NEWLINE,TEXT,NO_TABLES)
    #DOCX_display_paragraph_text_and_tables("sla krav",TITLE,INITIAL_NEWLINE,TEXT,TABLES)
    #DOCX_display_paragraph_text_and_tables("felhantering",TITLE,INITIAL_NEWLINE,TEXT,NO_TABLES)


    #print("\n*** IS ***")
    #DOCX_prepare_inspection("IS_*.doc*")
    #DOCX_display_paragraph_text_and_tables("klasser och attribut",TITLE,NO_INITIAL_NEWLINE,NO_TEXT,NO_TABLES)
    #DOCX_display_paragraph_text_and_tables("klasser och attribut",TITLE,INITIAL_NEWLINE,TEXT,NO_TABLES)
    #DOCX_display_paragraph_text_and_tables("Referenser",TITLE,NO_INITIAL_NEWLINE,TEXT,TABLES)
