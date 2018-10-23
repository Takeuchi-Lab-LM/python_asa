import time

from init.JsonFile import JsonFile
from load.LoadJson import LoadJson
from parse.Parse import Parse
from output.Output import Output
from result.Result import Result

from memory_profiler import profile

class ASA():

    @profile  # memory使用量を確認
    def __init__(self, analyzer: str = "cabocha") -> None:
        files = JsonFile()
        self.dicts = LoadJson(files)
        self.parser = Parse(self.dicts, analyzer)
        self.output = Output()

    def parse(self, sentence: str) -> None:
        self.result = self.parser.parse(sentence)

    def selectOutput(self, otype: str = "all") -> None:
        if otype == "all":
            self.output.outputAll(self.result)

