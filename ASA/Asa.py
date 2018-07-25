import time
from init.JsonFile import JsonFile
from myjson.LoadJson import LoadJson
from parse.Parse import Parse
from output.Output import Output


class Asa():

    def __init__(self, analyzer="cabocha"):
        files = JsonFile()
        self.dicts = LoadJson(files)
        self.parser = Parse(self.dicts, analyzer)
        self.output = Output()

    def parse(self, sentence):
        self.result = self.parser.parse(sentence)

    def selectOutput(self, otype="all"):
        if otype == "all":
            self.output.outputAll(self.result)


if __name__ == '__main__':

    start = time.time()

    asa = Asa()
    asa.parse("今日はいい天気だ")
    asa.selectOutput()
    elapsed_time = time.time() - start

    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
