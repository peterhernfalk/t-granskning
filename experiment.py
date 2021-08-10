
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

FOLDER_CODE_GEN = "/code_gen"
FOLDER_JAXWS = "/code_gen/jaxws"
FOLDER_WCF = "/code_gen/wcf"
FOLDER_DOCS = "/docs"
FOLDER_SCHEMAS = "/schemas"
FOLDER_CORE_COMPONENTS = "/schemas/core_components"
FOLDER_INTERACTIONS = "/schemas/interactions"
FOLDER_TEST_SUITE = "/test_suite"

local_test = True

def __test_download_from_Bitbucket():
    import requests
    document_link = "https://developer.atlassian.com/bitbucket/api/2/reference/resource/"
    document_link = "https://api.bitbucket.org/2.0/repositories/rivta-domains/riv.clinicalprocess.healthcond.certificate"
    document_link = "https://api.bitbucket.org/2.0/repositories/rivta-domains/riv.clinicalprocess.activity.request/src/1.0.2/"

    document_link = "https://api.bitbucket.org/2.0/repositories/rivta-domains/riv.clinicalprocess.activity.request/src/1.0.2/docs"
    document_link = "https://api.bitbucket.org/2.0/repositories/rivta-domains/riv.clinicalprocess.activity.request/src/1.0.2/schemas"
    #document_link = "https://api.bitbucket.org/2.0/repositories/rivta-domains/riv.clinicalprocess.activity.request/src/1.0.2/schemas/interactions"
    #document_link = "https://api.bitbucket.org/2.0/repositories/rivta-domains/riv.clinicalprocess.activity.request/src/1.0.2/schemas/interactions/ProcessRequestConfirmationInteraction"
    #document_link = "https://api.bitbucket.org/2.0/repositories/rivta-domains/riv.clinicalprocess.activity.request/src/ee5bfaa4572cca699be516e1bc2fb374997c8879/schemas/interactions/ProcessRequestConfirmationInteraction/ProcessRequestConfirmationResponder_1.0.xsd"

    document_link = "https://api.bitbucket.org/2.0/repositories/rivta-domains/riv.clinicalprocess.activity.request/src/ee5bfaa4572cca699be516e1bc2fb374997c8879/?pagelen=100"

    document_link = "https://api.bitbucket.org/2.0/repositories/rivta-domains/riv.clinicalprocess.activity.request/src/ee5bfaa4572cca699be516e1bc2fb374997c8879/?max_depth=100&pagelen=100"
        # Relative links to all folderss in the repo can be found with search expression: "path
        # Relative links to all files in the repo can be found with search expression: "mimetype":null,"links":{"self":{"href"

    #document_link = "https://api.bitbucket.org/2.0/repositories/rivta-domains/riv.clinicalprocess.activity.request/src/ee5bfaa4572cca699be516e1bc2fb374997c8879/schemas/interactions/"
        # Relative links to TK folders can be found with search expression: "path
    #document_link = "https://api.bitbucket.org/2.0/repositories/rivta-domains/riv.clinicalprocess.activity.request/src/ee5bfaa4572cca699be516e1bc2fb374997c8879/schemas/interactions/ProcessRequestConfirmationInteraction"
        #Relative links to schema files (wsdl and xsd) can be found with search expression: "path

    #document_link = "https://bitbucket.org/rivta-domains/riv.clinicalprocess.activity.request/src/1.0.2/docs/TKB_clinicalprocess_activity_request.docx"
    """print()
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

    for file in code_gen_files:
        print(file)
    print()
    for file in docs_files:
        print(file)
    print()
    for file in core_components_files:
        print(file)
    print()
    for file in interactions_files:
        print(file)
    print()
    for file in test_suite_files:
        print(file)"""

    #files = __get_files_from_bitbucket_list(document_link, FOLDER_CODE_GEN)
    #files = __get_files_from_bitbucket_list(document_link, FOLDER_DOCS)
    __print_domain_files(__get_files_from_bitbucket_list(document_link, FOLDER_CORE_COMPONENTS))
    __print_domain_files(__get_files_from_bitbucket_list(document_link, FOLDER_INTERACTIONS))
    #files = __get_files_from_bitbucket_list(document_link, FOLDER_TEST_SUITE)

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

def __print_domain_files(files):
    print()
    for file in files:
        print(file)

def __get_files_from_bitbucket_list(document_link, file_folder):
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

    """for file in code_gen_files:
        print(file)
    print()
    for file in docs_files:
        print(file)
    print()
    for file in core_components_files:
        print(file)
    print()
    for file in interactions_files:
        print(file)
    print()
    for file in test_suite_files:
        print(file)"""

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

def __test_inmemory_filesystem():
    domain_name = 'riv.clinicalprocess.activity.request'
    tag = "1.0.2"

    global dir
    dir = __create_inmemory_file_structure("/"+domain_name)

    subfolders = []
    subfolders.append("ProcessRequestConfirmationInteraction")
    subfolders.append("ProcessRequestInteraction")
    subfolders.append("ProcessRequestOutcomeInteraction")
    dir = __add_interactions_subfolders(dir,"/"+domain_name,subfolders)

    # Add domain files
    ### dev ###
    with dir.open('/riv.clinicalprocess.activity.request/code_gen/jaxws/pom.xml', 'w') as pom: pom.write('text...')
    with dir.open('/riv.clinicalprocess.activity.request/code_gen/wcf/generate-src-rivtabp21.bat', 'w') as bat: bat.write('text...')
    with dir.open('/riv.clinicalprocess.activity.request/schemas/core_components/clinicalprocess_activity_request_1.0.xsd', 'w') as dom_xsd_1: dom_xsd_1.write('text...')
    with dir.open('/riv.clinicalprocess.activity.request/schemas/core_components/codes.xsd', 'w') as dom_xsd_2: dom_xsd_2.write('text...')
    with dir.open('/riv.clinicalprocess.activity.request/schemas/core_components/codes.xsd', 'w') as dom_xsd_2: dom_xsd_2.write('text...')
    with dir.open('/riv.clinicalprocess.activity.request/schemas/core_components/interoperability_headers_1.0.xsd', 'w') as dom_xsd_3: dom_xsd_3.write('text...')
    with dir.open('/riv.clinicalprocess.activity.request/schemas/core_components/itintegration_registry_1.0.xsd', 'w') as dom_xsd_4: dom_xsd_4.write('text...')
    with dir.open('/riv.clinicalprocess.activity.request/schemas/interactions/ProcessRequestConfirmationInteraction/ProcessRequestConfirmationInteraction_1.0_RIVTABP21.wsdl', 'w') as tk_1_wsdl: tk_1_wsdl.write('text...')
    with dir.open('/riv.clinicalprocess.activity.request/schemas/interactions/ProcessRequestConfirmationInteraction/ProcessRequestConfirmationResponder_1.0.xsd', 'w') as tk_1_xsd_1: tk_1_xsd_1.write('text...')
    ### dev ###

    ### dev ###
    file_2_download = "TKB_clinicalprocess_activity_request.docx"
    file_page_link = __get_file_page_link(domain_name, tag, FOLDER_DOCS, file_2_download)
    downloaded_file_page = __get_downloaded_file(file_page_link)
    file_head_hash = __get_head_hash(downloaded_file_page)
    file_link = __get_file_link(domain_name, tag, file_2_download, file_head_hash)
    downloaded_file = __get_downloaded_file(file_link)
    global document
    if downloaded_file.status_code != 404:
        if file_2_download.find(".docx") > -1:
            document = __get_docx_document(downloaded_file)
            """document_paragraphs = ""
            for paragraph in document.paragraphs:
                if paragraph.text.strip() != "":
                    document_paragraphs += paragraph.text + "<br>"
                    #print(paragraph.text)"""

        __add_files(dir,"/"+domain_name,FOLDER_DOCS,file_2_download)
    ### dev ###

    print("\n")
    print(dir.tree())

def __create_inmemory_file_structure(domain_folder):
    # Domain
    dir = fs.open_fs('mem://')
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

    return head_hash

def __get_file_page_link(domainname, tag, file_folder, file_name):
    """
    Beräknar url till sidan som innehåller länk till angivet dokument för vald domän och tag i Bitbucket-repot.

    Returnerar: länk till dokumentsidan
    """
    url_prefix = "https://bitbucket.org/rivta-domains/"
    url_domain = globals.domain_prefix + domainname + "/"
    url_src = "src/"
    url_tag = tag
    url_file_folder = file_folder + "/"
    domain_name = domainname.replace(".","_")
    #url_doc = document +"_" + domain_name + ".docx"
    document_page_link = url_prefix+url_domain+url_src+url_tag+url_file_folder+file_name

    return document_page_link

def __get_file_link(domain_name, tag, file_name, head_hash):
    """
    Beräknar url till angiven fil för vald domän och tag i Bitbucket-repot.

    Returnerar: länk som kan användas vid nerladdning av angiven fil
    """
    url_prefix = "https://bitbucket.org/rivta-domains/"
    url_domain = globals.domain_prefix + domain_name + "/"
    url_raw = "raw/"
    url_docs = "docs/"
    domain_name = domain_name.replace(".","_")
    #url_doc = document +"_" + domain_name + ".docx"
    file_link = url_prefix+url_domain+url_raw+head_hash+"/"+url_docs+file_name

    return file_link

def __get_docx_document(downloaded_document):
    """
    Läser in angivet dokuments innehåll i ett docx-Document.

    Returnerar: docx-Documentet
    """
    with io.BytesIO(downloaded_document.content) as inmemoryfile:
        docx_document = Document(inmemoryfile)

    return docx_document



##### Execute test #####
if local_test == True:
    __test_download_from_Bitbucket()
    __test_inmemory_filesystem()
    #__test_inspection_comments(globals.TKB,"REF-LINKS",404)
