#!/usr/bin/env python3

import pprint
import io
import os
import codecs
import json

# Lien vers les dossiers de la racine ############################################
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
# from settings import PROJECT_ROOT
###################################################################################


def executeBashCommand(arg):
    pass


##############################################################
# Fonction : folder_here_or_create()
##############################################################
def folder_here_or_create(path_to_parent, name_folder):
    print('\n+++ Dossier : ', name_folder)
    if os.path.exists(path_to_parent + '/' + name_folder + '/'):
        print('\t+++ Dossier déjà existant')
    else:
        print(f"\n\t+++ Création du dossier : {name_folder}")
        try:
            os.makedirs(path_to_parent + '/' + name_folder + '/')
        except Exception as e:
            print('\tPROBLEME LORS DE LA CREATION DU DOSSIER.')
        else:
            print('\tCréation du dossier réussi.')


##############################################################
# Fonction : ()
##############################################################
def dump_dico_to_json(linkToFile, dicoToDump, name='dico'):
    with open(linkToFile, mode='w') as fileout:
        try:
            json.dump(dicoToDump, fileout)
        except Exception as e:
            raise
            print(f"PB : '{name}' n'a pas été enregistré.")
        else:
            print(f"Le dictionnaire '{name}' a été enregistré sous {linkToFile}.")


##############################################################
# Fonction : ()
##############################################################
def load_dico_from_json(linkToFile, name='dico'):
    dico = {}
    with open(linkToFile, mode='r') as filein:
        try:
            dico = json.load(filein)
        except Exception as e:
            raise
            print(f"PB : Le dictionnaire '{name}' n'a pas été loadé.")
            return 0
        else:
            print(f"Le dictionnaire '{name}' a été loadé de {linkToFile}.")
            return dico


##############################################################
# Fonction : folder_here_or_create()
##############################################################
def print_grande_etape(sentence):
    print("\n============================================================")
    print(f"{sentence}")
    print("============================================================\n")


if __name__ == '__main__':
    print("Je ne peux fonctionner seul.")
