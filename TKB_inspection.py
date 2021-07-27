from docx import *
#from docx import Document, document
import glob
import globals
import os

#from DOCX_display_document_contents import DOCX_document_structure_get_exact_levelvalue
from DOCX_display_document_contents import *
from utilities import write_output

from docx.document import Document as _Document
from docx.table import _Cell, Table, _Row
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.text.paragraph import Paragraph


NOT_FOUND = "Not found"
local_test = False

def TKB_get_interaction_version(interaction_name):
    version_number = "0"
    #2do: extract version number from interaction paragraph
    searched_paragraph_level = DOCX_document_structure_get_exact_levelvalue(interaction_name)
    #__display_paragraph_text_by_paragraph_level(interaction_name,searched_paragraph_level)
    version_number = DOCX_display_paragraph_text_by_paragraph_level(searched_paragraph_level,interaction_name)

    return version_number


def TKB_display_paragragh_title(searched_title_name):
    result = True
    result_description = ""
    searched_paragraph_level = DOCX_document_structure_get_exact_levelvalue(searched_title_name)
    if searched_paragraph_level != "":
        #result_description = "OK. TKB (" + searched_paragraph_level + "):  \t" + searched_title_name
        result_description = "TKB (" + searched_paragraph_level + "):  \t" + searched_title_name
        #write_output("OK. TKB (" + searched_paragraph_level + "):  \t" + searched_title_name)
    else:
        result_description = "FEL! " + searched_title_name + " verkar inte vara beskrivet i TKB!"
        #write_output("FEL! " + searched_title_name + " verkar inte vara beskrivet i TKB!")
        result = False
    return result, result_description

def __display_paragraph_text_by_paragraph_level(searched_paragraph_level,display_keylevel_text):
    global document_paragraph_index_dict
    previous_key = ""
    for key, value in document_paragraph_index_dict.items():
        if key[0:len(searched_paragraph_level)] == searched_paragraph_level:
            key_level_length = key.find(" ")
            if len(key.strip()) > key_level_length:
                this_key_level = key.strip()[0:key_level_length]
                if this_key_level == previous_key:
                    if display_keylevel_text == True:
                        write_output("\t" + key.strip()[key_level_length+1:])
                else:
                    write_output(key)
                previous_key = key.strip()[0:key_level_length]


if local_test == True:
    globals.document_path = "/Users/peterhernfalk/Desktop/Aktuellt/_T-granskningar/git-Repo/riv.clinicalprocess.healthcond.certificate/docs"
    #globals.document_path = "/Users/peterhernfalk/Desktop/Aktuellt/_T-granskningar/git-Repo/riv.clinicalprocess.healthcond.actoutcome/docs"
    #TKB_inspect_document_contents()

    #__display_paragraph_text_and_tables("revisionshistorik")
    #__display_paragraph_text_and_tables("referenser")
    #__display_paragraph_text_and_tables("getcertificate")   # Displays wrong contents

