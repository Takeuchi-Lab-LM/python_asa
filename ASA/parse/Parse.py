from parse.analyzer.Analyzer import Analyzer
from parse.analyzer.Basic import Basic
from parse.feature.Tagger import Tagger
from parse.idiom.Hiuchi import Hiuchi
from result.Result import Result
from load.LoadJson import LoadJson


class Parse():

    def __init__(self, dicts: LoadJson, analyzertype: str) -> None:
        self.analyzer = Analyzer(analyzertype, "utf-8")
        self.basic = Basic(dicts.frames)
        self.tagger = Tagger(dicts.ccharts, dicts.categorys)
        self.idiom = Hiuchi(dicts.idioms, dicts.filters)

    def parse(self, line: str) -> Result:
        result: Result
        result = self.parseChunk(line)
        result = self.parseFeature(result)
        result = self.parseIdiom(result)
        result = self.parseSemantic(result)
        result = self.parseCompoundPredicate(result)
        return result

    # cabochaを利用し文を文節と形態素を解析
    # また解析結果より相互関係や動詞などの情報を整理
    def parseChunk(self, line: str) -> Result:
        result = self.analyzer.parse(line)
        self.basic.parse(result)
        return result

    # 態や名詞カテゴリなどを付与
    def parseFeature(self, result: Result) -> Result:
        self.tagger.parse(result)
        return result

    # 慣用句の同定を行い，フィルタリングをする
    def parseIdiom(self, result: Result) -> Result:
        self.idiom.parse(result)
        return result

    # 語義や意味役割の付与
    def parseSemantic(self, result: Result) -> Result:
        return result

    # 複合述語の同定を行い，一部の語義と意味役割を上書きする
    def parseCompoundPredicate(self, result: Result) -> Result:
        return result
