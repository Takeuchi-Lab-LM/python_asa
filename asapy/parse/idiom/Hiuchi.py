from asapy.result.Result import Result
from asapy.result.Morph import Morph
from functools import reduce

# 慣用句同定のためのクラス
# 以下の手順により同定
# - 形態素のグラフ化
# - 慣用句の同定
# - フィルタリング


class Hiuchi():

    def __init__(self, idioms: dict, filters: dict) -> None:
        self.idioms = idioms
        self.filters = filters

    def parse(self, result: Result) -> None:
        self.__graphify(result)
        self.__matchIdiom(result)

    #
    # 慣用句同定のために入力グラフを作成
    #
    def __graphify(self, result: Result) -> None:
        self.__graphifyAsSequence(result)
        self.__graphifyAsDependency(result)

    #
    # 形態素の並び順によるグラフ化
    #
    def __graphifyAsSequence(self, result: Result) -> None:
        morphs = self.__getMorphs(result)
        for i, chunk in enumerate(morphs[1:]):
            prechunk = morphs[i]
            chunk.tree.append(prechunk)

    #
    # 係り受け関係によるグラフ化
    #
    def __graphifyAsDependency(self, result: Result) -> None:
        for chunk in result.chunks:
            modifiedmorphs = [chunk.morphs[-1] for chunk in chunk.modifiedchunks]
            chunk.morphs[0].tree.extend(modifiedmorphs)
            chunk.morphs[0].tree = list(set(chunk.morphs[0].tree))

    #
    # 慣用句表記辞書との比較し，慣用句情報の付与
    #
    def __matchIdiom(self, result: Result) -> None:
        morphs = self.__getMorphs(result)
        candicates = self.__getCandicate(morphs)
        for idiom in candicates:
            for idiommorphs in self.__matchMorphs(morphs, idiom["patterns"]):
                self.__setIdiom(idiom, idiommorphs)

    #
    # 慣用句表現辞書より候補となる慣用句の取得
    # (慣用句の最後の形態素と一致する形態素があれば候補とする)
    #
    def __getCandicate(self, morphs: list) -> list:
        candicates = []
        for morph in morphs:
            for idiom in self.idioms["dict"]:
                if self.__isMatchPattern(morph, idiom["patterns"][-1]):
                    if idiom not in candicates:
                        candicates.append(idiom)
        return candicates

    #
    # 慣用句の候補と入力文グラフを比較し，慣用句と一致する形態素を取得
    #
    def __matchMorphs(self, morphs: Morph, patterns: list) -> list:
        def foldRight(f, ptt):
            return reduce(lambda a, b: f(b, a), ptt[::-1], [])

        def flatten(arry):
            return [x for tmp in arry for x in tmp]

        idiommorphs = foldRight(
            lambda pattern, precandidates:
                list(filter(
                    lambda candidate:
                        self.__isMatchPattern(candidate[0], pattern),
                    flatten(
                        list(map(
                            lambda precandidate:
                                list(map(
                                    lambda morph:
                                        [morph] + precandidate, precandidate[0].tree
                                )),
                            precandidates
                        ))
                    ) if precandidates else list(map(lambda m: [m], morphs))
                )),
                patterns
            )
        idiommorphs = [ms for ms in idiommorphs if len(ms) == len(patterns)]
        return idiommorphs

    #
    # resultより全ての形態素を取得
    #
    def __getMorphs(self, result: Result):
        morphs = []
        for chunk in result.chunks:
            morphs.extend(chunk.morphs)
        return morphs

    #
    # 慣用句表記辞書内の1形態素分の一致判定
    #
    def __isMatchPattern(self, morph: Morph, pattern: dict) -> bool:
        bol = True
        if pattern["cases"]:
            for idcase in pattern["cases"]:
                if "base" in idcase:
                    bol = bol and idcase["base"] == morph.base
                if "read" in idcase:
                    bol = bol and idcase["read"] == morph.read
                if "pos" in idcase:
                    bol = bol and idcase["pos"] == morph.pos
        return bol

    #
    # 同定された慣用句の特徴をまとめるクラス
    # この特徴は慣用句に関係する文節よりもってくる
    #
    class mIdiom():

        def __init__(self) -> None:
            self.entry = ""
            self.voice = []
            self.polarity = []
            self.mood = []
            self.category = []
            self.sentlem = ""
            self.score = 0.0

    def __setIdiom(self, idiom: dict, morphs: list) -> None:
        chunks = []
        [chunks.extend([morph.chunk]) for morph in morphs]
        midiom = self.mIdiom()
        midiom.entry = idiom["entry"]
        for chunk in chunks:
            midiom.voice.append(chunk.voice)
            midiom.mood.append(chunk.mood)
            midiom.polarity.append(chunk.polarity)
        modifiedchunks = []
        [modifiedchunks.extend(chunk.modifiedchunks) for chunk in chunks]
        modifer = list(set(modifiedchunks) - set(chunks))
        [midiom.category.extend(chunk.category) for chunuk in modifer]
        self.__filtering(midiom)
        for chunk in chunks:
            chunk.idiom = idiom["entry"]
            if 'phrase' in idiom:
                chunk.phrase = idiom["phrase"]
            chunk.idiom_morph = morphs
            chunk.idiom_score = midiom.score

    #
    # フィルタリング辞書より曖昧性のスコアを計算
    #
    def __filtering(self, idiom: mIdiom) -> None:
        score = 0.5
        filter_ = [filter_ for filter_ in self.filters["dict"] if idiom.entry == filter_['entry']]
        if filter_:
            filter_ = filter_[0]
            nega = posi = 0.5
            if self.__disambiguator(filter_['negative'], idiom):
                nega = 0.0
            if self.__disambiguator(filter_['positive'], idiom):
                posi = 1.0
            score = (nega + posi) / 2
        idiom.score = score

    #
    # フィルタリング辞書のposi/nega要素の一致判定
    #
    def __disambiguator(self, feature: dict, idiom: mIdiom) -> bool:
        bool_ = False
        if 'polarity' in feature:
            bool_ |= (feature['polarity'] == idiom.polarity)
        if 'sentelem' in feature:
            pass
        if 'category' in feature:
            bool_ |= bool((set(feature['category']) & set(idiom.category)))
        if 'mood' in feature:
            bool_ |= bool((set(feature['mood']) & set(idiom.mood)))
        if 'voice' in feature:
            bool_ |= bool((set(feature['voice']) & set(idiom.voice)))
        return bool_
