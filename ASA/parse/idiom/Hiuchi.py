from result.Result import Result
from result.Morph import Morph

import pprint

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
            prechunk = morphs[i-1]
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
        #candicates = self.__getCandicate(morphs)
        #for idiom in candicates:
        #    self.__matchMorphs(morphs, idiom["patterns"])

    #
    # 慣用句表現辞書より候補となる慣用句の取得
    # (慣用句の最後の形態素と一致する形態素があれば候補とする)
    #
    def __getCandicate(self, morphs: list) -> list:
        candicate = []
        for morph in morphs:
            for idiom in self.idioms["dict"]:
                if self.__isMatchPattern(morph, idiom["patterns"][-1]):
                    candicate.append(idiom)
        return list(set(candicate))

    #
    # 慣用句の候補と入力文グラフを比較し，慣用句と一致する形態素を取得
    #
    '''
    def __matchMorphs(self, morphs: Morph, patterns: list) -> list:
        val idiommorphs = patterns.foldRight(Seq.empty[Seq[Morph]]) { (pattern, precandicates) =>
            val candicates = precandicates.isEmpty match {
                case true => morphs.map(Seq(_)) //ture=>初期設定として形態素ごとにをSeqに入れる(候補がなくなったときもここに入ってしまう)
                case false =>
                    precandicates.flatMap { precandicate => //false=>グラフの1つ先を追加
                        precandicate.head.tree.map(morph => morph +: precandicate)
                    }
            }
            candicates.filter(candicate => isMatchPattern(candicate.head, pattern)) //表記辞書との比較
        }.filter(_.size == patterns.size)
        return idiommorphs
    '''

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
                if "base" in idcase: bol = bol and idcase["base"] == morph.base
                if "read" in idcase: bol = bol and idcase["read"] == morph.read
                if "pos" in idcase: bol = bol and idcase["pos"] == morph.pos
        return bol
