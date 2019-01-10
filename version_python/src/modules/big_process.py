#!/usr/bin/env python3
# -*- coding : utf8 -*-

import os
import io
import re
import urllib
import json

# from settings import PROJECT_ROOT
# from collections import defaultdict

import modules.web as myweb
import modules.myhtml as myhtml
import modules.mycss as mycss
import modules.regexp as regexp
# import regexp as regexp

# Lien vers les dossiers de la racine ############################################
from settings import PROJECT_ROOT, OUTPUT_ROOT
from settings import CONTEXTES_TXT, CONTEXTES_HTML, DUMP_TEXT, IMAGES, PAGES_ASPIREES, TABLEAUX, URLS

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
##################################################################################


def aspirationOrDumping(abbr_langue, numero_dossier,
                        motclef, query, dicoInfos, patternforRegexp):

    # TELECHARGER LE FICHIER D'URL À PARTIR D'UNE REQUETE GOOGLE (GOOD)
    googleUrlsfile = f"{URLS}{abbr_langue}_{numero_dossier}_{motclef}_urls_google.txt"
    # print(f"\t file urls : {googleUrlsfile}")
    # myweb.extract_Urls_fromGoogleQuery_toFile(query, googleUrlsfile, abbr_langue)

    # ASPIRATION DES PAGES (voir détails dans modules/myweb.py)
    aspiringfolder = PAGES_ASPIREES

    myweb.aspireOrDump_listUrlsInFile_toOneFileEach('aspirer', googleUrlsfile, aspiringfolder,
                                                    abbr_langue, numero_dossier, dicoInfos,
                                                    patternforRegexp)

    # DUMPING DES PAGES (voir détails dans modules/myweb.py) (GOOD)
    dumpingfolder = DUMP_TEXT

    myweb.aspireOrDump_listUrlsInFile_toOneFileEach('dump', googleUrlsfile, dumpingfolder,
                                                    abbr_langue, numero_dossier, dicoInfos,
                                                    patternforRegexp)


def contextualisation(abbr_langue, numero_dossier,
                      motclef, query, dicoInfos, patternforRegexp):

    aspiringfolder = PAGES_ASPIREES
    dumpingfolder = DUMP_TEXT

    # CONTEXTUALISATIONs
    contexte_html_folder = CONTEXTES_HTML
    contexte_txt_folder = CONTEXTES_TXT

    regexp.contextualisation_listOfFiles_toOneFileEach('txt', dumpingfolder,
                                                       abbr_langue, numero_dossier, dicoInfos,
                                                       contexte_txt_folder, patternforRegexp)

    regexp.contextualisation_listOfFiles_toOneFileEach('html', aspiringfolder,
                                                       abbr_langue, numero_dossier, dicoInfos,
                                                       contexte_html_folder, patternforRegexp)


# def delaRequete_auDicoResume_pourHtml(abbr_langue, numero_dossier,
#                                       motclef, query, dicoInfos, patternforRegexp):
#
#
#     # abbr_langue = abbr_langue
#     pass
#

def duDicoResume_auTableauHtml(dicoInfos):
    ficHtml = TABLEAUX+'resume.html'
    ficCss = TABLEAUX+'style.css'

    print(f"Création du fichier {ficHtml.split('/')[-1]}")

    # GENERATION CSS
    mycss.generate_css(ficCss)

    # HEAD HTML
    myhtml.generate_html_head(ficHtml, title="Tableaux synthétiques")

    for numero_dossier in dicoInfos.keys():

        # info CORPUS from dicoInfos
        langue = f"{dicoInfos[numero_dossier]['infos_dossier']['langue']}"
        requete = f"{dicoInfos[numero_dossier]['infos_dossier']['requete']}"
        pattern = f"{dicoInfos[numero_dossier]['infos_dossier']['pattern']}"

        # TITRE TABLE
        titre_table = f"Langue : {langue} - Requête : {requete} - Pattern : {pattern}"

        with open(ficHtml, mode='a') as file:
            ligne = f"<h2> {titre_table} </h2>"
            file.write(ligne)

        # OPEN TABLE
        myhtml.generate_html_table_open(ficHtml)

        # HEADERS TABLE
        listHeaders = ['id', 'URL', 'PAGE ASPIRÉE', 'CODE_HTTP', 'CHARSET_initial',
                       'DUMP_utf8', 'CONTEXTE txt', 'CONTEXTE html', 'Freq motif']

        myhtml.generate_html_table_main_row(ficHtml, listHeaders)

        # TABLE ROWS
        for id_elt in dicoInfos[numero_dossier]['contenu_dossier'].keys():
            baseEltDansDico = dicoInfos[numero_dossier]['contenu_dossier'][id_elt]

            charset_initial = baseEltDansDico.get('charset_initial', 'Null')

            if (charset_initial == 'Null') or (charset_initial is None):
                continue

            # info FILE from dicoInfos
            id_elt = id_elt
            lien_html = baseEltDansDico.get('lien_web', 'Null')
            lien_aspiration = baseEltDansDico.get('lien_aspiration', 'Null')
            code_http = baseEltDansDico.get('code', 'inconnu')
            lien_dumping = baseEltDansDico.get('lien_dumping', 'Null')
            lien_contexte_txt = baseEltDansDico.get('lien_contexte_txt', 'Null')
            lien_contexte_html = baseEltDansDico.get('lien_contexte_html', 'Null')
            freqMotif = baseEltDansDico.get('freqMotif', '0')

            # ON CONSTRUIT LES MORCEAUX HTML QUE L'ON UTILISERA
            contenant_id = f"{id_elt}"
            contenant_lien_web = f"<a target=\"_blank\" href=\"{lien_html}\"> {id_elt} </a> "
            contenant_lien_aspiration = f"<a target=\"_blank\" href=\"{lien_aspiration}\"> {id_elt}.html </a>"
            contenant_lien_dumping = f"<a target=\"_blank\" href=\"{lien_dumping}\"> {id_elt}.txt </a>"
            contenant_charset = f"{charset_initial}"
            contenant_code = f"{code_http}"
            contenant_lien_contexte_txt = f"<a target=\"_blank\" href=\" {lien_contexte_txt}\"> c_{id_elt}.txt </a>"
            contenant_lien_contexte_html = f"<a target=\"_blank\" href=\" {lien_contexte_html}\"> c_{id_elt}.html </a>"
            contenant_freq = f"{freqMotif}"

            listContent = [contenant_id, contenant_lien_web, contenant_lien_aspiration,
                           contenant_code, contenant_charset, contenant_lien_dumping,
                           contenant_lien_contexte_txt, contenant_lien_contexte_html, contenant_freq]

            myhtml.generate_html_table_other_row(ficHtml, listContent)

        # CLOSE ROWS
        myhtml.generate_html_table_close(ficHtml)

    # TAIL HTML
    myhtml.generate_html_tail(ficHtml)

    print(f"\t... {ficHtml.split('/')[-1]} terminé.")


def main():
    pass


if __name__ == '__main__':
    main()
