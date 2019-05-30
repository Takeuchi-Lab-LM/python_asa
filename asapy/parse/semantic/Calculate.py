from asapy.result.Chunk import Chunk

from operator import itemgetter

#
# フレームより曖昧性を解消する計算を行うクラス
#
# @TODO ここで求まる結果はタプルで無理やり格納して返している <- 新たな構造体などを用意してきれいにしたい
#


class Calculate():

    def __init__(self, frames: dict) -> None:
        self.frames = frames

    #
    # 述語のフレームを取得し，その内から最も類似度の高いフレームを取得
    #
    def getFrame(self, verb: str, linkchunks: list) -> tuple:
        frameset = []
        frames = self.frames.getFrame(verb)
        if frames:
            for frame in frames:
                if 'instance' in frame:
                    if frame['instance']:
                        for instance in frame['instance']:
                            similar, insts = self.__calculateSntSimilar(instance, linkchunks)
                            frameset.append((frame['semantic'], similar, insts))
                    else:
                        frameset.append((frame['semantic'], -1.0, []))
                else:
                    frameset.append((frame['semantic'], -1.0, []))
        frameset = sorted(frameset, key=itemgetter(1))[-1]
        return frameset

    #
    # 事例の類似度を算出
    #
    def __calculateSntSimilar(self, instance: dict, linkchunks: list) -> tuple:
        comb = self.__calculateAllCombinations(instance, linkchunks)
        insts = []
        while(sum(c[0] for c in comb)):
            tmp_comb = []
            max_ = max(comb, key=lambda c: c[0])
            insts.append(max_)
            for c in comb:
                c_noun = c[1]['noun'] if c[1]['noun'] else ''
                c_part = c[1]['part'] if c[1]['part'] else ''
                m_noun = max_[1]['noun'] if max_[1]['noun'] else ''
                m_part = max_[1]['part'] if max_[1]['part'] else ''
                if (c_noun + c_part != m_noun + m_part) and (c[2] != max_[2]):
                    tmp_comb.append(c)
            comb = tmp_comb
        similar = sum(c[0] for c in insts)
        return (similar, insts)

    #
    # 入力文と事例の項のすべての組み合わせの項類似度を求める
    #
    def __calculateAllCombinations(self, instance: dict, linkchunks: list) -> list:
        combinations = []
        for linkchunk in linkchunks:
            for icase in instance['cases']:
                similar = self.__calculateArgSimilar(icase, linkchunk)
                combinations.append((similar, icase, linkchunk))
        return combinations

    #
    # 項の類似度を算出
    #
    def __calculateArgSimilar(self, icase: dict, chunk: Chunk) -> float:
        nounsimilar = self.__getNounSimilar(icase, chunk)
        partsimilar = self.__getPartSimilar(icase, chunk)
        surfsimilar = self.__getSurfSimilar(icase, chunk)
        similar = partsimilar * (surfsimilar + partsimilar + nounsimilar) * icase['weight']
        # print(icase.noun+"("+icase.category+")" +": "+ chunk.main + "= " + similar)
        return similar

    #
    # 名詞のカテゴリによる類似度
    #
    def __getNounSimilar(self, icase: dict, chunk: Chunk) -> float:
        similar = 0.0
        if icase['category'] in chunk.category:
            similar = 1.0
        return similar

    #
    # 名詞の表層による類似度
    #
    def __getSurfSimilar(self, icase: dict, chunk: Chunk) -> float:
        similar = 0.0
        if chunk.main:
            if chunk.main == icase['noun']:
                similar = 1.0
            else:
                similar = 0.0
        return similar

    #
    # 名詞につく格による類似度
    #
    def __getPartSimilar(self, icase: dict, chunk: Chunk) -> float:
        similar = 0.0
        if 'part' in icase:
            part = icase['part']
            if part == chunk.part: similar = 1.0
            elif part == 'は' and chunk.part == 'が': similar = 1.1
            elif part == 'は' and chunk.part == 'を': similar = 1.1
            elif part in chunk.another_parts: similar = 1.0
            elif chunk.modifyingchunk:
                voice = chunk.modifyingchunk.voice
                if 'causative_part' in icase:
                    if voice == 'CAUSATIVE' and part == icase['causative_part']: similar = 1.0
                if 'passive_part' in icase:
                    if voice == 'PASSIVE' and part == icase['passive_part']: similar = 1.0
                else: similar = 0.0
            else: similar = 0.0
        else: similar = 0.0
        return similar
