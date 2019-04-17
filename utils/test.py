import time
from ASA import ASA

if __name__ == '__main__':

    init_start = time.time()
    asa = ASA()
    init_time = time.time() - init_start
    print ("起動時間:{0}".format(init_time) + "[sec]")
    for line in open('testdata/test_set.txt'):
        start = time.time()
        asa.parse(line.strip())
        asa.selectOutput()
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    print('終了')

