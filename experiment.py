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
from fs import open_fs

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

#global dir
used_domain_name = ""
used_tag = ""

local_test = True


def __build_and_load_inmemory_filesystem(domain_name, tag):
    #2do: explore how to get repo listing for given tag, see: https://pygithub.readthedocs.io/en/latest/apis.html
    # Doesn't use the tag: https://api.bitbucket.org/2.0/repositories/rivta-domains/riv.clinicalprocess.logistics.logistics/src/56ec8ddc62098574d936eb623fee12e253bb42f3/?tag=2.0.4_RC1&pagelen=100&max_depth=10
    # manually added ref works: https://api.bitbucket.org/2.0/repositories/rivta-domains/riv.clinicalprocess.logistics.logistics/src/92f191f4e5379cc52c0a5e25c5d58e79b13a4251/?tag=2.0.4_RC1&pagelen=100&max_depth=10
    global link_2_repo_listing
    global domain_hash_in_repo
    domain_hash_in_repo = __get_domain_hash_from_repo(domain_name, tag)
    link_2_repo_listing = "https://api.bitbucket.org/2.0/repositories/rivta-domains/"+domain_name+"/src/?pagelen=100&max_depth=10&tag="+tag

    global dir
    dir = __create_inmemory_file_structure("/"+domain_name)

    global domain_folder_name
    domain_folder_name = domain_name

    global used_domain_name, used_tag
    used_domain_name = domain_name
    used_tag = tag

    ### test ###
    global dir_complete
    dir_complete = __save_complete_structure_and_files_in_filesys(domain_name, link_2_repo_listing)
    print("dir_complete:")
    print(dir_complete.tree())
    #print(list(dir_complete.scandir("/riv.clinicalprocess.logistics.logistics")))
    ##############################
    home_fs = open_fs(dir_complete)
    filter = "*"
    #display_file_contents = False
    #file_in_dir = False

    #print("\n---Visar innehållet i det virtuella filsystemet---")
    for path in home_fs.walk.files(filter=[filter]):
        #print("  dir_complete, path:",path)
        """this_dir_file = ""
        exists_in_dir = dir_complete.exists(path)
        is_file = dir_complete.isfile(path)
        print("  ",str(exists_in_dir) + " " + str(is_file),"(exists, isfile)",path)
        if file_2_display in path:
            file_in_dir = True
            with dir_complete.open(path, 'r') as dir_file:
                this_dir_file = dir_file.read()
                if display_file_contents == True:
                    print("\tfilinnehåll [0:100]:" + this_dir_file[0:100])
        if "wsdl" in path or "xsd" in path:
            if this_dir_file != "":
                __validate_xml_file(this_dir_file)"""
    ##############################

    """for file_array in file_list:
        for file in file_array:
            if "code_gen" in file:
                delimiter_index = file.rfind("/")
                path = "/"+domain_name+"/"+file[0:delimiter_index]
                file_in_path = file[delimiter_index+1:]
                interaction_folder = ""
                if "jaxws" in file:
                    file_folder = FOLDER_CODE_GEN + "/jaxws"
                elif "wcf" in file:
                    file_folder = FOLDER_CODE_GEN + "/wcf"
                else:
                    file_folder = FOLDER_CODE_GEN
                downloaded_file = __get_file_from_repo(dir, "/"+domain_name, tag, file_folder, interaction_folder, file_in_path)
                print("downloaded file", downloaded_file, file_in_path, "\t",dir.exists("/"+domain_name+file_folder+"/"+file_in_path), "(exists)")
                #print("pom",downloaded_file.text)
            if "docs" in file:
                delimiter_index = file.rfind("/")
                path = "/"+domain_name+"/"+file[0:delimiter_index]
                file_in_path = file[delimiter_index+1:]
                file_page_link = __get_file_page_link(domain_name, tag, FOLDER_DOCS, file_in_path)
                downloaded_file_page = __get_downloaded_file(file_page_link)
                file_head_hash = __get_head_hash(downloaded_file_page)
                file_link = __get_file_link(domain_name, tag, FOLDER_DOCS, file_in_path, file_head_hash)
                downloaded_file = __get_downloaded_file(file_link)
                global document
                if downloaded_file.status_code != 404:
                    path = "/"+domain_name+"/docs/"
                    dir = __write_file_in_filesys(dir, path, file_in_path, downloaded_file)
                print("downloaded_file", downloaded_file, file_in_path, "\t",dir.exists("/" + domain_name + FOLDER_DOCS + "/" + file_in_path), "(exists)")
            if "core_components" in file or "interactions" in file:
                #print("__build_and_load_inmemory_filesystem.file",file)
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
                    #print("interaction_folder",interaction_folder)
                    file_folder = FOLDER_INTERACTIONS
                downloaded_file = __get_file_from_repo(dir, "/"+domain_name, tag, file_folder, interaction_folder, file_in_path)
                if "core_components" in path:
                    print("downloaded_file, core", downloaded_file, file_in_path, "\t", dir.exists("/" + domain_name + FOLDER_CORE_COMPONENTS + "/" + interaction_folder + "/" + file_in_path), dir.isfile("/" + domain_name + FOLDER_CORE_COMPONENTS + "/" + interaction_folder + "/" + file_in_path), "(exists, isfile)")
                elif "interactions" in path:
                    print("downloaded_file, interactions", downloaded_file, file_in_path, "\t", dir.exists("/" + domain_name + FOLDER_INTERACTIONS + "/" + interaction_folder + "/" + file_in_path), dir.isfile("/" + domain_name + FOLDER_INTERACTIONS + "/" + interaction_folder + "/" + file_in_path), "(exists, isfile)")"""
    ### test ###

    global file_list
    file_list = []
    file_list.append(__get_file_list_from_repo(link_2_repo_listing, FOLDER_CODE_GEN))
    file_list.append(__get_file_list_from_repo(link_2_repo_listing, FOLDER_DOCS))
    file_list.append(__get_file_list_from_repo(link_2_repo_listing, FOLDER_CORE_COMPONENTS))
    file_list.append(__get_file_list_from_repo(link_2_repo_listing, FOLDER_INTERACTIONS))
    file_list.append(__get_file_list_from_repo(link_2_repo_listing, FOLDER_TEST_SUITE))
    __print_domain_files(file_list)

    ### 2do: replace by dynamic code ###
    #interactions_subfolders = []
    #interactions_subfolders.append("ProcessRequestConfirmationInteraction")
    #interactions_subfolders.append("ProcessRequestInteraction")
    #interactions_subfolders.append("ProcessRequestOutcomeInteraction")
    #schemas_delimiter = file.find("schemas/interactions/")
    #interaction_folder = file[schemas_delimiter + 21:delimiter_index]

    #dir = __add_interactions_subfolders(dir,"/"+domain_name,interactions_subfolders)
    dir = __save_interactions_subfolders_in_filesys(dir)
    #print(__save_interactions_subfolders_in_filesys(dir))
    ### 2do ###

    #global file_list
    #print(dir.tree())
    for file_array in file_list:
        for file in file_array:
            if "code_gen" in file:
                delimiter_index = file.rfind("/")
                path = "/"+domain_name+"/"+file[0:delimiter_index]
                file_in_path = file[delimiter_index+1:]
                interaction_folder = ""
                if "jaxws" in file:
                    file_folder = FOLDER_CODE_GEN + "/jaxws"
                elif "wcf" in file:
                    file_folder = FOLDER_CODE_GEN + "/wcf"
                else:
                    file_folder = FOLDER_CODE_GEN
                downloaded_file = __get_file_from_repo(dir, "/"+domain_name, tag, file_folder, interaction_folder, file_in_path)
                print("downloaded file", downloaded_file, file_in_path, "\t",dir.exists("/"+domain_name+file_folder+"/"+file_in_path), "(exists)")
                #print("pom",downloaded_file.text)
            if "docs" in file:
                delimiter_index = file.rfind("/")
                path = "/"+domain_name+"/"+file[0:delimiter_index]
                file_in_path = file[delimiter_index+1:]
                file_page_link = __get_file_page_link(domain_name, tag, FOLDER_DOCS, file_in_path)
                downloaded_file_page = __get_downloaded_file(file_page_link)
                file_head_hash = __get_head_hash(downloaded_file_page)
                file_link = __get_file_link(domain_name, tag, FOLDER_DOCS, file_in_path, file_head_hash)
                downloaded_file = __get_downloaded_file(file_link)
                global document
                if downloaded_file.status_code != 404:
                    path = "/"+domain_name+"/docs/"
                    dir = __write_file_in_filesys(dir, path, file_in_path, downloaded_file)
                print("downloaded_file", downloaded_file, file_in_path, "\t",dir.exists("/" + domain_name + FOLDER_DOCS + "/" + file_in_path), "(exists)")
            if "core_components" in file or "interactions" in file:
                #print("__build_and_load_inmemory_filesystem.file",file)
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
                    #print("interaction_folder",interaction_folder)
                    file_folder = FOLDER_INTERACTIONS
                downloaded_file = __get_file_from_repo(dir, "/"+domain_name, tag, file_folder, interaction_folder, file_in_path)
                if "core_components" in path:
                    print("downloaded_file, core", downloaded_file, file_in_path, "\t", dir.exists("/" + domain_name + FOLDER_CORE_COMPONENTS + "/" + interaction_folder + "/" + file_in_path), dir.isfile("/" + domain_name + FOLDER_CORE_COMPONENTS + "/" + interaction_folder + "/" + file_in_path), "(exists, isfile)")
                elif "interactions" in path:
                    print("downloaded_file, interactions", downloaded_file, file_in_path, "\t", dir.exists("/" + domain_name + FOLDER_INTERACTIONS + "/" + interaction_folder + "/" + file_in_path), dir.isfile("/" + domain_name + FOLDER_INTERACTIONS + "/" + interaction_folder + "/" + file_in_path), "(exists, isfile)")
                #dir.writefile(downloaded_file, path, file_in_path)

    print("dir:\n")
    print(dir.tree())

    #print(list(dir.scandir("/riv.clinicalprocess.activity.request")))

    #os.system("ls /Users/peterhernfalk/Desktop")
    #os.system("ls mem://riv.clinicalprocess.activity.request/docs")
    #os.system("open -a Safari mem:///riv.clinicalprocess.activity.request/docs")
    #os.system("open -a Safari mem://")

    #dir.close()

#def __download_from_Bitbucket(domain_name, tag):
#    global link_2_repo_listing

#    link_2_repo_listing = "https://api.bitbucket.org/2.0/repositories/rivta-domains/"+domain_name+"/src/?pagelen=100&max_depth=100&tag="+tag

    """global file_list
    file_list = []
    file_list.append(__get_file_list_from_repo(link_2_repo_listing, FOLDER_CODE_GEN))
    file_list.append(__get_file_list_from_repo(link_2_repo_listing, FOLDER_DOCS))
    file_list.append(__get_file_list_from_repo(link_2_repo_listing, FOLDER_CORE_COMPONENTS))
    file_list.append(__get_file_list_from_repo(link_2_repo_listing, FOLDER_INTERACTIONS))
    file_list.append(__get_file_list_from_repo(link_2_repo_listing, FOLDER_TEST_SUITE))
    __print_domain_files(file_list)"""


##############################################################################

def __get_domain_hash_from_repo(domain_name, tag):
    domain_hash_in_repo = ""
    """
        https://api.bitbucket.org/2.0/repositories/rivta-domains/riv.clinicalprocess.logistics.logistics/refs?tag=2.0.4_RC1
        Want to find: 92f191f4e5379cc52c0a5e25c5d58e79b13a4251
        Seems to work:
            1. Read the page: https://api.bitbucket.org/2.0/repositories/rivta-domains/riv.clinicalprocess.logistics.logistics/refs?tag=2.0.4_RC1
            2. Search for: '"type": "tag", "target": {"hash": "'
            3. Immediately after that, extract the hash (example: '92f191f4e5379cc52c0a5e25c5d58e79b13a4251", ')
                from index+35 from search
                to '", '
    """
    #link_2_repo_hash_page = "https://api.bitbucket.org/2.0/repositories/rivta-domains/"+domain_name+"/src/?pagelen=100&max_depth=10&tag="+tag
    link_2_repo_hash_page = "https://api.bitbucket.org/2.0/repositories/rivta-domains/"+domain_name+"/refs?tag="+tag
    downloaded_file = requests.get(link_2_repo_hash_page, stream=True)
    search_index = downloaded_file.text.find('"type": "tag", "target": {"hash": "')
    domain_hash_in_repo = downloaded_file.text[search_index+35:search_index+75]
    #print("__get_domain_hash_from_repo",domain_hash_in_repo)

    return domain_hash_in_repo

def __save_complete_structure_and_files_in_filesys(domain_name, document_link):
    downloaded_requests_get = requests.get(document_link, stream=True)
    dict_containing_json = json.loads(downloaded_requests_get.content)
    json_dumps_dict = json.dumps(dict_containing_json['values'], indent=1)
    rsplit_json_dumps_dict = json_dumps_dict.rsplit("\n")
    code_gen_files = []
    docs_files = []
    core_components_files = []
    interactions_files = []
    test_suite_files = []

    domain_folder = "/"+domain_name
    dir = fs.open_fs("mem://")
    dir.makedirs(domain_folder)
    SubFS(MemoryFS(), domain_folder)

    for line in rsplit_json_dumps_dict:
        if line.find('"path') > 0:
            #print("__test_save_structure_from_repo.line", line)
            file_to_save = line.replace(" ", "").replace('"path":"', '').replace('",', '')
            #print("__test_save_structure_from_repo.file_to_save", file_to_save)
            dir.makedirs(domain_folder + "/" + file_to_save)
            SubFS(MemoryFS(), domain_folder + "/" + file_to_save)
            downloaded_file = __dev_get_file_from_repo(file_to_save)
            """with dir.open(downloaded_file, 'rb', buffering =0) as inmemoryfile:
                if dir.exists(file_to_save) == False:  # exists isempty
                    dir.open(file_to_save, 'x')
                    dir.writefile(file_to_save, inmemoryfile)"""

    return dir

def __dev_get_file_from_repo(file_path):
    global used_domain_name
    global used_tag

    downloaded_file = ""
    folder_name = ""
    path_to_folder_and_file = ""
    ###file_to_download = ""
    file_delimiter = file_path.rfind("/")
    if file_delimiter > 0:
        #folder_name = "/"+file_path[0:file_delimiter]
        path_to_folder_and_file = file_path.strip()
        print("__dev_get_file_from_repo", folder_name, path_to_folder_and_file)
    file_page_link = __get_file_page_link(used_domain_name, used_tag, folder_name, path_to_folder_and_file)
    print("__dev_get_file_from_repo", folder_name, path_to_folder_and_file,file_page_link)
    #downloaded_file_page = __get_downloaded_file(file_page_link)
    #file_head_hash = __get_head_hash(downloaded_file_page)
    #file_link = __get_file_link(domain_name, tag, folder_name+"/"+interaction_folder+"/", file_name, file_head_hash)
    #downloaded_file = __get_downloaded_file(file_link)

    ###path = domain_name+folder_name+"/"+interaction_folder+"/"
    ###global dir_complete
    ###dir_complete = __write_file_in_filesys(dir_complete, path, file_name, downloaded_file)

    return downloaded_file

def __create_inmemory_file_structure(domain_folder):
    # Domain
    dir = fs.open_fs("mem://")
    dir.makedirs(domain_folder)
    SubFS(MemoryFS(), domain_folder)

    # Domain/code_gen
    #dir.makedirs(domain_folder+FOLDER_CODE_GEN)
    #SubFS(MemoryFS(), domain_folder+FOLDER_CODE_GEN)
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

def __write_file_in_filesys(dir, path, file_name, downloaded_file):
    temp_dir = dir
    with io.BytesIO(downloaded_file.content) as inmemoryfile:
        file_2_save = path + file_name
        file_2_save = file_2_save.replace("//","/")
        #if "interactions" in file_2_save:
        #print("__write_file_in_filesys, before", temp_dir.exists(file_2_save), temp_dir.isempty(file_2_save), file_2_save)
        if temp_dir.exists(file_2_save) == False:   #exists isempty
            temp_dir.open(file_2_save, 'x')
            temp_dir.writefile(file_2_save, inmemoryfile)

    return temp_dir


def __write_file_in_filesys_2(dir, path, file_name, downloaded_file):
    ### 2do ###
    temp_dir = dir
    with dir.open(downloaded_file, 'rb', buffering =0) as inmemoryfile:
        file_2_save = path + file_name
        file_2_save = file_2_save.replace("//", "/")
        if "interactions" in file_2_save:
            print("__write_file_in_filesys, before", temp_dir.exists(file_2_save), temp_dir.isempty(file_2_save),
                  file_2_save)
        if temp_dir.exists(file_2_save) == False:  # exists isempty
            temp_dir.open(file_2_save, 'x')
            temp_dir.writefile(file_2_save, inmemoryfile)

    """with io.BytesIO(downloaded_file.content) as inmemoryfile:
        file_2_save = path + file_name
        file_2_save = file_2_save.replace("//","/")
        if "interactions" in file_2_save:
            print("__write_file_in_filesys, before", temp_dir.exists(file_2_save), temp_dir.isempty(file_2_save), file_2_save)
        if temp_dir.exists(file_2_save) == False:   #exists isempty
            temp_dir.open(file_2_save, 'x')
            temp_dir.writefile(file_2_save, inmemoryfile)"""

        #elif temp_dir.exists(file_2_save) == True:
        #    if temp_dir.isempty(file_2_save) == True:
        #        temp_dir.remove(file_2_save)
        #        temp_dir.open(file_2_save, 'x')
        #        temp_dir.writefile(file_2_save, inmemoryfile)

            #print("__write_file_in_filesys, isfile",temp_dir.isfile(file_2_save),file_2_save)
        #print("__write_file_in_filesys, after", temp_dir.exists(file_2_save), file_2_save)
        #print("__write_file_in_filesys.file_2_save",file_2_save,dir.exists(file_2_save))

    #print(dir.tree())
    ### 2do ###
    return temp_dir

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

    #global interactions_subfolders
    #interactions_subfolders = []
    for line in rsplit_json_dumps_dict:
        delimiter_index = line.rfind("/")
        if line.find('"path') > 0:
            #if file_folder == FOLDER_CODE_GEN:
            #    print("__get_file_list_from_repo.interactions line", line)
            if line.find("pom") > 0 or line.find(".bat") > 0:
                code_gen_files.append(line.replace(" ","").replace('"path":"','').replace('",',''))
            elif line.find(".docx") > 0:
                docs_files.append(line.replace(" ","").replace('"path":"','').replace('",',''))
            elif line.find("core_components") > 0:
                if line.find(".xsd") > 0 or line.find(".wsdl") > 0:
                    core_components_files.append(line.replace(" ","").replace('"path":"','').replace('",',''))
            elif line.find("interactions") > 0:
                #print("__get_file_list_from_repo.interactions line",line)
                schemas_delimiter = line.find("schemas/interactions/")
                #interactions_subfolders.append(line[schemas_delimiter + 21:delimiter_index])
                #print("__get_file_list_from_repo.interactions_subfolders",interactions_subfolders)
                if line.find(".xsd") > 0 or line.find(".wsdl") > 0:
                    interactions_files.append(line.replace(" ","").replace('"path":"','').replace('",',''))
            elif line.find("test-suite") > 0 and line.find(".") > 0:
                test_suite_files.append(line.replace(" ","").replace('"path":"','').replace('",',''))

    #dir = __add_interactions_subfolders(dir,"/"+domain_name,interactions_subfolders)
    """
    interactions_subfolders = []
    interactions_subfolders.append("ProcessRequestConfirmationInteraction")
    interactions_subfolders.append("ProcessRequestInteraction")
    interactions_subfolders.append("ProcessRequestOutcomeInteraction")
    #schemas_delimiter = file.find("schemas/interactions/")
    #interaction_folder = file[schemas_delimiter + 21:delimiter_index]

    dir = __add_interactions_subfolders(dir,"/"+domain_name,interactions_subfolders)
    """

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


def __get_file_from_repo(in_dir, domain_name, tag, folder_name, interaction_folder, file_name):
    #https://bitbucket.org/rivta-domains/riv.clinicalprocess.activity.request/raw/ee5bfaa4572cca699be516e1bc2fb374997c8879/schemas/core_components/clinicalprocess_activity_request_1.0.xsd

    path_to_folder_and_file = file_name
    file_page_link = __get_file_page_link(domain_name, tag, folder_name, path_to_folder_and_file)
    #print("__get_file_from_repo.file_page_link",file_page_link)
    downloaded_file_page = __get_downloaded_file(file_page_link)
    file_head_hash = __get_head_hash(downloaded_file_page)
    file_link = __get_file_link(domain_name, tag, folder_name+"/"+interaction_folder+"/", file_name, file_head_hash)
    downloaded_file = __get_downloaded_file(file_link)

    path = domain_name+folder_name+"/"+interaction_folder+"/"
    global dir
    dir = __write_file_in_filesys(in_dir, path, file_name, downloaded_file)
    #print("__get_file_from_repo, after", dir.exists("/riv.clinicalprocess.activity.request/schemas/core_components/clinicalprocess_activity_request_1.0.xsd"))
    #print("__get_file_from_repo, after", dir.exists(path+file_name),path+file_name)

    """global document
    if downloaded_file.status_code != 404:
        if file_name.find(".docx") > -1:
            document = __get_docx_document(downloaded_file)
        __add_files(dir,"/"+domain_name,folder_name)"""

    return downloaded_file


def __add_interactions_subfolders(dir,domain_folder,subfolders):
    for subfolder in subfolders:
        dir.makedirs(domain_folder+FOLDER_INTERACTIONS+"/"+subfolder)
        SubFS(MemoryFS(), domain_folder+FOLDER_INTERACTIONS+"/"+subfolder)

    return dir

def __save_interactions_subfolders_in_filesys(dir):
    global link_2_repo_listing
    global domain_folder_name
    downloaded_requests_get = requests.get(link_2_repo_listing, stream=True)
    dict_containing_json = json.loads(downloaded_requests_get.content)
    json_dumps_dict = json.dumps(dict_containing_json['values'], indent=1)
    rsplit_json_dumps_dict = json_dumps_dict.rsplit("\n")

    interactions_subfolders = []
    for line in rsplit_json_dumps_dict:
        delimiter_index = line.rfind('",')
        if line.find('"path') > 0:
            if line.find("schemas/interactions/") > 0:
                schemas_delimiter = line.find("schemas/interactions/")
                subfolder_name = line[schemas_delimiter + 21:delimiter_index]
                if subfolder_name != "" and subfolder_name not in interactions_subfolders and "/" not in subfolder_name:
                    interactions_subfolders.append(subfolder_name)
                    dir.makedirs(domain_folder_name+FOLDER_INTERACTIONS+"/"+subfolder_name)
                    SubFS(MemoryFS(), domain_folder_name+FOLDER_INTERACTIONS+"/"+subfolder_name)

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

"""def __add_files(dir,domain_name,folder_name,files):
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

    return dir"""

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
        #print("__get_file_page_link.docs.file_page_link",file_page_link)
    else:
        #print("__get_file_page_link.inparams",domain_name, tag, file_folder, file_name)
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

    wsdl = "/riv.clinicalprocess.logistics.logistics/schemas/interactions/GetCareContactsInteraction/GetCareContactsInteraction_3.0_RIVTABP21.wsdl"
    xsd = "/riv.clinicalprocess.logistics.logistics/schemas/interactions/GetCareContactsInteraction/GetCareContactsResponder_3.0.xsd"

    wsdl = "/riv.crm.requeststatus/schemas/interactions/GetRequestActivitiesInteraction/GetRequestActivitiesInteraction_2.0_RIVTABP21.wsdl"
    xsd = "/riv.crm.requeststatus/schemas/interactions/GetRequestActivitiesInteraction/GetRequestActivitiesResponder_2.0.xsd"

    xsd = "/riv.crm.requeststatus/schemas/core_components/crm_requeststatus_2.0.xsd"

    #xml_path = dir.open('/riv.clinicalprocess.activity.request/schemas/core_components/','r')
    #xsd_path = dir.open('/riv.clinicalprocess.activity.request/schemas/core_components/clinicalprocess_activity_request_1.0.xsd','r')
    #with dir.open('/riv.clinicalprocess.activity.request/schemas/interactions/ProcessRequestConfirmationInteraction/ProcessRequestConfirmationInteraction_1.0_RIVTABP21.wsdl', 'w') as tk_1_wsdl: tk_1_wsdl.write('text...')
    #with dir.open('/riv.clinicalprocess.activity.request/schemas/interactions/ProcessRequestConfirmationInteraction/ProcessRequestConfirmationResponder_1.0.xsd', 'w') as tk_1_xsd_1: tk_1_xsd_1.write('text...')

    #print(dir.isfile(('/riv.clinicalprocess.activity.request/schemas/interactions/ProcessRequestConfirmationInteraction/ProcessRequestConfirmationInteraction_1.0_RIVTABP21.wsdl')))

    #print("dir.exists: wsdl",dir.exists('/riv.clinicalprocess.activity.request/schemas/interactions/ProcessRequestConfirmationInteraction/ProcessRequestConfirmationInteraction_1.0_RIVTABP21.wsdl'))
    #print("dir.exists: xsd",dir.exists('/riv.clinicalprocess.activity.request/schemas/interactions/ProcessRequestConfirmationInteraction/ProcessRequestConfirmationResponder_1.0.xsd'))
    #xml_path = dir.open('/riv.clinicalprocess.activity.request/schemas/interactions/ProcessRequestConfirmationInteraction/ProcessRequestConfirmationInteraction_1.0_RIVTABP21.wsdl', 'r')
    #xsd_path = dir.open('/riv.clinicalprocess.activity.request/schemas/interactions/ProcessRequestConfirmationInteraction/ProcessRequestConfirmationResponder_1.0.xsd', 'r')
    #print(xsd_path.read())

    #xml_path = dir.open('/riv.clinicalprocess.activity.request/schemas/core_components/clinicalprocess_activity_request_1.0.xsd', 'r')
    #xsd_path = dir.open('/riv.clinicalprocess.activity.request/schemas/core_components/clinicalprocess_activity_request_1.0.xsd', 'r')

    #xml_path = dir.open('/riv.clinicalprocess.healthcond.basic/schemas/interactions/GetObservationsInteraction/GetObservationsInteraction_2.0_RIVTABP21.wsdl', 'r')
    #xsd_path = dir.open('/riv.clinicalprocess.healthcond.basic/schemas/interactions/GetObservationsInteraction/GetObservationsResponder_2.0.xsd', 'r')
    #print(dir.open('/riv.clinicalprocess.healthcond.basic/schemas/interactions/GetObservationsInteraction/GetObservationsInteraction_2.0_RIVTABP21.wsdl', 'r'))
    #print(dir.open('/riv.clinicalprocess.healthcond.basic/schemas/core_components/itintegration_registry_1.0.xsd', 'r'))
    #print("dir.isfile",dir.isfile('/riv.clinicalprocess.healthcond.basic/schemas/interactions/GetObservationsInteraction/GetObservationsInteraction_2.0_RIVTABP21.wsdl'))

    #pom = "/riv.crm.requeststatus/code_gen/jaxws/pom.xml"
    #xsd = "/riv.crm.requeststatus/schemas/core_components/crm_requeststatus_2.0.xsd"
    #x = dir.open(pom)


    print("wsdl, dir.exists:",dir.exists(wsdl))
    if dir.exists(wsdl) == True:
        print("wsdl, dir.isfile:",dir.isfile(wsdl))
        if dir.isfile(wsdl) == True:
            print("wsdl, dir.open:",dir.open(wsdl))
        if dir.exists(wsdl) == True and dir.isfile(wsdl) == True:
            print(wsdl.read())

    print("xsd, dir.exists:",dir.exists(xsd))
    if dir.exists(xsd) == True:
        print("xsd, dir.isfile:",dir.isfile(xsd))
        if dir.isfile(xsd) == True:
            print("xsd, dir.open:",dir.open(xsd))
        if dir.exists(xsd) == True and dir.isfile(xsd) == True:
            #x = dir.open(xsd)
            #print(x)
            print("xsd.read()")
            #xmlschema_doc = etree.parse(xsd)

    #validate(xml_path, xsd_path)

def validate(xml_path: str, xsd_path: str) -> bool:
    print("xml_path:", xml_path)
    print("xsd_path:", xsd_path)

    #xmlschema_doc = etree.parse(xsd_path)
    #xmlschema = etree.XMLSchema(xmlschema_doc)
    #xml_doc = etree.parse(xml_path)
    #result = xmlschema.validate(xml_doc)

    return "result"

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


def __validate_files_in_filesys(current_domain):
    file_2_display = "generate-src-rivtabp21.bat"   # OK
    file_2_display = "crm_requeststatus_2.0.xsd"    # OK
    #file_2_display = "AB_crm_requeststatus.docx"    #read(): UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa1 in position 15: invalid start byte
    file_2_display = "GetRequestActivitiesInteraction_2.0_RIVTABP21.wsdl"   # OK
    file_2_display = "GetRequestActivitiesResponder_2.0.xsd"   # OK
    #file_2_display = "/riv.clinicalprocess.healthcond.description/schemas/core_components/clinicalprocess_healthcond_description_2.1.xsd"
    #file_2_display = "/riv.clinicalprocess.healthcond.description/schemas/core_components/itintegration_registry_1.0.xsd"
    global dir
    home_fs = open_fs(dir)

    display_file_contents = False
    file_in_dir = False
    filter = "*"    # *     *.xsd   *.doc

    print("\n---Validering av innehållet i det virtuella filsystemet---")
    for path in home_fs.walk.files(filter=[filter]):
        this_dir_file = ""
        exists_in_dir = dir.exists(path)
        is_file = dir.isfile(path)
        print("  ",str(exists_in_dir) + " " + str(is_file),"(exists, isfile)",path)
        if file_2_display in path:
            file_in_dir = True
            with dir.open(path, 'r') as dir_file:
                this_dir_file = dir_file.read()
                if display_file_contents == True:
                    print("\tfilinnehåll [0:100]:" + this_dir_file[0:100])
        if "wsdl" in path or "xsd" in path:
            if this_dir_file != "":
                __validate_xml_file(this_dir_file)
    if file_in_dir == False:
        print("\nSökt fil ("+file_2_display+") saknas i filsystemet!")
    print("----------------------------------------------------------")

def __validate_xml_file(xml_file):
    print("\t--- XML-validering ska göras---")
    xmlschema_doc = etree.parse(xml_file)
    #xmlschema = etree.XMLSchema(xmlschema_doc)
    #xml_doc = etree.parse(xml_file)
    #result = xmlschema.validate(xml_doc)


##### Execute test #####
if local_test == True:
    current_domain = "riv.clinicalprocess.healthcond.certificate"           # Bug: empty TK folders
    current_tag = "4.0.5"
    current_domain = "riv.clinicalprocess.activity.request"                 # OK
    current_tag = "1.0.2"
    current_domain = "riv.clinicalprocess.healthcond.basic"                 # OK
    current_tag = "1.0.10"
    current_domain = "riv.clinicalprocess.healthcond.description"           # Bug: empty TK folders
    current_tag = "2.1.16"
    current_domain = "riv.clinicalprocess.logistics.logistics"              # OK
    current_tag = "3.0.9"
    current_domain = "riv.crm.requeststatus"                                # OK
    current_tag = "2.0_RC5"
    current_domain = "riv.clinicalprocess.logistics.logistics"              # OK, but should fail, because code_gen doesn't exist in the repo
    current_tag = "2.0.4_RC1"
    #current_domain = "riv.clinicalprocess.healthcond.description"
    #current_tag = "3.0_RC1"

    __build_and_load_inmemory_filesystem(current_domain, current_tag)
    __validate_files_in_filesys(current_domain)
    print("\n==================================================")
    print("2do: explore how to get repo listing for given tag")
    print("==================================================")

    #__wsdlvalidation()
    #__test_inspection_comments(globals.TKB,"REF-LINKS",404)

    global dir
    dir.close()
