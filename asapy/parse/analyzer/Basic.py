# cabochaの解析結果より文節間の関係や，語義付与に必要な動詞や格助詞などの情報の付与するクラス
import re
from asapy.result.Chunk import Chunk
from asapy.result.Result import Result


class Basic():

    def __init__(self, frames: dict) -> None:
        self.frames = frames

    def parse(self, result: Result) -> Result:
        for chunk in result.chunks:
            chunk.surface = self.__getChunkSurface(chunk)
            chunk.modifyingchunk = self.__getModifyingChunk(result, chunk)
            chunk.modifiedchunks = self.__getModifiedChunks(result, chunk)
            chunk.ctype = self.__getChunkType(chunk)
            chunk.main = self.__getHead(chunk)
            chunk.part = self.__getPart(chunk)
            for morph in chunk.morphs:
                morph.chunk = chunk
        return result

    # 文節内の形態素の表層をつなげて，文節の表層を取得
    # @param chunk 文節
    # @return 文節の表層
    def __getChunkSurface(self, chunk: Chunk) -> str:
        surface = "".join([morph.surface for morph in chunk.morphs])
        return surface

    # 係っている文節の取得
    def __getModifyingChunk(self, result: Result, chunk: Chunk) -> Chunk:
        modifyingchunk = None
        if chunk.link != -1:
            modifyingchunk = result.chunks[chunk.link]
        return modifyingchunk

    # 文節の係りを受けている文節を取得
    # @param chunk 文節
    # @return 係り元の文節集合
    def __getModifiedChunks(self, result: Result, depchunk: Chunk):
        linkchunks = [chunk for chunk in result.chunks if chunk.link == depchunk.id]
        return linkchunks

    # 文節のタイプを取得
    #  - verb:      動詞
    #  - adjective: 形容詞，形容動詞
    #  - copula:    コピュラ（AはBだ）
    #  - elem:      その他
    def __getChunkType(self, chunk: Chunk) -> str:
        if any([re.search(r"動詞,自立", m.pos) for m in chunk.morphs]):
            return 'verb'
        elif any([re.search(r"形容詞|形容詞,自立|形容動詞語幹", m.pos) for m in chunk.morphs]):
            return 'adjective'
        elif any([re.search(r"特殊・ダ|特殊・デス|判定詞", m.cform) for m in chunk.morphs]):
            return 'copula'
        return 'elem'

    # その文節の主辞となるような語の取得(意味役割付与に使用)
    def __getHead(self, chunk: Chunk) -> str:
        head = ''
        if chunk.ctype == "copula":
            morphs = [morph for morph in chunk.morphs if "名詞" in morph.pos]
            head = "".join([morph.surface if morph.base == "*" else morph.base for morph in morphs])
        elif chunk.ctype == "verb":
            ismorph = [morph for morph in chunk.morphs if morph.base == "する"]
            if ismorph:
                morph = ismorph[0]
                sahen = [m.surface for m in chunk.morphs if m.id < morph.id]
                if sahen:
                    predicate = "".join(sahen[len(sahen) - 2:len(sahen)]) + "する"
                    head = predicate if self.frames.isFrame(predicate) else sahen[-1] + "する"
                else:
                    head = "する"
            else:
                morph = [m for m in chunk.morphs if re.search(r"動詞,自立", m.pos)][0]
                ism = [m for m in chunk.morphs if m.pos1 == "動詞" and m.id == morph.id + 1]
                predicate = ""
                if ism:
                    m = ism[0]
                    predicate = morph.surface + m.base
                else:
                    ismm = [mm for mm in chunk.morphs if mm.id == morph.id - 1]
                    if ismm:
                        mm = ismm[0]
                        predicate = mm.surface + morph.base
                    else:
                        predicate = morph.base
                head = predicate if self.frames.isFrame(predicate) else morph.base
        elif chunk.ctype == "adjective":
            morph = [morph for morph in chunk.morphs if re.search(r"形容詞|形容詞,自立|形容動詞語幹", morph.pos)][0]
            if re.search(r"形容詞|形容詞,自立", morph.pos):
                head = morph.base
            elif re.search(r"形容動詞語幹", morph.pos):
                ispremorph = [m for m in chunk.morphs if m.id == morph.id - 1]
                if ispremorph:
                    premorph = ispremorph[0]
                    head = premorph.surface + morph.base + "だ"
                else:
                    head = morph.base + "だ"
        elif chunk.ctype == "elem":
            head = "".join([morph.surface for morph in chunk.morphs if re.search(r"名詞|副詞", morph.pos)])
        return head

    # 文節内の名詞につく格助詞の取得
    # @param chunk 文節
    # @return 文節内の格助詞or係助詞
    def __getPart(self, chunk: Chunk) -> str:
        part = ""
        ismorph = [morph for morph in chunk.morphs if re.search(r"格助詞|係助詞|連体化|助動詞|副助詞|判定詞", morph.pos)]
        if ismorph:
            morph = ismorph[-1]
            part = morph.base
        return part
