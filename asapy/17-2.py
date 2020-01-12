#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os, sys, re

#sys.path.append(os.path.join(os.path.dirname(__file__), '/home/a6m1/Dropbox/Masataka/linguistics/python/python_asa/asapy'))

# bashで実行する際、pyファイル名の後に調べたいテキストを入力できるようにする

from ASA import ASA

asa = ASA()

txt = open(sys.argv[1])

for line in txt:

    line    =   line.rstrip()

#inp = input(open(sys.argv[1]))
    inp = line
    asa.parse(inp)
    print(asa.selectOutput())

