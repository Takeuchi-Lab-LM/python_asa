import time
from ASA import ASA

if __name__ == '__main__':

    init_start = time.time()
    asa = ASA()
    init_time = time.time() - init_start
    print ("起動時間:{0}".format(init_time) + "[sec]")
    while(True):
        inp = input()
        if not inp:
            break
        start = time.time()
        asa.parse(inp)
        asa.selectOutput()
        elapsed_time = time.time() - start
        print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    print('ASA終了')

'''
asa.parse("今日はいい天気だ")
asa.selectOutput()
asa.parse("昨日はいい天気だった")
asa.selectOutput()
asa.parse("明日はいい天気だろう")
asa.selectOutput()
asa.parse("あの人は自立できる")
asa.parse("太郎は走った")
asa.selectOutput()
'''
