# cabochaの解析結果より文節間の関係や，語義付与に必要な動詞や格助詞などの情報の付与するクラス


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
            # result.chunks[i].part = self.getPart(result.chunks[i])
            # for ii in range(len(result.chunks[i].morphs)):
            #    result.chunks[i].morphs[ii].chunk = result.chunks[i]
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
            if "動詞,自立" in morph.pos:
                ctype = "verb"
            elif "形容詞" in morph.pos or "形容詞,自立" in morph.pos or "形容動詞語幹" in morph.pos:
                ctype = "adjective"
            elif "特殊・ダ" in morph.cform or "特殊・デス" in morph.cform or "判定詞" in morph.cform:
                ctype = "copula"
        return ctype

    # その文節の主辞となるような語の取得(意味役割付与に使用)
    def __getHead(iself, chunk):
        head = None
        if chunk.ctype == "copula":
            morphs = [morph for morph in chunk.morphs if "名詞" in morph.pos]
            head = "".join([morph.surface if morph.base == "*" else morph.base for morph in morphs])
        elif chunk.ctype == "verb":
            head = "未実装"
        elif chunk.ctype == "adjective":
            for morph in chunk.morphs:
                if "形容詞" in morph.pos or "形容詞,自立" in morph.pos:
                    head = morph.base
                    break
                elif "形容詞語幹" in morph.pos:
                    premorph = [m for m in chunk.morphs if m.id == morph.id - 1]
                    if len(premorph) != 0:
                        head = premorph[0].surface + morph.base + "だ"
                    else:
                        head = morph.base + "だ"
        # elif chunk.ctype == "verb":
        #     sahen = [morph for morph in chunk.morphs if morph.base == "する"]
        #     if len(sahen) != 0:
        elif chunk.ctype == "elem":
            head = "".join([morph.surface for morph in chunk.morphs if "名詞" in morph.pos or "副詞" in morph.pos])
        return head
