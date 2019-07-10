
class Dict2():

    def __init__(self, dic, yaml):
        self.index = {}
        for line in open(dic):
            n = line.strip().split(' ')
            self.index.update({n[0]: (int(n[1]), int(n[2]))})
