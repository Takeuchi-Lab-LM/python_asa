# cabochaの解析結果より文節間の関係や，語義付与に必要な動詞や格助詞などの情報の付与するクラス
import re


class Basic():

    def __init__(self):
        self.frames = None

    def setFrames(self, frames):
        self.frames = frames

    def parse(self, result):
        for i in range(len(result.chunks)):
            result.chunks[i].surface = self.__getChunkSurface(result.chunks[i])
            result.chunks[i].modifyingchunk = self.__getModifyingChunk(result, result.chunks[i])
            result.chunks[i].modifiedchunks = self.__getModifiedChunks(result, result.chunks[i])
            result.chunks[i].ctype = self.__getChunkType(result.chunks[i])
            result.chunks[i].main = self.__getHead(result.chunks[i])
            result.chunks[i].part = self.__getPart(result.chunks[i])
            for ii in range(len(result.chunks[i].morphs)):
                result.chunks[i].morphs[ii].chunk = result.chunks[i]
        return result

    # 文節内の形態素の表層をつなげて，文節の表層を取得
    # @param chunk 文節
    # @return 文節の表層
    def __getChunkSurface(self, chunk):
        surface = "".join([morph.surface for morph in chunk.morphs])
        return surface

    # 係っている文節の取得
    def __getModifyingChunk(self, result, chunk):
        modifyingchunk = None
        if chunk.link != -1:
            modifyingchunk = result.chunks[chunk.link]
        return modifyingchunk

    # 文節の係りを受けている文節を取得
    # @param chunk 文節
    # @return 係り元の文節集合
    def __getModifiedChunks(self, result, depchunk):
        linkchunks = [chunk for chunk in result.chunks if chunk.link == depchunk.id]
        return linkchunks

    # 文節のタイプを取得
    #  - verb:      動詞
    #  - adjective: 形容詞，形容動詞
    #  - copula:    コピュラ（AはBだ）
    #  - elem:      その他
    def __getChunkType(self, chunk):
        ctype = "elem"
        for morph in chunk.morphs:
            if re.search(r"動詞,自立", morph.pos):
                ctype = "verb"
            elif re.search(r"形容詞|形容詞,自立|形容動詞語幹", morph.pos):
                ctype = "adjective"
            elif re.search(r"特殊・ダ|特殊・デス|判定詞", morph.cform):
                ctype = "copula"
        return ctype

    # その文節の主辞となるような語の取得(意味役割付与に使用)
    def __getHead(self, chunk):
        head = None
        if chunk.ctype == "copula":
            morphs = [morph for morph in chunk.morphs if "名詞" in morph.pos]
            head = "".join([morph.surface if morph.base == "*" else morph.base for morph in morphs])
        elif chunk.ctype == "verb":
            morph = [morph for morph in chunk.morphs if morph.base == "する"]
            if morph:
                sahen = [m.surface for m in chunk.morphs if m.id < morph.id]
                if sahen:
                    predicate = "".join(sahen[len(sahen) - 2:len(sahen)]) + "する"
                    head = predicate if self.frames.isFrame(predicate) else sahen[-1] + "する"
                else:
                    head = "する"
            else:
                morph = [m for m in chunk.morphs if re.search(r"動詞,自立", m.pos)][0]
                m = [m for m in chunk.morphs if m.pos1 == "動詞" and m.id == morph.id + 1]
                predicate = ""
                if m:
                    predicate = morph.surface + m[0].base
                else:
                    mm = [mm for mm in chunk.morphs if mm.id == morph.id - 1]
                    predicate = mm.surface + morph.base if mm else morph.base
                head = predicate if self.frames.isFrame(predicate) else morph.base
        elif chunk.ctype == "adjective":
            morph = [morph for morph in chunk.morphs if re.search(r"形容詞|形容詞,自立|形容詞語幹", morph.pos)][-1]
            if re.search(r"形容詞|形容詞,自立", morph.pos):
                head = morph.base
            elif re.search(r"形容詞語幹", morph.pos):
                premorph = [m for m in chunk.morphs if m.id == morph.id - 1]
                if premorph:
                    head = premorph.surface + morph.base + "だ"
                else:
                    head = morph.base + "だ"
        elif chunk.ctype == "elem":
            head = "".join([morph.surface for morph in chunk.morphs if re.search(r"名詞|副詞", morph.pos)])
        return head

    # 文節内の名詞につく格助詞の取得
    # @param chunk 文節
    # @return 文節内の格助詞or係助詞
    def __getPart(self, chunk):
        morph = [morph for morph in chunk.morphs if re.search(r"格助詞|係助詞|連体化|助動詞|副助詞|判定詞", morph.pos)]
        part = morph[-1].base if morph else ""
        return part
