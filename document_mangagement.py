from docx import Document
import globals
import io
import requests

def DOC_get_document_page_link(domainname, tag, document):
    """
    Beräknar url till sidan som innehåller länk till angivet dokument för vald domän och tag i Bitbucket-repot.

    Returnerar: länk till dokumentsidan
    """
    url_prefix = "https://bitbucket.org/rivta-domains/"
    url_domain = globals.domain_prefix + domainname + "/"
    url_src = "src/"
    url_tag = tag + "/"
    url_docs = "docs/"
    domain_name = domainname.replace(".","_")
    url_doc = document +"_" + domain_name + ".docx"
    document_page_link = url_prefix+url_domain+url_src+url_tag+url_docs+url_doc

    return document_page_link

def DOC_get_document_link(domainname, tag, document, head_hash, alt_document_name):
    """
    Beräknar url till angivet dokument för vald domän och tag i Bitbucket-repot.

    Returnerar: länk som kan användas vid nerladdning av angivet dokument
    """
    url_prefix = "https://bitbucket.org/rivta-domains/"
    url_domain = globals.domain_prefix + domainname + "/"
    url_raw = "raw/"
    url_docs = "docs/"
    domain_name = domainname.replace(".","_")
    if len(alt_document_name.strip()) > 0:
        url_doc = alt_document_name
    else:
        url_doc = document +"_" + domain_name + ".docx"
    document_link = url_prefix+url_domain+url_raw+head_hash+"/"+url_docs+url_doc

    if document == globals.IS:
        globals.IS_document_name = url_doc
    elif document == globals.TKB:
        globals.TKB_document_name = url_doc

    return document_link


def DOC_get_downloaded_document(document_link):
    """
    Laddar ner dokument från angiven länk.

    Returnerar: nerladdat dokument
    """
    downloaded_doc = requests.get(document_link, stream=True)

    return downloaded_doc

def DOC_get_head_hash(document_page):
    """
    hämtar head-hash för det dokument som ska laddas ner. Hashen finns i den Bitbucketsida som innehåller länk till dokumentet.

    Returnerar: head-hash
    """
    hash_start = document_page.text.find('{"hash":')
    hash_end = hash_start+17
    head_hash = document_page.text[hash_start+10:hash_end]

    return head_hash

def DOC_get_docx_document(downloaded_document):
    """
    Läser in angivet dokuments innehåll i ett docx-Document.

    Returnerar: docx-Documentet
    """
    with io.BytesIO(downloaded_document.content) as inmemoryfile:
        docx_document = Document(inmemoryfile)

    return docx_document