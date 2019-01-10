#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
#tokenizer.py entree.txt sortie.txt

import sys
from janome.tokenizer import Tokenizer

t = Tokenizer()
chemin = str(sys.argv[1])
entree = open(sys.argv[1], 'r', encoding='UTF-8')
sortie = open(sys.argv[2], 'w', encoding='UTF-8')
for token in t.tokenize(entree.read(), wakati=True):
	sortie.write(token + ' ')
