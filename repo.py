
import globals

def REPO_get_domain_docs_link(domainname, tag):
    """
    Beräknar url till docs-sidan för vald domän och tag i Bitbucket-repot.

    Returenar: länk till dokumentsidan
    """
    url_prefix = "https://bitbucket.org/rivta-domains/"
    url_domain = globals.domain_prefix + domainname + "/"
    url_src = "src/"
    url_tag = tag + "/"
    url_docs = "docs/"
    document_page_link = url_prefix+url_domain+url_src+url_tag+url_docs


    globals.REPOINFO_detail_box_contents += "<br>Länk till domänens Bitbucket-repo: <a href='" + url_prefix+url_domain+url_src+url_tag + "'" + " target='_blank'>" + url_prefix+url_domain+url_src+url_tag + "</a>"

    return document_page_link
