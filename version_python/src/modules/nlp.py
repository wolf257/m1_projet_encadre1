#!/usr/bin/env python3

import pprint
import io
import os
import nltk
from nltk.tokenize import word_tokenize

# Lien vers les dossiers de la racine ############################################
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
# from settings import PROJECT_ROOT
###################################################################################


def produceAndPrint_bigrams(text):
    """ Produce and print bigrams """

    tokens = word_tokenize(text)
    bigram = nltk.bigrams(tokens)

    print(*map(' '.join, bigram), sep='\n')


if __name__ == '__main__':
    text = 'To be or not to be'

    produceAndPrint_bigrams(text)
