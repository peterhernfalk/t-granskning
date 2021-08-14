#import os

from lxml import etree

import globals
import fs
import requests
from fs.memoryfs import MemoryFS
from fs.subfs import SubFS
from docx import Document
import io
import json

#from fs import open_fs
# https://stackoverflow.com/questions/51508179/how-to-construct-an-in-memory-virtual-file-system-and-then-write-this-structure
# https://readthedocs.org/projects/pyfilesystem2/downloads/pdf/latest/

FOLDER_CODE_GEN = "/code_gen"
FOLDER_JAXWS = "/code_gen/jaxws"
FOLDER_WCF = "/code_gen/wcf"
FOLDER_DOCS = "/docs"
FOLDER_SCHEMAS = "/schemas"
FOLDER_CORE_COMPONENTS = "/schemas/core_components"
FOLDER_INTERACTIONS = "/schemas/interactions"
FOLDER_TEST_SUITE = "/test_suite"

local_test = True

def __download_from_Bitbucket():
    link_2_repo_listing = "https://api.bitbucket.org/2.0/repositories/rivta-domains/riv.clinicalprocess.activity.request/src/ee5bfaa4572cca699be516e1bc2fb374997c8879/?max_depth=100&pagelen=100"

    global file_list
    file_list = []
    file_list.append(__get_file_list_from_repo(link_2_repo_listing, FOLDER_CODE_GEN))
    file_list.append(__get_file_list_from_repo(link_2_repo_listing, FOLDER_DOCS))
    file_list.append(__get_file_list_from_repo(link_2_repo_listing, FOLDER_CORE_COMPONENTS))
    file_list.append(__get_file_list_from_repo(link_2_repo_listing, FOLDER_INTERACTIONS))
    file_list.append(__get_file_list_from_repo(link_2_repo_listing, FOLDER_TEST_SUITE))
    __print_domain_files(file_list)

    #print(type(downloaded_requests_get))
    #print(type(downloaded_requests_get.text))
    #print(type(downloaded_requests_get.content))
    #downloaded_page_2_json = downloaded_requests_get.json()
    #print(downloaded_page_2_json)
    #print("downloaded_doc.text:",downloaded_doc.text)
    #print(json.dumps(dict_containing_json, indent=4))
    #print(type(dict_containing_json))
    #print(dict_containing_json)
    #print(json_dumps_dict)

    #print(json_dumps_dict['path'])
    #json_loads_dumps = json.loads(json_dumps_dict)
    #print(json_loads_dumps)

    #json_value_list = list(dict_containing_json.values())
    #json_value_list_1 = json.dumps(json_value_list[1])
    #json_test = json.loads(json_value_list_1)
    #print(type(json_test),json_test)

    #json_test2 = str(json_test).replace("[{'path'", "{'path'").replace("2188}]","2188}")
    #print("json_test2:",json_test2)

    #print(json_value_list_1)
    #print(type(json_value_list_1))
    #json.load(json_value_list)

    #for item in dict_containing_json.items():
    #    print(str(item))

    #print(json.loads(dict_containing_json.values()))
    #print(dict_containing_json.values())
    #print(dict_containing_json.keys())
    #print(dict_containing_json.items())
    #for value in dict_containing_json.values():
    #    print("value:",value)

    #print(f"json_file['values']: {json_file['values']}")
    #print({json_file['values']['mimetype']})
    #print(json_file['values'])
    #print(json_file['values']['path'])
    #x = json.dumps(json_file, indent=4, sort_keys=True)
    #print(x["href"])

def __build_and_load_inmemory_filesystem(domain_name, tag):
    global dir
    dir = __create_inmemory_file_structure("/"+domain_name)

    ### 2do: replace by dynamic code ###
    interactions_subfolders = []
    interactions_subfolders.append("ProcessRequestConfirmationInteraction")
    interactions_subfolders.append("ProcessRequestInteraction")
    interactions_subfolders.append("ProcessRequestOutcomeInteraction")
    dir = __add_interactions_subfolders(dir,"/"+domain_name,interactions_subfolders)
    ### 2do ###

    """
    Examples:
        code_gen/jaxws/pom.xml
        docs/IS_clinicalprocess_activity_request.docx
        schemas/core_components/clinicalprocess_activity_request_1.0.xsd
        schemas/interactions/ProcessRequestConfirmationInteraction/ProcessRequestConfirmationInteraction_1.0_RIVTABP21.wsdl
    """

    global file_list
    for file_array in file_list:
        for file in file_array:
            if "code_gen" in file:
                delimiter_index = file.rfind("/")
                path = "/"+domain_name+"/"+file[0:delimiter_index]
                file_in_path = file[delimiter_index+1:]
                #print("path,file_in_path",path,file_in_path)
                #downloaded_file = __get_file_from_repo(dir, "/"+domain_name, tag, "ProcessRequestConfirmationInteraction", file_in_path)
                interaction_folder = ""
                if "jaxws" in file:
                    file_folder = FOLDER_CODE_GEN + "/jaxws"
                elif "wcf" in file:
                    file_folder = FOLDER_CODE_GEN + "/wcf"
                else:
                    file_folder = FOLDER_CODE_GEN
                downloaded_file = __get_file_from_repo(dir, "/"+domain_name, tag, file_folder, interaction_folder, file_in_path)
                #print("code_gen, "+file_in_path+":\n", downloaded_file.text)
            if "docs" in file:
                ### 2do ###
                #file_2_download = "TKB_clinicalprocess_activity_request.docx"
                delimiter_index = file.rfind("/")
                path = "/"+domain_name+"/"+file[0:delimiter_index]
                file_in_path = file[delimiter_index+1:]
                #print("docs.file_in_path",file_in_path)
                file_page_link = __get_file_page_link(domain_name, tag, FOLDER_DOCS, file_in_path)
                print("docs.file_page_link",file_page_link)
                downloaded_file_page = __get_downloaded_file(file_page_link)
                print("docs.downloaded_file_page",downloaded_file_page)
                file_head_hash = __get_head_hash(downloaded_file_page)
                file_link = __get_file_link(domain_name, tag, FOLDER_DOCS, file_in_path, file_head_hash)
                print("docs.file_link",file_link)
                downloaded_file = __get_downloaded_file(file_link)
                #print(downloaded_file, file_link)
                global document
                if downloaded_file.status_code != 404:
                    with io.BytesIO(downloaded_file.content) as inmemoryfile:
                        #docx_document = Document(inmemoryfile)
                        #dir.open(domain_name + folder_name + "/" + interaction_folder + "/" + file_name, 'x')
                        file_2_save = "/riv.clinicalprocess.activity.request/docs/"+file_in_path
                        dir.open(file_2_save, 'x')
                        dir.writefile(file_2_save, inmemoryfile)
            ### 2do ###
            if "core_components" in file or "interactions" in file:
                delimiter_index = file.rfind("/")
                path = "/"+domain_name+"/"+file[0:delimiter_index]
                file_in_path = file[delimiter_index+1:]
                #print("path,file_in_path",path,file_in_path)
                #downloaded_file = __get_file_from_repo(dir, "/"+domain_name, tag, "ProcessRequestConfirmationInteraction", file_in_path)
                interaction_folder = ""
                if "core_components" in file:
                    file_folder = FOLDER_CORE_COMPONENTS
                else:
                    schemas_delimiter = file.find("schemas/interactions/")
                    interaction_folder = file[schemas_delimiter+21:delimiter_index]
                    print("interaction_folder",interaction_folder)
                    file_folder = FOLDER_INTERACTIONS
                downloaded_file = __get_file_from_repo(dir, "/"+domain_name, tag, file_folder, interaction_folder, file_in_path)
                if "schemas" in path:
                    print("downloaded schema file",path,file_in_path,downloaded_file)
                    #print("\tdownloaded_file.text",downloaded_file.text)
                    #print("\tdownloaded_file.content",downloaded_file.content)
                #dir.writefile(downloaded_file, path, file_in_path)



    print("\n")
    print(dir.tree())

    #print(list(dir.scandir("/riv.clinicalprocess.activity.request")))

    #os.system("ls /Users/peterhernfalk/Desktop")
    #os.system("ls mem://riv.clinicalprocess.activity.request/docs")
    #os.system("open -a Safari mem:///riv.clinicalprocess.activity.request/docs")
    #os.system("open -a Safari mem://")

    #dir.close()

def __print_domain_files(file_list):
    print()
    for file_array in file_list:
        for file in file_array:
            print(file)
        print()

def __get_file_list_from_repo(document_link, file_folder):
    ### 2do: simplify the code ###
    downloaded_requests_get = requests.get(document_link, stream=True)
    dict_containing_json = json.loads(downloaded_requests_get.content)
    json_dumps_dict = json.dumps(dict_containing_json['values'], indent=1)
    rsplit_json_dumps_dict = json_dumps_dict.rsplit("\n")
    code_gen_files = []
    docs_files = []
    core_components_files = []
    interactions_files = []
    test_suite_files = []
    for line in rsplit_json_dumps_dict:
        if line.find('"path') > 0:
            if line.find("pom") > 0 or line.find(".bat") > 0:
                code_gen_files.append(line.replace(" ","").replace('"path":"','').replace('",',''))
            elif line.find(".docx") > 0:
                docs_files.append(line.replace(" ","").replace('"path":"','').replace('",',''))
            elif line.find("core_components") > 0:
                if line.find(".xsd") > 0 or line.find(".wsdl") > 0:
                    core_components_files.append(line.replace(" ","").replace('"path":"','').replace('",',''))
            elif line.find("interactions") > 0:
                if line.find(".xsd") > 0 or line.find(".wsdl") > 0:
                    interactions_files.append(line.replace(" ","").replace('"path":"','').replace('",',''))
            elif line.find("test-suite") > 0 and line.find(".") > 0:
                test_suite_files.append(line.replace(" ","").replace('"path":"','').replace('",',''))

    if file_folder == FOLDER_CODE_GEN:
        return code_gen_files
    elif file_folder == FOLDER_DOCS:
        return docs_files
    elif file_folder == FOLDER_CORE_COMPONENTS:
        return core_components_files
    elif file_folder == FOLDER_INTERACTIONS:
        return interactions_files
    elif file_folder == FOLDER_TEST_SUITE:
        return test_suite_files

def __test_inspection_comments(document,inspection_type,inspection_result):
    comment = ""
    return comment

class InspectionComment:
    """
    Inspected_object: TKB
    Inspection: Revision_history
    Req: Revision_history MUST have same version as domain-tag
    Req_exclusion: don't use version suffix in comparison
    Inspection_comment: SVART: revisionshistoriken behöver uppdateras till granska domänversion
    """
    inspected_comment = ""


def __get_file_from_repo(dir, domain_name, tag, folder_name, interaction_folder, file_name):
    #https://bitbucket.org/rivta-domains/riv.clinicalprocess.activity.request/raw/ee5bfaa4572cca699be516e1bc2fb374997c8879/schemas/core_components/clinicalprocess_activity_request_1.0.xsd

    path_to_folder_and_file = file_name
    file_page_link = __get_file_page_link(domain_name, tag, folder_name, path_to_folder_and_file)
    #print("__get_file_from_repo.file_page_link",file_page_link)
    downloaded_file_page = __get_downloaded_file(file_page_link)
    file_head_hash = __get_head_hash(downloaded_file_page)
    file_link = __get_file_link(domain_name, tag, folder_name+"/"+interaction_folder+"/", file_name, file_head_hash)
    downloaded_file = __get_downloaded_file(file_link)

    with io.BytesIO(downloaded_file.content) as inmemoryfile:
        file_2_save = domain_name+folder_name+"/"+interaction_folder+"/"+file_name
        dir.open(file_2_save, 'x')
        dir.writefile(file_2_save,inmemoryfile)

    """global document
    if downloaded_file.status_code != 404:
        if file_name.find(".docx") > -1:
            document = __get_docx_document(downloaded_file)
        __add_files(dir,"/"+domain_name,folder_name)"""

    return downloaded_file


def __create_inmemory_file_structure(domain_folder):
    # Domain
    dir = fs.open_fs("mem://")
    dir.makedirs(domain_folder)
    SubFS(MemoryFS(), domain_folder)

    # Domain/code_gen
    dir.makedirs(domain_folder+FOLDER_CODE_GEN)
    SubFS(MemoryFS(), domain_folder+FOLDER_CODE_GEN)
    dir.makedirs(domain_folder+FOLDER_JAXWS)
    SubFS(MemoryFS(), domain_folder+FOLDER_JAXWS)
    dir.makedirs(domain_folder+FOLDER_WCF)
    SubFS(MemoryFS(), domain_folder+FOLDER_WCF)

    # Domain/docs
    dir.makedirs(domain_folder+FOLDER_DOCS)
    SubFS(MemoryFS(), domain_folder+FOLDER_DOCS)

    # Domain/schemas/core_components
    dir.makedirs(domain_folder+FOLDER_CORE_COMPONENTS)
    SubFS(MemoryFS(), domain_folder+FOLDER_CORE_COMPONENTS)

    # Domain/schemas/interactions
    dir.makedirs(domain_folder+FOLDER_INTERACTIONS)
    SubFS(MemoryFS(), domain_folder+FOLDER_INTERACTIONS)

    # Domain/test_suite
    dir.makedirs(domain_folder+FOLDER_TEST_SUITE)
    SubFS(MemoryFS(), domain_folder+FOLDER_TEST_SUITE)

    return dir

def __add_interactions_subfolders(dir,domain_folder,subfolders):
    for subfolder in subfolders:
        dir.makedirs(domain_folder+FOLDER_INTERACTIONS+"/"+subfolder)
        SubFS(MemoryFS(), domain_folder+FOLDER_INTERACTIONS+"/"+subfolder)

    return dir


"""def __add_file_2_dir(dir,domain_name,folder_name,file_name, file_contents):
    if folder_name == FOLDER_INTERACTIONS:
        file_2_save = domain_name+"/"+file_name
        #print("file_2_save:",file_2_save)
        with dir.open(file_2_save, 'x') as dir_file:
            #print("file_name:",file_name)
            #print("dir_file:",dir_file)
            dir_file.write(str(file_contents))
            #dir.writefile(file_name,dir_file)
        with dir.open(file_2_save, 'r') as dir_file:
            this_dir_file = dir_file.read()
            #print(this_dir_file,file_name)

    return dir"""

def __add_files(dir,domain_name,folder_name,files):
    if folder_name == FOLDER_DOCS:
        global document
        # for paragraph in document.paragraphs:
        #    print(paragraph.text)
        ### dev ###
        #document_link = "https://bitbucket.org/rivta-domains/riv.clinicalprocess.activity.request/src/1.0.2/docs/TKB_clinicalprocess_activity_request.docx"
        #downloaded_doc = requests.get(document_link, stream=True)
        #with dir.open(domain_name+FOLDER_DOCS+'/'+files, 'x') as tkb: tkb.write(str(downloaded_doc.text))
        #with dir.open(domain_name+FOLDER_DOCS+'/'+files, 'r') as tkb: print(tkb.read())
        with dir.open(domain_name+FOLDER_DOCS+'/'+files, 'x') as tkb:
            tkb.write(str(document))
        with dir.open(domain_name+FOLDER_DOCS+'/'+files, 'r') as tkb:
            this_tkb = tkb.read()
            #print(this_tkb)
        ### dev ###
    #elif folder_name == FOLDER_CORE_COMPONENTS:

    return dir

def __get_downloaded_file(file_link):
    """
    Laddar ner fil från angiven länk.

    Returnerar: nerladdad fil
    """
    downloaded_file = requests.get(file_link, stream=True)

    return downloaded_file

def __get_head_hash(document_page):
    """
    hämtar head-hash för det dokument som ska laddas ner. Hashen finns i den Bitbucketsida som innehåller länk till dokumentet.

    Returnerar: head-hash
    """
    hash_start = document_page.text.find('{"hash":')
    hash_end = hash_start+17
    head_hash = document_page.text[hash_start+10:hash_end]
    globals.head_hash = head_hash

    #print("__get_head_hash",hash_start,hash_end,head_hash,document_page.text[0:50])

    return head_hash

def __get_file_page_link(domain_name, tag, file_folder, file_name):
    """
    Beräknar url till sidan som innehåller länk till angivet dokument för vald domän och tag i Bitbucket-repot.

    Returnerar: länk till dokumentsidan
    """
    if "docx" in file_name:
        url_prefix = "https://bitbucket.org/rivta-domains/"
        url_domain = globals.domain_prefix + domain_name + "/"
        url_src = "src/"
        url_tag = tag
        url_file_folder = file_folder + "/"
        #print("__get_file_page_link.file_folder",file_folder)
        #if ".xsd" not in file_name and ".wsdl" not in file_name:
        #    url_file_folder = file_folder + "/"
        domain_name = domain_name.replace(".","_")
        #url_doc = document +"_" + domain_name + ".docx"
        #app:     document_page_link = url_prefix+url_domain+url_src+url_tag+url_docs+url_doc
        file_page_link = url_prefix+url_domain+url_src+url_tag+url_file_folder+file_name
        #print("__get_file_page_link.inparameters",domain_name, tag, file_folder, file_name)
        #print("__get_file_page_link.page link elements",url_prefix,url_domain,url_src,url_tag,url_file_folder,file_name)
        print("__get_file_page_link.docs.file_page_link",file_page_link)
    else:
        print("__get_file_page_link.inparams",domain_name, tag, file_folder, file_name)
        #file_page_link = __get_file_link(domain_name, tag, file_name, "")
        url_prefix = "https://bitbucket.org/rivta-domains"
        url_domain = globals.domain_prefix + domain_name
        domain_name = domain_name.replace(".","_")
        url_src = "/src/"
        url_tag = tag
        file_page_link = url_prefix+url_domain+url_src+url_tag+file_folder+"/"+file_name


    return file_page_link

def __get_file_link(domain_name, tag, file_folder, file_name, head_hash):
    """
    Beräknar url till angiven fil för vald domän och tag i Bitbucket-repot.

    Returnerar: länk som kan användas vid nerladdning av angiven fil
    """
    if "docx" in file_name:
        url_prefix = "https://bitbucket.org/rivta-domains/"
        url_domain = globals.domain_prefix + domain_name + "/"
        url_raw = "raw/"
        url_docs = "docs/"
        domain_name = domain_name.replace(".","_")
        #url_doc = document +"_" + domain_name + ".docx"
        file_link = url_prefix+url_domain+url_raw+head_hash+"/"+url_docs+file_name
    else:
        #https://bitbucket.org/rivta-domains/riv.clinicalprocess.activity.request/raw/ee5bfaa4572cca699be516e1bc2fb374997c8879/schemas/core_components/clinicalprocess_activity_request_1.0.xsd
        url_prefix = "https://bitbucket.org/rivta-domains"
        url_domain = globals.domain_prefix + domain_name
        domain_name = domain_name.replace(".","_")
        url_raw = "/raw/"
        #url_tag = tag
        file_link = url_prefix+url_domain+url_raw+head_hash+file_folder+"/"+file_name

    #print("__get_file_link.file_link:",file_link)

    return file_link

def __get_docx_document(downloaded_document):
    """
    Läser in angivet dokuments innehåll i ett docx-Document.

    Returnerar: docx-Documentet
    """
    #print("__get_docx_document.downloaded_document",downloaded_document.content)
    with io.BytesIO(downloaded_document.content) as inmemoryfile:
        docx_document = Document(inmemoryfile)


    return docx_document

def __wsdlvalidation():
    #pip install lxml
    from lxml import etree
    global dir
    #xml_path = dir.open('/riv.clinicalprocess.activity.request/schemas/core_components/','r')
    #xsd_path = dir.open('/riv.clinicalprocess.activity.request/schemas/core_components/clinicalprocess_activity_request_1.0.xsd','r')
    #with dir.open('/riv.clinicalprocess.activity.request/schemas/interactions/ProcessRequestConfirmationInteraction/ProcessRequestConfirmationInteraction_1.0_RIVTABP21.wsdl', 'w') as tk_1_wsdl: tk_1_wsdl.write('text...')
    #with dir.open('/riv.clinicalprocess.activity.request/schemas/interactions/ProcessRequestConfirmationInteraction/ProcessRequestConfirmationResponder_1.0.xsd', 'w') as tk_1_xsd_1: tk_1_xsd_1.write('text...')

    #print(dir.isfile(('/riv.clinicalprocess.activity.request/schemas/interactions/ProcessRequestConfirmationInteraction/ProcessRequestConfirmationInteraction_1.0_RIVTABP21.wsdl')))

    xml_path = dir.open('/riv.clinicalprocess.activity.request/schemas/interactions/ProcessRequestConfirmationInteraction/ProcessRequestConfirmationInteraction_1.0_RIVTABP21.wsdl', 'r')
    xsd_path = dir.open('/riv.clinicalprocess.activity.request/schemas/interactions/ProcessRequestConfirmationInteraction/ProcessRequestConfirmationResponder_1.0.xsd', 'r')
    #print(xml_path.read())

    #xml_path = dir.open('/riv.clinicalprocess.activity.request/schemas/core_components/clinicalprocess_activity_request_1.0.xsd', 'r')
    #xsd_path = dir.open('/riv.clinicalprocess.activity.request/schemas/core_components/clinicalprocess_activity_request_1.0.xsd', 'r')
    #print(xml_path.read())

    validate(xml_path, xsd_path)

def validate(xml_path: str, xsd_path: str) -> bool:
    print("xml_path:", xml_path)
    print("xsd_path:", xsd_path)

    #xmlschema_doc = etree.parse(xsd_path)
    #xmlschema = etree.XMLSchema(xmlschema_doc)
    #xml_doc = etree.parse(xml_path)
    #result = xmlschema.validate(xml_doc)

    return "result"


##### Execute test #####
if local_test == True:
    __download_from_Bitbucket()
    __build_and_load_inmemory_filesystem("riv.clinicalprocess.activity.request", "1.0.2")
    __wsdlvalidation()

    #__test_inspection_comments(globals.TKB,"REF-LINKS",404)
