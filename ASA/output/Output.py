from result.Result import Result
from result.Chunk import Chunk
from result.Morph import Morph

# 解析結果を出力するためのクラス


class Output():

    def outputAll(self, result: Result) -> None:
        print("sentence: " + result.surface)
        for chunk in result.chunks:
            self.__outputChunk(chunk)

    def __outputChunk(self, chunk: Chunk) -> None:
        print("ID: " + str(chunk.id) + " " + chunk.surface)
        print("\tlink: " + str(chunk.link))
        print("\ttype: " + chunk.ctype)
        if chunk.main: print("\tmain: " + chunk.main)
        if chunk.part: print("\tpart: " + chunk.part)
        if chunk.category: print("\tcategory: " + chunk.category[0])
        if chunk.semrole: print("\tsemrole: " + "|".join(chunk.semrole))
        if chunk.arg: print("\targ: " + "|".join(chunk.arg))
        if chunk.similar > 0.0: print("\tscore: " + str(chunk.similar))
        if chunk.semantic: print("\tsemantic: " + chunk.semantic)
        modchunks = chunk.modifiedchunks
        if modchunks:
            frame = []
            for modchunk in modchunks:
                if modchunk.semrole:
                    frame.append(str(modchunk.id) + "-" + "|".join(modchunk.semrole) + "-" + "|".join(modchunk.arg))
                else:
                    frame.append(str(modchunk.id) + "-" + modchunk.ctype)
            print("\tframe: " + ",".join(frame))
        if chunk.idiom:
            print("\tidiom: " + chunk.idiom)
            print("\tfilter: " + str(chunk.idiom_score))
            ids = sorted([str(morph.chunk.id) + "-" + str(morph.id) for morph in chunk.idiom_morph])
            print("\tidiom_id: " + ",".join(ids))

        if (chunk.phrase): print("\tphrase: " + ",".join(chunk.phrase))
        if (chunk.voice): print("\tvoice: " + chunk.voice)
        if (chunk.tense): print("\ttense: " + chunk.tense)
        if (chunk.sentelem): print("\tsentelem: " + chunk.sentelem)
        if (chunk.polarity): print("\tpolarity: " + chunk.polarity)
        if (chunk.mood): print("\tmood: " + chunk.mood)
        for morph in chunk.morphs:
            self.__outputMorph(morph)
        if (chunk.noun_agentiveL): print("\tnoun_adjective: " + chunk.noun_agentiveL)
        if (chunk.noun_arg): print("\tnoun_arg: " + chunk.noun_arg)
        if (chunk.noun_semantic): print("\tnoun_semantic: " + chunk.noun_semantic)
        if (chunk.noun_semrole): print("\tnoun_semrole: " + chunk.noun_semrole)
        if (chunk.noun_semantic):
            frame = []
            for modchunk in modchunks:
                if modchunk.noun_arg and modchunk.noun_agentiveRole:
                    frame.append(str(modchunk.id) + "-" + modchunk.noun_arg + "-" + modchunk.noun_agentiveRole)
                elif modchunk.noun_arg:
                    frame.append(str(modchunk.id) + "-" + modchunk.noun_arg)
                print("\tnoun_agentiveRole: " + ",".join(frame))

    def __outputMorph(self, morph: Morph) -> None:
        morphs = [str(morph.id), morph.surface, morph.read, morph.base, morph.pos, morph.cform, morph.ctype, morph.ne]
        print("\t\t" + "\t".join(morphs))

