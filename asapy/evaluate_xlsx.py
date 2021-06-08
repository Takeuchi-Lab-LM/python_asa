import time
import json #hikaku you
#import xlrd # pip install xlrd xlsxファイルに対応しなくなったらしい
import openpyxl #pip install openpyxl
from ASA import ASA

EXAMPLES = 27320 #should be changed

if __name__ == '__main__':
    init_start = time.time()
    asa = ASA()
    init_time = time.time() - init_start
    print("起動時間:{0}".format(init_time) + "[sec]")

    wb = openpyxl.load_workbook('data/pth20210305.xlsx')
    sheet = wb['pth20210305-sjis']
    cell = sheet['A3:BB3']

    sentence = cell[0][39].value
    case1 = [cell[0][4].value,cell[0][5].value,cell[0][6].value,cell[0][7].value,cell[0][8].value,cell[0][9].value,cell[0][10].value]
    case2 = [cell[0][11].value,cell[0][12].value,cell[0][13].value,cell[0][14].value,cell[0][15].value,cell[0][16].value,cell[0][17].value]
    case3 = [cell[0][18].value,cell[0][19].value,cell[0][20].value,cell[0][21].value,cell[0][22].value,cell[0][23].value,cell[0][24].value]
    case4 = [cell[0][25].value,cell[0][26].value,cell[0][27].value,cell[0][28].value,cell[0][29].value,cell[0][30].value,cell[0][31].value]
    case5 = [cell[0][32].value,cell[0][33].value,cell[0][34].value,cell[0][35].value,cell[0][36].value,cell[0][37].value,cell[0][38].value]

    print(case1)
    print(case2)
    start = time.time()
    asa.parse(sentence)
    asa.selectOutput()
    result = asa.evaluate()
    #print(result.chunks[0].surface)

    for chunk in result.chunks:
        if chunk.arg:
            print(chunk.arg[0] in case1)
            print(case1)
            print(chunk.arg[0])

    #jsonを通す必要はなさそう？
    #data = asa.dumpJson()
    #with open('result.json',mode='w',encoding='utf-8') as file:
    #    json.dump(data, file, ensure_ascii=False, indent=2)
    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    print('終了')

    #深層系 = semrole
    #格1 = 4~10
    #格2 = 11~17
    #格3 = 18~24
    #格4 = 25~31
    #格5 = 32~38
    #例文 = 39

#TODO 得られた出力結果から精度を識別する=> listに要素が含まれているかどうかで調べる。
#出力されるjsonファイルにはArgの項目が出力されてないけど、出力してもいいか？