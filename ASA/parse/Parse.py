from parse.analyzer.Analyzer import Analyzer
from parse.analyzer.Basic import Basic


class Parse():

    def __init__(self, dicts, analyzertype):
        self.analyzer = Analyzer(analyzertype, "utf-8")
        self.basic = Basic()
        self.basic.setFrames(dicts.frames)

    def parse(self, line):
        result = self.parseChunk(line)
        result = self.parseFeature(result)
        result = self.parseIdiom(result)
        result = self.parseSemantic(result)
        result = self.parseCompoundPredicate(result)
        return result

    # cabochaを利用し文を文節と形態素を解析
    # また解析結果より相互関係や動詞などの情報を整理
    def parseChunk(self, line):
        result = self.analyzer.parse(line)
        result = self.basic.parse(result)
        return result

    # 態や名詞カテゴリなどを付与
    def parseFeature(self, result):
        return result

    # 慣用句の同定を行い，フィルタリングをする
    def parseIdiom(self, result):
        return result

    # 語義や意味役割の付与
    def parseSemantic(self, result):
        return result

    # 複合述語の同定を行い，一部の語義と意味役割を上書きする
    def parseCompoundPredicate(self, result):
        return result
