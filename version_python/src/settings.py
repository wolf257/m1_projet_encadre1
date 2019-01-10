#!/usr/bin/env python3
# -*- coding : utf8 -*-

# NOTE : Ne surtout pas déplacer ce fichier !! Sinon tous les paths changeront !!
# NOTE : Lancer python3 settings.py une fois avant de lancer main.

import os
import modules.others as others

# .../version_python/
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__ + "/../../"))
# .../version_python/src/
SRC_ROOT = os.path.abspath(os.path.dirname(__file__))
# /version_python/OUTPUT/
OUTPUT_ROOT = os.path.join(PROJECT_ROOT, 'OUTPUT/')


def check_initialOutputFolders():
    listeOutputFolders = ['CONTEXTES_TXT', 'CONTEXTES_HTML',  'DUMP_TEXT', 'IMAGES',
                          'PAGES_ASPIREES', 'TABLEAUX', 'URLS', 'BIGRAMS']

    for folder in listeOutputFolders:
        others.folder_here_or_create(OUTPUT_ROOT, folder)


CONTEXTES_TXT = os.path.join(OUTPUT_ROOT, 'CONTEXTES_TXT/')
CONTEXTES_HTML = os.path.join(OUTPUT_ROOT, 'CONTEXTES_HTML/')
DUMP_TEXT = os.path.join(OUTPUT_ROOT, 'DUMP_TEXT/')
IMAGES = os.path.join(OUTPUT_ROOT, 'IMAGES/')
PAGES_ASPIREES = os.path.join(OUTPUT_ROOT, 'PAGES_ASPIREES/')
TABLEAUX = os.path.join(OUTPUT_ROOT, 'TABLEAUX/')
URLS = os.path.join(OUTPUT_ROOT, 'URLS/')
BIGRAMS = os.path.join(OUTPUT_ROOT, 'BIGRAMS/')


def main():
    print(f"\n* La base du projet est : \n\t{PROJECT_ROOT}")
    print(f"\n* Tous les codes seront sous : \n\t{SRC_ROOT}")
    print(f"\n* Tous les résultats seront sous : \n\t{OUTPUT_ROOT}")

    check_initialOutputFolders()


if __name__ == '__main__':
    main()
