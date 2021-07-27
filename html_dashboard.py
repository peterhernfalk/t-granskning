import app
import globals
from repo import *

def get_page_html():
    html = __html_start() + __html_head() + __html_body_start() + __html_sidebar() + __html_overview_start(globals.domain_name, globals.tag)
    html += __html_summary_infospec() + __html_summary_TKB() + __html_section_end()

    html += __html_detail_section_begin("Infospec")
    html += __html_recent_inspection_box_begin("Infospec-granskning") + globals.IS_detail_box_contents + __html_recent_inspection_box_end()

    html += __html_br()+__html_detail_box_begin_TKB()+globals.TKB_detail_box_contents+__box_content_end()
    html += __html_section_end()+__html_br()+__html_br()+__html_body_end()+__html_end()
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
    <title> I-granskning </title>
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
      background: #081D45;
    }
    .sidebar .nav-links li a:hover{
      background: #081D45;
    }
    .sidebar .nav-links li i{
      min-width: 60px;
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
          <a href="#Infospec">
            <i></i>
            <span class="links_name">Infospec-granskning</span>
          </a>
        </li>
        <li>
          <a href="#TKB">
            <i></i>
            <span class="links_name">TKB-granskning</span>
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
        <span class="dashboard">I-granskning av: &nbsp '''
    html += domain_name + ' (' + tag + ')</span>'
    html += '''
    </div>
    </nav>
    <div class="home-content">
    <div class="overview-boxes">
    '''
    return html

def __html_summary_infospec():
    html = '''
    <ul class="recent-result box">
    <div>
    <div class="box-topic">Sammanfattning: infospec</div>
    '''
    if globals.IS_exists == True:
        html += '<div><li>' + __get_infospec_summary("revisionshistorik") + '</li></div>'
        html += '<div><li>' + __get_infospec_summary("referenslänkar") + '</li></div>'
        html += '<div><li>' + __get_infospec_summary("klassbeskrivning") + '</li></div>'
        html += '<div><li>' + __get_infospec_summary("multiplicitet") + '</li></div>'
        html += '<div><li>' + __get_infospec_summary("datatyper") + '</li></div>'
        html += '<div><li>' + __get_infospec_summary("referensinfomodell") + '</li></div>'
        html += '<div><li>' + __get_infospec_summary("tabellcellinnehåll") + '</li></div>'
    else:
        #html = globals.IS_felmeddelande
        #html += "<br><i><b>Infospec saknas.</b> <br>Här ska det kompletteras med information som kan underlätta för granskaren.</i>"
        html += __text_document_not_found(globals.IS, globals.domain_name, globals.tag)
    html += '''
    </div>
    </ul>
    '''
    return html

def __text_document_not_found(doc, domain, tag):

    """
    Sammanställer ett meddelande till användaren då sökt dokument saknas eller då fel dokumentnamn har angivits.

    Returenar: information i html-format
    """
    document_name = "Infospec"
    if doc == globals.TKB:
        document_name = globals.TKB

    document_info = globals.HTML_2_SPACES
    document_info += document_name + " saknas eller har annat namn än det förväntade: <i><br>" + globals.HTML_2_SPACES+globals.HTML_2_SPACES + doc.upper() + "_" + domain.replace(".", "_") + ".docx</i>"
    docs_link = REPO_get_domain_docs_link(domain, tag)
    document_info += "<br><br>" + globals.HTML_2_SPACES + "Kontrollera dokumentnamn här: <a href='" + docs_link + "'" + " target='_blank'>" + docs_link + "</a>"
    document_info += "<br><br>" + globals.HTML_2_SPACES + "Om det finns en " + document_name + " så har den ett annat än det förväntade namnet. "
    if doc == globals.IS:
        document_info += "<br>" + globals.HTML_2_SPACES + "I så fall kan du ange det namnet som en url-parameter enligt: <br>" + globals.HTML_2_SPACES + globals.HTML_2_SPACES + "<i>url...</i><b>&is=dokumentnamn</b>"
        document_info += "<br>" + globals.HTML_2_SPACES + "Om detta är en applikationsspecifik domän kan du ange det i en url-parameter: <br>" + globals.HTML_2_SPACES+globals.HTML_2_SPACES + "<i>url...</i><b>&domainprefix=true</b>"

    return document_info


def __get_infospec_summary(topic):
    html = ""
    if topic == "revisionshistorik":
        if globals.IS_antal_brister_revisionshistorik == 0:
            html += "Revisionshistoriken är <b>korrekt</b>"
        else:
            html += "<b>Fel versionsnummer</b> angivet i revisionshistoriken"
    elif topic == "referenslänkar":
        html += "<b>" + str(globals.IS_antal_brister_referenslänkar) + " &nbsp</b>felaktiga länkar i referenstabellen"
    elif topic == "klassbeskrivning":
        html += "<b>" + str(globals.IS_antal_brister_klassbeskrivning) + " &nbsp</b>saknade klassbeskrivningar"
    elif topic == "multiplicitet":
        html += "<b>" + str(globals.IS_antal_brister_multiplicitet) + " &nbsp</b>saknade multipliciteter i klasstabeller"
    elif topic == "datatyper":
        html += "<b>" + str(globals.IS_antal_brister_datatyper) + " &nbsp</b>odefinierade datatyper"
    elif topic == "referensinfomodell":
        html += "<b>" + str(globals.IS_antal_brister_referensinfomodell) + " &nbsp</b>saknade referenser till RIM i klasstabeller"
    elif topic == "tabellcellinnehåll":
        html += "<b>" + str(globals.IS_antal_brister_tomma_tabellceller) + " &nbsp</b>tomma celler i klasstabeller"
    return html

def __html_summary_TKB():
    html = '''
    <ul class="recent-result box">
    <div>
    <div class="box-topic">Sammanfattning: TKB</div>
    '''

    #html += "<div><li>" + __get_TKB_summary() + "</li></div>"
    if globals.TKB_exists == True:
        html += __get_TKB_summary()
    else:
        html += __text_document_not_found(globals.TKB, globals.domain_name, globals.tag)

    html += '''
    </div>
    </ul>
    </div>
    '''
    return html

def __get_TKB_summary():
    html = ""
    if globals.TKB_antal_brister_revisionshistorik == 0:
        html += "<div><li>Revisionshistoriken är <b>korrekt</b></li></div>"
    else:
        html += "<div><li><b>Fel versionsnummer</b> angivet i revisionshistoriken</li></div>"
    html += "<div><li><b>" + str(globals.TKB_antal_brister_referenslänkar) + " &nbsp</b>felaktiga länkar i referenstabellen</li></div>"

    return html

def __html_section_end():
    html = "</section>"
    return html

def __html_detail_section_begin(id):
    if id.strip() != "":
        html = '''
        <section id="'''+id+'''" class="home-section">
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
        <div class="title">'''+title+'''</div>
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

def __demo_add_box_content_IS():
    html = '''
      <li><b>Krav:</b> om dokumentegenskaper finns ska version och ändringsdatum stämma överens med granskad version</li>
      <br>
      <li><b>Krav:</b> revisionshistoriken ska vara uppdaterad för samma version som domänen</li>
      <li><b>Granskningsstöd:</b> om revisionshistoriken inte är uppdaterad, kontakta beställaren eller skriv en granskningskommentar</li>
      <li><b>Resultat:</b> Revisionshistoriken är uppdaterad för denna version av domänen</li>
      <li>Revisionshistorikens sista rad: ('4.0.5', '2020-01-17', 'Peter Hernfalk', 'Ändrat versionsnummer till 4.0.5')</li>
      <br>
      <li><b>Krav:</b> länkarna i referenstabellen ska fungera</li>
      <li><b>OK</b> (statuskod: 301) för: <a href="http://rivta.se/" target="_blank"">http://rivta.se/</a></li>
      <li><b>OK</b> (statuskod: 302) för: http://informationsstruktur.socialstyrelsen.se/</li>
      <li><b>OK</b> (statuskod: 200) för: https://inera.atlassian.net/wiki/spaces/KINT/pages/3615655/Kodverk+i+nationella+tj+nstekontrakt</li>
      <li><b>OK</b> (statuskod: 301) för: http://termbank.socialstyrelsen.se/</li>
      <li><b>OK</b> (statuskod: 302) för: http://www.rivta.se/domains/clinicalprocess_healthcond_certificate.html</li>
      <li><b>OK</b> (statuskod: 200) för: https://inera.atlassian.net/wiki/spaces/EIT/overview</li>
      <li><b>OK</b> (statuskod: 307) för: http://www.rikstermbanken.se/mainMenu.html</li>
      <li><b>OK</b> (statuskod: 200) för: https://www.sis.se/produkter/informationsteknik-kontorsutrustning/ittillampningar/halso-och-sjukvardsinformatik/sseniso139402016/</li>
      <li><b>OK</b> (statuskod: 200) för: https://www.sis.se/produkter/informationsteknik-kontorsutrustning/ittillampningar/halso-och-sjukvardsinformatik/sseniso210902011/</li>
      <br>
      <li><b>Krav:</b> infomodellklasserna ska komma i alfabetisk ordning </li>
      <li><b>Krav:</b> infomodellklassernas rubriker ska börja med stor bokstav </li>
      <li><b>Kontroll</b> att infomodellklassernas rubriker är i alfabetisk ordning och börjar med stor bokstav </li>
      <li>&nbsp&nbsp 8 Klasser och attribut </li>
      <li>&nbsp&nbsp 8.1 Avsändare av meddelande </li>
      <li>&nbsp&nbsp 8.2 Delfråga </li>
      <li>&nbsp&nbsp 8.3 Delsvar </li>
      <li>&nbsp&nbsp 8.4 Enhet: Organisation </li>
      <li>&nbsp&nbsp 8.5 Fråga </li>
      <li>&nbsp&nbsp 8.6 HoS-personal: Hälso och sjukvårdspersonal </li>
      <li>&nbsp&nbsp 8.7 Händelse </li>
      <li>&nbsp&nbsp 8.8 Intygsmottagare: Organisation </li>
      <li>&nbsp&nbsp 8.9 Intyg: Dokument (inom hälso- och sjukvård) </li>
      <li>&nbsp&nbsp 8.10 Kompletteringsfråga </li>
      <li>&nbsp&nbsp 8.11 Makulering </li>
      <li>&nbsp&nbsp 8.12 Meddelande </li>
      <li>&nbsp&nbsp 8.13 Metadata </li>
      <li>&nbsp&nbsp 8.14 Mottagare av meddelande </li>
      <li>&nbsp&nbsp 8.15 Part </li>
      <li>&nbsp&nbsp 8.16 Patient: Person </li>
      <li>&nbsp&nbsp 8.17 Referens </li>
      <li>&nbsp&nbsp 8.18 Relation </li>
      <li>&nbsp&nbsp 8.19 Sjukfall </li>
      <li>&nbsp&nbsp 8.20 Status </li>
      <li>&nbsp&nbsp 8.21 Svar </li>
      <li>&nbsp&nbsp 8.22 Vårdgivare: Organisation </li>
      <li>&nbsp&nbsp 8.23 Ärenden </li>
      <li><b>Resultat: </b>för närvarande sker kontrollen manuellt, med ovanstående listning som underlag </li>
    '''
    return html

def __demo_add_box_content_TKB():
    html = '''
        <li><b>Krav:</b> om dokumentegenskaper finns ska version och ändringsdatum stämma överens med granskad version</li>
        <br>
        <li><b>Krav:</b> revisionshistoriken ska vara uppdaterad för samma version som domänen</li>
        <li><b>Resultat:</b> Revisionshistoriken är uppdaterad för denna version av domänen</li>
        <li>Revisionshistorikens sista rad: ('4.0.5', '', '2020-01-17', 'Uppdaterat versionsnummer till 4.0.5
        <br>Lagt till attributet hanteratAv i den gemensamma
        klassen Handelse.
        <br>Uppdaterat versionsnummer för ListCertificatesForCareWithQA till 3.3 eftersom den ska använda det nya Händelsefältet. \nUppdaterat tabell för kompatibilitet.', 'Peter Hernfalk', '')</li>
    '''
    return html

def __box_content_end():
    html = '''
    </ul>
    </div>
    </div>
    '''
    return html

get_page_html()