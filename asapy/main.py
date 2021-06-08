#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json #hikaku you
from ASA import ASA

if __name__ == '__main__':
    init_start = time.time()
    asa = ASA()
    init_time = time.time() - init_start
    print("起動時間:{0}".format(init_time) + "[sec]")
    while(True):
        inp = input()
        if not inp:
            break
        start = time.time()
        asa.parse(inp)
        asa.selectOutput()
        #比較用
        data = asa.dumpJson()
        with open('result.json',mode='w',encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        elapsed_time = time.time() - start
        print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    print('終了')
