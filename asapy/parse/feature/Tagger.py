import re
from asapy.result.Result import Result
from asapy.result.Chunk import Chunk
from asapy.result.Morph import Morph

# 態や時制などの情報を付与するためのクラス


class Tagger():

    def __init__(self, ccharts: dict, categorys: dict) -> None:
        self.ccharts = ccharts
        self.categorys = categorys

    def parse(self, result: Result) -> Result:
        for chunk in result.chunks:
            chunk.voice = self.__parseVoice(chunk)
            chunk.tense = self.__parseTense(chunk)
            chunk.polarity = self.__parsePolarity(chunk)
            chunk.sentelem = self.__parseSentElem(chunk)
            chunk.mood = self.__parseMood(chunk)
            chunk.category = self.__parseCategory(chunk)
            for morph in chunk.morphs:
                morph.forms = self.__parseCchart(morph)
        return result

    #
    # 文節態を解析し取得
    # 付与する態
    # - ACTIVE: 能動態
    # - CAUSATIVE: 使役態
    # - PASSIVE: 受動態
    # - POTENTIAL: 可能態
    #
    def __parseVoice(self, chunk: Chunk) -> str:
        voice = ""
        if chunk.morphs:
            for morph in chunk.morphs:
                # if re.search(r"れる|られる", morph.base) and re.search(r"動詞,接尾", morph.pos):
                if (morph.base == "れる" or morph.base == "られる") and \
                    re.search(r"動詞,接尾", morph.pos):
                    voice = "PASSIVE"
                elif morph.base == "できる" and re.search(r"動詞,自立", morph.pos):
                    voice = "POTENTIAL"
                elif (morph.base in ["せる", "させる"] and re.search(r"動詞,接尾", morph.pos)) or \
                     (morph.base == "もらう" or morph.base == "いただく") and \
                     re.search(r"動詞,非自立", morph.pos):
                    voice = "CAUSATIVE"
        if "elem" != chunk.ctype and not voice:
            voice = "ACTIVE"
        return voice

    #
    # 時制情報の解析と付与
    # 付与する時制の情報
    # - PAST: 過去
    #
    def __parseTense(self, chunk: Chunk) -> str:
        tense = ""
        isPast = False
        if chunk.morphs:
            isPast = bool([morph for morph in chunk.morphs if re.search(r"助動詞", morph.pos) and morph.base in ["た", "き", "けり"]])
            if not isPast:
                before_morph = ""
                for morph in chunk.morphs:
                    if re.search(r"助動詞", morph.pos) and morph.base == "だ":
                        if "連用" in before_morph.ctype:
                            isPast = True
                    before_morph = morph
        if isPast:
            tense = "PAST"
        else:
            tense = "PRESENT"
        return tense

    #
    # 極性情報の解析と取得
    # 付与する極性の情報
    # AFFIRMATIVE: 肯定
    # NEGATIVE: 否定
    #
    def __parsePolarity(self, chunk: Chunk) -> str:
        polarity = ""
        isNegative = False
        if chunk.morphs:
            isNegative = bool([morph for morph in chunk.morphs if re.search(r"助動詞", morph.pos) and (morph.base in ["ない", "ぬ"] or re.search(r"まい", morph.base))])
        if isNegative:
            polarity = "NEGATIVE"
        elif "elem" != chunk.ctype:
            polarity = "AFFIRMATIVE"
        else:
            polarity = ""
        return polarity

    #
    # 文要素の情報を解析し取得
    #
    def __parseSentElem(self, chunk: Chunk) -> str:
        sentelem = ""
        last = chunk.morphs[-1]
        if re.search(r"体言接続", last.cform) or re.search(r"連体詞|形容詞", last.pos) or (re.search(r"助詞,連体化", last.pos) and last.base == "の"):
            sentelem = "ADNOMINAL"
        elif re.search(r"連用", last.cform) or re.search(r"副詞", last.pos) or (re.search(r"助詞,格助詞", last.pos) and last.base == "に"):
            sentelem = "ADVERBIAL"
        elif not chunk.modifyingchunk:
            sentelem = "PREDICATE"
        else:
            sentelem = ""
        return sentelem

    #
    # 法情報を解析し取得
    #
    def __parseMood(self, chunk: Chunk) -> str:
        mood_list = []
        mood = ""
        for morph in chunk.morphs:
            if morph.cform == "仮定":
                mood_list.append("SUBJUNCTIVE")
            elif morph.cform == "命令":
                mood_list.append("IMPERATIVE")
            elif morph.base == "な" and re.search(r"助詞,終助詞", morph.pos):
                mood_list.append("PROHIBITIVE")
            elif morph.base == "たい" and re.search(r"助動詞", morph.pos):
                mood_list.append("DESIDERATIVE")
            elif morph.base == "?" or (morph.base == "か" and re.search("／", morph.pos)):
                mood_list.append("INTERROGATIVE")
        if mood_list:
            mood = ",".join(list(set(mood_list)))
        elif "elem" != chunk.ctype:
            mood = "INDICATIVE"
        else:
            mood = ""
        return mood

    #
    # 文節中に名詞カテゴリが付与できるものがあればカテゴリの種類を返す
    # @param morphs 文節中の形態素の配列
    # @return カテゴリ
    #
    def __parseCategory(self, linkchunk: str) -> list:
        category = [d["category_name"] for d in self.categorys["dict"] if linkchunk.main in d["noun"]]
        if linkchunk.morphs:
            for morph in linkchunk.morphs:
                if morph.pos in ["名詞,接尾,助数詞", "名詞,数"]:
                    # if morph.surface in ["年", "月", "日", "時", "分", "秒"]:
                    if re.search(r"年|月|日|時|分|秒", morph.surface):
                        category.append("時間")
                    else:
                        category.append("数値")
                if morph.pos in ["名詞,固有名詞,人名", "名詞,接尾,人名"]:
                    category.append("人")
                elif morph.pos in ["名詞,固有名詞,地域,一般","名詞,固有名詞,地域,国", "名詞,接尾,地域"]:
                    category.append("場所")
                elif morph.pos in ["名詞,固有名詞,組織"]:
                    category.append("組織")
        return list(set(category))

    #
    # 形態素の活用型の情報を解析し取得
    #
    def __parseCchart(self, morph: Morph) -> list:
        forms = []
        if morph.cform:
            for d in self.ccharts["dict"]:
                if d["ctype"] == morph.cform:
                    forms = d["form"]
        return forms
