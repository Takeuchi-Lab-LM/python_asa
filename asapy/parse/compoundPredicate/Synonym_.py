from result.Result import Result
from result.Morph import Morph

# 名詞複合述語を見つけ、その類語と同じ語義、意味役割を付与する
#
# ほとんどHiuchiのコピペ
# 見つけた慣用句に対して与える情報が違うだけ


class Synonym():

    def __init__(self, compoundPredicate: dict, filters: dict) -> None:
        self.compoundPredicate = compoundPredicate
        self.filters = filters

    def parse(self, result: Result) -> None:
        #self.__graphify(result)
        self.__matchCompoundPredicate(result)


    '''
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
    '''
    #
    # @todo 全ての形態素を使用し連語の候補を取得した後、再びすべての形態素と候補でマッチングを行っている<-これは無駄
    #
    def __matchCompoundPredicate(self, result: Result) -> None:
        morphs = self.__getMorphs(result)
        candicates = self.__getCandicate(morphs)
        for compoundPredicate in candicates:
            for compoundPredicate_morph in self.__matchs(morphs, compoundPredicate["patterns"]):
                self.__setCompoundPredicate(compoundPredicate, compoundPredicate_morph)

    def __getCandicate(self, morphs: list) -> list:
        candicates = []
        for morph in morphs:
            for idiom in self.compoundPredicate["dict"]:
                if self.__isMatchPattern(morph, idiom["patterns"][-1]):
                    if idiom not in candicates:
                        candicates.append(idiom)
        return candicates

    #
    # 連語の同定
    #
    def __matchs(self, morphs: Morph, patterns: list) -> list:
        idiom = [[]]
        if patterns:
            for morph in morphs:
                if self.__isMatchPattern(morph, patterns[-1]):
                    idm = self.__matchs(morph.tree, patterns[:-1])
                    if idm:
                        idm.append(morphs)
                        idiom = idm
        return idiom[0]

    #
    # resultより全ての形態素を取得
    #
    def __getMorphs(self, result: Result):
        morphs = []
        for chunk in result.chunks:
            morphs.extend(chunk.morphs)
        return morphs

    def __isMatchPattern(self, morph: Morph, pattern: dict) -> bool:
        bol = True
        if pattern["cases"]:
            for idcase in pattern["cases"]:
                if "base" in idcase: bol = bol and idcase["base"] == morph.base
                if "read" in idcase: bol = bol and idcase["read"] == morph.read
                if "pos" in idcase: bol = bol and idcase["pos"] == morph.pos
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

    def __setCompoundPredicate(self, compoundPredicate: dict, morphs: list) -> None:
        chunks = []
        [chunks.extend([morph.chunk]) for morph in morphs]
        score = self.__filtering()  # 複合名詞と語義のどちらを選ぶかのスコアを判定（未実装）
        if score > 0.8:
            for chunk in chunks:
                if chunk == chunks[-1]:
                    chunk.semantic = compoundPredicate['semantic']
                else:
                    chunk.idiom = compoundPredicate['entry']
                    chunk.phrase = [compoundPredicate['phrase']]
                    chunk.semrole = ['慣用句']
                    chunk.idiom_morph = morphs
                    chunk.idiom_score = score

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
            if 'phrase' in idiom: chunk.phrase = idiom["phrase"]
            chunk.idiom_morph = morphs
            chunk.idiom_score = midiom.score


    def __filtering(self) -> None:
        score = 1.0
        return score


    #
    # フィルタリング辞書のposi/nega要素の一致判定
    #
    def __disambiguator(self, feature: dict, idiom: mIdiom) -> bool:
        bool_ = False
        if 'polarity' in feature: bool_ |= (feature['polarity'] == idiom.polarity)
        if 'sentelem' in feature: pass
        if 'category' in feature: bool_ |= bool((set(feature['category']) & set(idiom.category)))
        if 'mood' in feature: bool_ |= bool((set(feature['mood']) & set(idiom.mood)))
        if 'voice' in feature: bool_ |= bool((set(feature['voice']) & set(idiom.voice)))
        return bool_
