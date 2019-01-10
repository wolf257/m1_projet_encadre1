#!/usr/bin/env python3
# -*- coding : utf8 -*-

import os
import io
import re
import urllib

try:
    import requests
except ImportError:
    print("No module named 'requests' found.\n Run 'pip3 install requests'.")

try:
    import inscriptis
except ImportError:
    print("No module named 'inscriptis' found.\n Run 'pip3 install inscriptis'.")

try:
    import bs4
except ImportError:
    print("No module named 'bs4' found.\n Run 'pip3 install bs4'.")

try:
    import googlesearch as google
except ImportError:
    print("No module named 'googlesearch' found.\n Can you run 'pip3 install google' please.")


# import modules.l1_big_process as bp
# from modules.regexp import findAndExtract_pattern_in_txt
import modules.regexp as myregexp

# Lien vers les dossiers de la racine ############################################
from settings import PROJECT_ROOT, OUTPUT_ROOT
from settings import CONTEXTES_TXT, CONTEXTES_HTML, DUMP_TEXT, IMAGES, PAGES_ASPIREES, TABLEAUX, URLS

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
###################################################################################


# GOOD
def extract_Urls_fromGoogleQuery_toFile(query, file, abbr_langue):
    """
    # Install : pip3 install google
    # Import : import googlesearch as google
    # syn : google.search(query, tld='com', lang='en', num=10, start=0, stop=None, pause=2)
    # * query : query string that we want to search for.
    # * tld : top level domain : google.(com|fr|...).
    # * lang : language : (fr|en|...).
    # * num : Number of results we want.
    # * start : First result to retrieve.
    # * stop : Last result to retrieve. None to keep searching.
    # * pause : Lapse between HTTP requests. Lapse too short may cause Google to block your IP.
    """

    query += '&tbm=nws'

    with open(file, mode='w', encoding="utf8") as fileout:
        if abbr_langue == 'fr':
            results = google.search(query, tld="fr", lang='fr', num=100, stop=100, pause=10)
        elif abbr_langue == 'en':
            results = google.search(query, tld="com", lang='en', num=100, stop=100, pause=10)

        for link in results:

            print(f"*** Nouveau lien : {link}.")

            if link.endswith('.pdf'):
                continue
            else:
                fileout.write(f"{link}\n")
                print(f"--------> ajouté")


# GOOD
def aspireOrDump_Page_toFile(todo, url, entreeEltDansDico, ficout, dicoInfos):

    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webbyte = urllib.request.urlopen(req)

    charset = webbyte.info().get_content_charset()
    entreeEltDansDico['charset_initial'] = charset

    code = webbyte.getcode()
    entreeEltDansDico['code'] = code

    webpage = webbyte.read().decode(charset)

    if todo == 'dump':
        content_text = inscriptis.get_text(webpage)
        # delete pending whitespace
        content_text = re.sub(" +", ' ', content_text).strip()

    with open(ficout, mode='w', encoding="utf8") as fileout:
        if todo == 'aspirer':
            fileout.write(webpage)
        elif todo == 'dump':
            fileout.write(content_text)


# GOOD
def aspireOrDump_listUrlsInFile_toOneFileEach(todo, ficin, folder, langue, numero_dossier,
                                              dicoInfos, patternforRegexp):

    racineDesElementsDansDicoInfos = dicoInfos[numero_dossier]['contenu_dossier']
    id_elt = 0

    if todo == 'aspirer':
        print(f"\nAspiration :")
    else:
        print(f"\nDumping :")

    with open(ficin, mode='r', encoding="utf8") as filein:
        first50lines = filein.readlines()[0:30]

        for url in first50lines:
            # print(f"\nURL en cours de traitement : {url}")

            racineDesElementsDansDicoInfos.setdefault(id_elt, {})

            # Juste pour simplifier l'écriture et éviter les erreurs,
            entreeEltDansDico = racineDesElementsDansDicoInfos[id_elt]
            entreeEltDansDico['lien_web'] = url.strip()

            if todo == 'aspirer':
                # aspiration html
                namePagetoCreateSource = f"{folder}{langue}_{numero_dossier}_{id_elt}.html"
                entreeEltDansDico['lien_aspiration'] = namePagetoCreateSource

                # contexte html
                # namePageofContext = f"{contexteFolder}{langue}_{numero_dossier}_{id_elt}.html"
                # entreeEltDansDico['lien_contexte_html'] = namePageofContext

            elif todo == 'dump':
                # dumping txt
                namePagetoCreateSource = f"{folder}{langue}_{numero_dossier}_{id_elt}.txt"
                entreeEltDansDico['lien_dumping'] = namePagetoCreateSource

                # contexte txt
                # namePageofContext = f"{contexteFolder}{langue}_{numero_dossier}_{id_elt}.txt"
                # entreeEltDansDico['lien_contexte_txt'] = namePageofContext

            try:
                aspireOrDump_Page_toFile(todo, url, entreeEltDansDico,
                                         namePagetoCreateSource, dicoInfos)

            except Exception as e:
                print(f"-", end='')

            else:
                print(f"+", end='')

                # myregexp.findAndExtract_pattern(namePagetoCreateSource, patternforRegexp,
                #                                 namePageofContext, todo)

            id_elt += 1
    print()


if __name__ == '__main__':
    print("Oups, je ne peux fonctionner seul.")
