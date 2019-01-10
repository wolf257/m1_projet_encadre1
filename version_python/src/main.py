#!/usr/bin/env python3
# -*- coding : utf8 -*-

import os
# import re
# import random
import pprint
# import io
# import codecs
# import time
import pickle
import pprint

from settings import PROJECT_ROOT
from collections import defaultdict

import modules.big_process as big_process
import modules.myhtml as myhtml
import modules.others as others

# Lien vers les dossiers de la racine ############################################
from settings import PROJECT_ROOT
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
###################################################################################


def main():
    print("\nNote de version : ")
    print("\t - v1.0 : ... . \n")

    sentence = f"CHARGEMENT DES PARAMETRES INITIAUX : dicoParametresInitiaux"
    others.print_grande_etape(sentence)

    linkToFileParaInit = './datasDict/dicoParametresInitiaux'
    # remplir initialement
    dicoParametresInitiaux = {}
    dicoParametresInitiaux = others.load_dico_from_json(linkToFileParaInit, 'dicoParametres')

    dicoInfos = {}
    linkToFileDicoInfo = './datasDict/dicoInfo'

    if os.path.isfile(linkToFileDicoInfo):
        sentence = f"CHARGEMENT DU DICTIONNAIRE DE DONNEES : dicoInfo"
        others.print_grande_etape(sentence)

        print(f"Great {linkToFileDicoInfo} exists. Let's load it.")

        dicoInfos = others.load_dico_from_json(linkToFileDicoInfo, 'dicoInfo')

    else:
        sentence = f"TRAVAIL LES URLS"
        others.print_grande_etape(sentence)

        print(f"On va devoir faire le travail.")

        for abbr_langue in dicoParametresInitiaux.keys():

            for motclef in dicoParametresInitiaux[abbr_langue].keys():
                # PARAMETRE  : premier element d'identification
                numero_dossier = f"{dicoParametresInitiaux[abbr_langue][motclef]['num']}"
                langue = f"{dicoParametresInitiaux[abbr_langue][motclef]['langue']}"
                query = f"{dicoParametresInitiaux[abbr_langue][motclef]['query']}"
                patternforRegexp = f"{dicoParametresInitiaux[abbr_langue][motclef]['pattern']}"

                # dicoInfos
                dicoInfos.setdefault(numero_dossier, {})
                dicoInfos[numero_dossier].setdefault('infos_dossier', {})
                dicoInfos[numero_dossier].setdefault('contenu_dossier', {})

                dicoInfos[numero_dossier]['infos_dossier']['langue'] = langue
                dicoInfos[numero_dossier]['infos_dossier']['requete'] = query
                dicoInfos[numero_dossier]['infos_dossier']['pattern'] = patternforRegexp

                big_process.aspirationOrDumping(abbr_langue, numero_dossier,
                                                motclef, query, dicoInfos,
                                                patternforRegexp)

                big_process.contextualisation(abbr_langue, numero_dossier,
                                              motclef, query, dicoInfos, patternforRegexp)

        sentence = f"SAUVEGARDE DONNEES GÉNÉRÉES"
        others.print_grande_etape(sentence)

        others.dump_dico_to_json(linkToFileDicoInfo, dicoInfos, 'dicoInfo')

    sentence = f"GÉNÉRATION TABLEAU HTML"
    others.print_grande_etape(sentence)

    big_process.duDicoResume_auTableauHtml(dicoInfos)

    print()


if __name__ == '__main__':
    main()
