#!/usr/bin/env python3
# -*- coding : utf8 -*-

import os
import re

import modules.myhtml as myhtml

# Lien vers les dossiers de la racine ############################################
from settings import PROJECT_ROOT

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
###################################################################################


def findAndExtract_pattern_in_fileSource(fileSourcein, pattern, fileout, todo, entreeEltDansDico):
    mypattern = re.compile(f"{pattern}", re.I)
    freqMotif = 0

    with open(fileSourcein, mode='r') as fileSourcein:

        if todo == 'html':
            # HEAD HTML
            myhtml.generate_html_head(fileout, title="Contexte")

            sautLigne = f"<br />"

        else:
            sautLigne = f"\n"

        phraseOne = f"Fichier de travail (INPUT) : {fileSourcein.name} {sautLigne}"
        phrasePattern = f"\nPattern : {pattern} {sautLigne}"
        phraseNext = f"{sautLigne}----------------------------------------{sautLigne}{sautLigne}"

        if todo == 'html':
            myhtml.append_line_to_html(fileout, phraseOne)
            myhtml.append_line_to_html(fileout, phrasePattern)
            myhtml.append_line_to_html(fileout, phraseNext)
        else:
            fileout = open(fileout, mode='a')
            fileout.write(phraseOne)
            fileout.write(phrasePattern)
            fileout.write(phraseNext)

        for i, line in enumerate(fileSourcein):
            numeroligne = i+1
            matchObj = re.search(mypattern, line)

            if matchObj:
                numeroligne = numeroligne
                freqMotif += 1

                if todo == 'html':
                    s = re.sub(mypattern,
                               f""" <span style=\"color:red;font-weight:bold;font-size:200%;\">
                                    {matchObj.group()} </span> """, line)

                    ligne = f"Ligne {numeroligne} : {s} {sautLigne}"

                    myhtml.append_line_to_html(fileout, ligne)

                elif todo == 'txt':

                    s = re.sub(mypattern, f"+++ {matchObj.group()} +++", line)
                    # print(s)
                    fileout.write(s)
                    fileout.write(f"{sautLigne}")

        if todo == 'html':
            # TAIL HTML
            myhtml.generate_html_tail(fileout)
        elif todo == 'txt':
            fileout.close()

    entreeEltDansDico['freqMotif'] = freqMotif


def contextualisation_listOfFiles_toOneFileEach(todo, folderSource, langue, numero_dossier,
                                                dicoInfos, contexteFolder, patternforRegexp):

    racineDesElementsDansDicoInfos = dicoInfos[numero_dossier]['contenu_dossier']

    if todo == 'txt':
        print(f"\nContextualisation texte :")
        extension = '.txt'
    else:
        print(f"\nContextualisation html :")
        extension = '.html'

    listeFicInFolderSource = os.listdir(folderSource)

    for fileSource in listeFicInFolderSource:
        linkToFileSource = f"{folderSource}{fileSource}"

        if not fileSource.endswith(extension):
            continue

        id_elt = int(fileSource.split('.')[0].split('_')[-1:][0])

        # Juste pour simplifier l'écriture et éviter les erreurs,
        entreeEltDansDico = racineDesElementsDansDicoInfos[id_elt]

        if todo == 'html':
            namePageofContext = f"{contexteFolder}{langue}_{numero_dossier}_{id_elt}.html"
            entreeEltDansDico['lien_contexte_html'] = namePageofContext

        elif todo == 'txt':
            namePageofContext = f"{contexteFolder}{langue}_{numero_dossier}_{id_elt}.txt"
            entreeEltDansDico['lien_contexte_txt'] = namePageofContext

        # print(f"{namePageofContext}")

        try:
            findAndExtract_pattern_in_fileSource(linkToFileSource, patternforRegexp,
                                                 namePageofContext, todo, entreeEltDansDico)

        except Exception as e:
            raise e
            print(f"-", end='')

        else:
            print(f"+", end='')


if __name__ == '__main__':
    print("Can't be use alone.")
