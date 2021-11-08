#import app
#import globals
import granskning_AB
import granskning_TKB
import repo
from repo import *

AB_antal_brister = 0
TKB_antal_brister = 0


def get_page_html():
    global AB_antal_brister
    AB_antal_brister = 0
    global IS_antal_brister
    IS_antal_brister = 0
    global TKB_antal_brister
    TKB_antal_brister = 0

    html = __html_start() + __html_head() + __html_body_start() + __html_sidebar() + __html_overview_start(globals.domain_name, globals.tag)
    html += __html_summary_documents() + __html_summary_SCHEMAS() + __html_section_end()

    html += __html_detail_section_begin("TKB")

    html += __html_detail_box_begin_TKB() + granskning_TKB.TKB_detail_box_contents + __box_content_end()

    html += __html_br() + __html_detail_box_begin_AB() + granskning_AB.AB_detail_box_contents + __box_content_end()

    html += __html_br() + __html_detail_box_begin_RIVTA() + globals.RIVTA_detail_box_contents + __box_content_end()

    html += __html_br() + __html_detail_box_begin_XML() + globals.XML_detail_box_contents + __box_content_end()

    html += __html_br() + __html_detail_box_begin_COMPATIBILITY() + globals.COMPATIBILITY_detail_box_contents + __box_content_end()

    if globals.REPOINFO_detail_box_contents == "":
        globals.REPOINFO_detail_box_contents += "<br>Commit-id: " + globals.head_hash
    repo.REPO_get_domain_docs_link(globals.domain_name,globals.tag)
    html += __html_br() + __html_detail_box_begin_REPOINFO() + globals.REPOINFO_detail_box_contents + __box_content_end()

    globals.COMMENTS_detail_box_contents = "Här ska förslag till granskningskommentarer visas, inklusive färgkodning och i samma struktur som granskningsrapporten"
    html += __html_br() + __html_detail_box_begin_COMMENTS() + globals.COMMENTS_detail_box_contents + __box_content_end()

    html += __html_section_end() + __html_br() + __html_br()
    html += __html_body_end() + __html_end()
    return html


def __html_start():
    html = '''
    <!DOCTYPE html>
    <html lang="en" dir="ltr">
    '''
    return html


def __html_end():
    html = '''
    </html>
    '''
    return html


def __html_head():
    html = '''
    <head>
    <meta charset="UTF-8">
    <title> T-granskning </title>
    '''
    html += __html_style()
    html += '''
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    '''
    return html


def __html_style():
    html = '''
    <style>
    /* Googlefont Poppins CDN Link */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600;700&display=swap');
    *{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Poppins', sans-serif;
    }

    .sidebar{
      position: fixed;
      height: 100%;
      width: 240px;
      background: gray;  //#0A2558;
      transition: all 0.5s ease;
    }
    .sidebar.active{
      width: 60px;
    }
    .sidebar .nav-links{
      margin-top: 10px;
    }
    .sidebar .nav-links li{
      position: relative;
      list-style: none;
      height: 50px;
    }
    .sidebar .nav-links li a{
      height: 100%;
      width: 100%;
      display: flex;
      align-items: center;
      text-decoration: none;
      transition: all 0.4s ease;
    }
    .sidebar .nav-links li a.active{
      //background: #081D45;
      background: #505050;
    }
    .sidebar .nav-links li a:hover{
      background: #081D45;
    }
    .sidebar .nav-links li i{
      //min-width: 60px;
      padding-left: 20px;
      text-align: center;
      font-size: 18px;
      color: #fff;
    }
    .sidebar .nav-links li a .links_name{
      color: #fff;
      font-size: 15px;
      font-weight: 400;
      white-space: nowrap;
    }
    .sidebar .nav-links .log_out{
      position: absolute;
      bottom: 0;
      width: 100%;
    }
    .sidebar .logo-details{
      height: 80px;
      display: flex;
      align-items: center;
    }
    .sidebar .logo-details i{
      font-size: 28px;
      font-weight: 500;
      color: #fff;
      min-width: 60px;
      text-align: center
    }
    .sidebar .logo-details .logo_name{
      color: #fff;
      font-size: 24px;
      font-weight: 500;
    }
    .home-section{
      position: relative;
      background: #f5f5f5;
      min-height: 30vh;  //100vh;
      width: calc(100% - 240px);
      left: 240px;
      transition: all 0.5s ease;
    }
    .home-section nav .sidebar-button{
      display: flex;
      align-items: center;
      font-size: 24px;
      font-weight: 500;
    }
    nav .sidebar-button i{
      font-size: 35px;
      margin-right: 10px;
    }
    .home-section .home-content{
      position: relative;
      padding-top: 40px;
    }
    .home-content .overview-boxes{
      display: flex;
      //align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      padding: 0 20px;
      //margin-bottom: 26px;
    }
    .overview-boxes .box{
      display: flex;
      //align-items: center;
      justify-content: center;
      width: calc(100% / 2 - 55px);
      background: #fff;
      padding: 15px 14px;
      border-radius: 12px;
      box-shadow: 0 5px 10px rgba(0,0,0,0.1);
    }
    .overview-boxes .box-topic{
      font-size: 20px;
      font-weight: 500;
    }
    .overview-boxes .box-topic-large{
      font-size: 30px;
      font-weight: 500;
    }
    /* left box */
    .home-content .detail-boxes .recent-inspection{
      width: 97%;
      background: #fff;
      padding: 20px 30px;
      margin: 0 20px;
      border-radius: 12px;
      box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
    }
    .detail-boxes .box .title{
      font-size: 24px;
      font-weight: 500;
      /* margin-bottom: 10px; */
    }
    .detail-boxes .inspection-details li{
      list-style: none;
      margin: 8px 0;
    }

    /* Responsive Media Query */
    @media (max-width: 1240px) {
      .sidebar{
        width: 60px;
      }
      .sidebar.active{
        width: 220px;
      }
      .home-section{
        width: calc(100% - 60px);
        left: 60px;
      }
      .sidebar.active ~ .home-section{
        /* width: calc(100% - 220px); */
        overflow: hidden;
        left: 220px;
      }
      .home-section nav{
        width: calc(100% - 60px);
        left: 60px;
      }
      .sidebar.active ~ .home-section nav{
        width: calc(100% - 220px);
        left: 220px;
      }
    }
    @media (max-width: 1150px) {
      .home-content .inspection-boxes{
        flex-direction: column;
      }
      .home-content .inspection-boxes .box{
        width: 100%;
        overflow-x: scroll;
        margin-bottom: 30px;
      }
      .home-content .inspection-boxes{
        margin: 0;
      }
    }
    @media (max-width: 1000px) {
      .overview-boxes .box{
        width: calc(100% / 2 - 15px);
        margin-bottom: 15px;
      }
    }
    @media (max-width: 700px) {
      nav .sidebar-button .dashboard,
      nav .profile-details .admin_name,
      nav .profile-details i{
        display: none;
      }
      .home-section nav .profile-details{
        height: 50px;
        min-width: 40px;
      }
      .home-content .inspection-boxes .inspection-details{
        width: 560px;
      }
    }
    @media (max-width: 550px) {
      .overview-boxes .box{
        width: 100%;
        margin-bottom: 15px;
      }
      .sidebar.active ~ .home-section nav .profile-details{
        display: none;
      }
    }
    </style>
    '''
    return html


def __html_br():
    html = '''
    <br>
    '''
    return html


def __html_body_start():
    html = '''
    <body>
    '''
    return html


def __html_body_end():
    html = '''
    </body>
    '''
    return html


def __html_sidebar():
    html = '''
      <div class="sidebar">
      <ul class="nav-links">
        <li>
          <a href="#" class="active">
            <i></i>
            <span class="links_name"><b>Innehåll</b></span>
          </a>
        </li>
        <li>
          <a href="#TKB">
            <i></i>
            <span class="links_name">TKB-granskning</span>
          </a>
        </li>
        <li>
          <a href="#AB">
            <i></i>
            <span class="links_name">AB-granskning</span>
          </a>
        </li>
        <li>
          <a href="#RIVTA">
            <i></i>
            <span class="links_name">RIVTA-verifiering</span>
          </a>
        </li>
        <li>
          <a href="#XML">
            <i></i>
            <span class="links_name">XML-validering</span>
          </a>
        </li>
        <li>
          <a href="#COMPATIBILITY">
            <i></i>
            <span class="links_name">Kompatibilitet</span>
          </a>
        </li>
        <li>
          <a href="#REPOINFO">
            <i></i>
            <span class="links_name">Repo-information</span>
          </a>
        </li>
        <li>
          <a href="#Comments">
            <i></i>
            <span class="links_name">Granskningskommentarer</span>
          </a>
        </li>
        </div>
    '''
    return html


def __html_overview_start(domain_name, tag):
    html = '''
      <section class="home-section">
    <nav>
      <div class="sidebar-button">
        <i></i>
        <span class="dashboard">T-granskning av: &nbsp '''
    html += domain_name + ' (' + tag + ')</span>'
    html += '''
    </div>
    </nav>
    <div class="home-content">
    <div class="overview-boxes">
    '''
    return html


def __html_summary_documents():
    html = '''
    <ul class="recent-result box">
    <div>
    '''

    html += '''
        <div class="box-topic-large">Dokumentgranskning:</div>
    '''

    html += '''
        <div class="box-topic">Sammanfattning: TKB</div>
    '''
    if granskning_TKB.TKB_exists == True:
        html += __get_TKB_summary()
    else:
        html += __text_document_not_found(globals.TKB, globals.domain_name, globals.tag)

    html += '''
        <br><div class="box-topic">Sammanfattning: AB</div>
    '''

    if granskning_AB.AB_exists == True:
        html += __get_AB_summary()
    else:
        html += __text_document_not_found(globals.AB, globals.domain_name, globals.tag)


    html += '''
    </div>
    </ul>
    '''
    return html


def __html_summary_SCHEMAS():
    html = '''
    <ul class="recent-result box">
    <div>
    <div class="box-topic-large">Interaktions- och schemafiler:</div>
    '''

    html += '''
        <div class="box-topic">Sammanfattning: RIVTA-verifiering</div>
    '''
    html += "<div><li><i>Exempel på hur det kan se ut när detta är implementerat</i></li></div>"
    html += "<div><li>There were <b>0</b> errors and <b>0</b> warnings.</li></div>"

    html += '''
        <br><div class="box-topic">Sammanfattning: XML-validering</div>
    '''
    html += "<div><li><i>Exempel på hur det kan se ut när detta är implementerat</i></li></div>"
    html += "<div><li><b>Valid</b> WSDL</li></div>"

    html += '''
        <br><div class="box-topic">Sammanfattning: versionskompatibilitet</div>
    '''
    html += "<div><li><i>Exempel på hur det kan se ut när detta är implementerat</i></li></div>"
    html += "<div><li>Denna domänversion är <b>kompatibel</b> med förra domänversionen</li></div>"

    html += '''
        <br><div class="box-topic-large">Konfigurationsstyrning:</div>
        <div><li><i>Exempel på hur det kan se ut när detta är implementerat</i></li></div>
        <div><li><b>Alla  &nbsp</b>obligatoriska kataloger och filer finns i domänen</div></li>
    '''

    html += '''
        <br><div class="box-topic-large">Granskningskommentarer:</div>
        <div><li><i>Exempel på hur det kan se ut när detta är implementerat</i></li></div>
        <div><li><b>0  &nbsp</b>förslag till granskningskommentarer</div></li>
    '''


    html += '''
    </div>
    </ul>
    </div>
    '''
    return html

def __text_document_not_found(doc, domain, tag):
    """
    Sammanställer ett meddelande till användaren då sökt dokument saknas eller då fel dokumentnamn har angivits.

    Returenar: information i html-format
    """
    document_name = doc

    document_info = globals.HTML_2_SPACES
    document_info += document_name + " saknas eller har annat namn än det förväntade: <i><br>" + globals.HTML_2_SPACES + globals.HTML_2_SPACES + doc.upper() + "_" + domain.replace(
        ".", "_") + ".docx</i>"
    docs_link = REPO_get_domain_docs_link(domain, tag)
    document_info += "<br><br>" + globals.HTML_2_SPACES + "Kontrollera dokumentnamn här: <a href='" + docs_link + "'" + " target='_blank'>" + docs_link + "</a>"
    document_info += "<br><br>" + globals.HTML_2_SPACES + "Om det finns en " + document_name + " så har den ett annat än det förväntade namnet. "
    if doc == globals.IS:
        document_info += "<br>" + globals.HTML_2_SPACES + "I så fall kan du ange det namnet som en url-parameter enligt: <br>" + globals.HTML_2_SPACES + globals.HTML_2_SPACES + "<i>url...</i><b>&is=dokumentnamn</b>"
        document_info += "<br>" + globals.HTML_2_SPACES + "Om detta är en applikationsspecifik domän kan du ange det i en url-parameter: <br>" + globals.HTML_2_SPACES + globals.HTML_2_SPACES + "<i>url...</i><b>&domainprefix=true</b>"

    return document_info


def __html_summary_TKB():
    html = '''
    <ul class="recent-result box">
    <div>
    <div class="box-topic">Sammanfattning: TKB</div>
    '''

    # html += "<div><li>" + __get_TKB_summary() + "</li></div>"
    if globals.TKB_exists == True:
        html += __get_TKB_summary()
    else:
        html += __text_document_not_found(globals.TKB, globals.domain_name, globals.tag)

    html += '''
        <br><div class="box-topic">Sammanfattning: AB</div>
    '''
    html += __get_AB_summary()

    html += '''
    </div>
    </ul>
    </div>
    '''
    return html


def __get_TKB_summary():
    global TKB_antal_brister
    html = ""
    if granskning_TKB.TKB_antal_brister_revisionshistorik == 0:
        html += "<div><li>Revisionshistoriken har <b>korrekt</b> version angiven</li></div>"
    else:
        html += "<div><li><b>Fel versionsnummer</b> angivet i revisionshistoriken</li></div>"
        TKB_antal_brister += 1
    html += "<div><li><b>" + str(
        granskning_TKB.TKB_antal_brister_tomma_revisionshistoriktabellceller) + " &nbsp;</b>tomma celler i revisionshistoriken</li></div>"
    TKB_antal_brister += granskning_TKB.TKB_antal_brister_tomma_revisionshistoriktabellceller
    html += "<br>"
    html += "<div><li><b>" + str(
        granskning_TKB.TKB_antal_brister_referenslänkar) + " &nbsp;</b>felaktiga länkar i referenstabellen</li></div>"
    TKB_antal_brister += granskning_TKB.TKB_antal_brister_referenslänkar
    html += "<div><li><b>" + str(
        granskning_TKB.TKB_antal_brister_tomma_referenstabellceller) + " &nbsp;</b>tomma celler i referenstabellen</li></div>"
    TKB_antal_brister += granskning_TKB.TKB_antal_brister_tomma_referenstabellceller
    html += "<br>"
    if granskning_TKB.TKB_meddelandemodeller_finns == True:
        html += "<div><li>Meddelandemodeller <b>finns</b></li></div>"
    else:
        html += "<div><li>Meddelandemodeller <b>saknas</b></li></div>"
        TKB_antal_brister += 1
    html += "<br>"
    html += "<b>" + str(TKB_antal_brister) + " &nbsp;brister i TKB</b> upptäckta av automatiserad granskning<br>"

    return html


def __html_summary_AB():
    html = '''
    <ul class="recent-result box">
    <div>
    <div class="box-topic">Sammanfattning: AB</div>
    '''

    html += __get_AB_summary()
    """if globals.TKB_exists == True:
        html += __get_TKB_summary()
    else:
        html += __text_document_not_found(globals.TKB, globals.domain_name, globals.tag)"""

    html += '''
    </div>
    </ul>
    </div>
    '''
    return html


def __get_AB_summary():
    global AB_antal_brister
    html = ""
    if granskning_AB.AB_antal_brister_revisionshistorik == 0:
        html += "<div><li>Revisionshistoriken har <b>korrekt</b> version angiven</li></div>"
    else:
        html += "<div><li><b>Fel versionsnummer</b> angivet i revisionshistoriken</li></div>"
        AB_antal_brister += 1
    html += "<div><li><b>" + str(granskning_AB.AB_antal_brister_tomma_revisionshistoriktabellceller) + " &nbsp;</b>tomma celler i revisionshistoriken</li></div>"
    AB_antal_brister += granskning_AB.AB_antal_brister_tomma_revisionshistoriktabellceller

    html += "<div><li><b>" + str(granskning_AB.AB_antal_brister_referenslänkar) + " &nbsp;</b>felaktiga länkar i referenstabellen</li></div>"
    AB_antal_brister += granskning_AB.AB_antal_brister_referenslänkar

    html += "<div><li><b>" + str(granskning_AB.AB_antal_brister_tomma_referenstabellceller) + " &nbsp;</b>tomma celler i referenstabellen</li></div>"
    AB_antal_brister += granskning_AB.AB_antal_brister_tomma_referenstabellceller
    html += "<br><b>" + str(AB_antal_brister) + " &nbsp;brister i AB</b> upptäckta av automatiserad granskning<br>"

    return html


def __html_section_end():
    html = "</section>"
    return html


def __html_detail_section_begin(id):
    if id.strip() != "":
        html = '''
        <section id="''' + id + '''" class="home-section">
        <div class="home-content">
          <div class="detail-boxes">
        '''
    else:
        html = '''
        <section class="home-section">
        <div class="home-content">
          <div class="detail-boxes">
        '''
    return html


def __html_section_end():
    html = '''
    </section>
    '''
    return html


def __html_recent_inspection_box_begin(title):
    html = ""
    if title.strip() != "":
        html = '''
        <div class="recent-inspection box">
        <div class="title">''' + title + '''</div>
        <div class="inspection-details">
        <ul class="details">
        <li class="topic">
        '''
    return html


def __html_recent_inspection_box_end():
    html = '''
    </ul>
    </div>
    </div>
    </div>
    '''
    return html


def __html_detail_box_begin_TKB():
    html = '''
    <div id = "TKB" class="detail-boxes">
	<div class="recent-inspection box">
    <div class="title">TKB-granskning</div>
    <div class="inspection-details">
    <ul class="details">
    '''
    return html


def __html_detail_box_begin_AB():
    html = '''
    <div id = "AB" class="detail-boxes">
	<div class="recent-inspection box">
    <div class="title">AB-granskning</div>
    <div class="inspection-details">
    <ul class="details">
    '''
    return html


def __html_detail_box_begin_RIVTA():
    html = '''
    <div id = "RIVTA" class="detail-boxes">
	<div class="recent-inspection box">
    <div class="title">RIVTA-verifiering</div>
    <div class="inspection-details">
    <ul class="details">
    '''
    return html


def __html_detail_box_begin_XML():
    html = '''
    <div id = "XML" class="detail-boxes">
	<div class="recent-inspection box">
    <div class="title">XML-validering</div>
    <div class="inspection-details">
    <ul class="details">
    '''
    return html

def __html_detail_box_begin_COMPATIBILITY():
    html = '''
    <div id = "COMPATIBILITY" class="detail-boxes">
	<div class="recent-inspection box">
    <div class="title">Versionskompatibilitet</div>
    <div class="inspection-details">
    <ul class="details">
    '''
    return html


def __html_detail_box_begin_REPOINFO():
    html = '''
    <div id = "REPOINFO" class="detail-boxes">
	<div class="recent-inspection box">
    <div class="title">Repo-information</div>
    <div class="inspection-details">
    <ul class="details">
    '''
    return html

def __html_detail_box_begin_COMMENTS():
    html = '''
    <div id = "Comments" class="detail-boxes">
	<div class="recent-inspection box">
    <div class="title">Förslag till granskningskommentarer</div>
    <div class="inspection-details">
    <ul class="details">
    '''
    return html


def __box_content_end():
    html = '''
    </ul>
    </div>
    </div>
    '''
    return html
