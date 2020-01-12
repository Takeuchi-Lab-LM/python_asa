from asapy.init.JsonFile import JsonFile
from asapy.load.LoadJson import LoadJson
from asapy.parse.Parse import Parse
from asapy.output.Output import Output

#from memory_profiler import profile


class ASA():

    #@profile  # memory使用量を確認
    def __init__(self, analyzer: str = "cabocha") -> None:
        files = JsonFile()
        self.result = None
        self.dicts = LoadJson(files)
        self.parser = Parse(self.dicts, analyzer)
        self.output = Output()

    def parse(self, sentence: str) -> None:
        self.result = self.parser.parse(sentence)

    def selectOutput(self, otype: str = "all") -> None:
        if otype == "all":
            self.output.outputAll(self.result)

    def dumpJson(self) -> dict:
        return self.output.outputJson(self.result)
