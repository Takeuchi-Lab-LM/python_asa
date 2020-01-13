from asapy.result.Result import Result
from asapy.result.Chunk import Chunk
from asapy.result.Morph import Morph

import json

# 解析結果を出力するためのクラス


class Output():

    def outputJson(self, result: Result) -> None:
        result_json = {'chunks': [], 'surface': result.surface}
        for chunk in result.chunks:
            chunk_dic = {}
            chunk_dic['id'] = chunk.id
            chunk_dic['surface'] = chunk.surface
            chunk_dic['link'] = chunk.link
            chunk_dic['head'] = chunk.head
            chunk_dic['fanc'] = chunk.fanc
            chunk_dic['score'] = chunk.score
            if chunk.modifiedchunks:
                chunk_dic['modified'] = []
                for mchunk in chunk.modifiedchunks:
                    chunk_dic['modified'].append(mchunk.id)
            chunk_dic['type'] = chunk.ctype
            chunk_dic['main'] = chunk.main
            if chunk.part: chunk_dic['part'] = chunk.part
            if chunk.tense: chunk_dic['tense'] = chunk.tense
            if chunk.voice: chunk_dic['voice'] = chunk.voice
            if chunk.polarity: chunk_dic['polarity'] = chunk.polarity
            if chunk.sentelem: chunk_dic['sentelem'] = chunk.sentelem
            if chunk.mood: chunk_dic['mood'] = chunk.mood
            if chunk.semantic: chunk_dic['semantic'] = chunk.semantic
            if chunk.modifiedchunks:
                chunk_dic['frames'] = []
                for mchunk in chunk.modifiedchunks:
                    frame_dic = {}
                    frame_dic['id'] = mchunk.id
                    frame_dic['semrole'] = '|'.join(mchunk.semrole)
                    chunk_dic['frames'].append(frame_dic)
            if chunk.semrole: chunk_dic['semrole'] = '|'.join(chunk.semrole)
            if chunk.adjunct: chunk_dic['adjunct'] = chunk.adjunct
            if chunk.category: chunk_dic['category'] = chunk.category

            chunk_dic['morphs'] = []
            for morph in chunk.morphs:
                morph_dic = {}
                morph_dic['id'] = morph.id
                morph_dic['surface'] = morph.surface
                morph_dic['pos'] = morph.pos
                morph_dic['cform'] = morph.cform
                morph_dic['ctype'] = morph.ctype
                morph_dic['base'] = morph.base
                morph_dic['read'] = morph.read
                morph_dic['pos'] = morph.pos
                if morph.forms:
                    morph_dic['forms'] = []
                    for form in morph.forms:
                        morph_dic['forms'].append(form)
                chunk_dic['morphs'].append(morph_dic)
            result_json['chunks'].append(chunk_dic)
        return result_json

    def outputAll(self, result: Result) -> None:
        print("sentence: " + result.surface)
        for chunk in result.chunks:
            self.__outputChunk(chunk)

    def __outputChunk(self, chunk: Chunk) -> None:
        print("ID: " + str(chunk.id) + " " + chunk.surface)
        print("\tlink: " + str(chunk.link))
        print("\ttype: " + chunk.ctype)
        if chunk.main:
            print("\tmain: " + chunk.main)
        if chunk.part:
            print("\tpart: " + chunk.part)
        if chunk.category:
            print("\tcategory: " + chunk.category[0])
        if chunk.semrole:
            print("\tsemrole: " + "|".join(chunk.semrole))
        if chunk.arg:
            print("\targ: " + "|".join(chunk.arg))
        if chunk.similar > 0.0:
            print("\tscore: " + str(round(chunk.similar, 6)))
        if chunk.semantic:
            print("\tsemantic: " + chunk.semantic)
        modchunks = chunk.modifiedchunks
        if modchunks:
            frame = []
            for modchunk in modchunks:
                if modchunk.semrole:
                    frame_line = str(modchunk.id) + "-" + "|".join(modchunk.semrole) + "-" + "|".join(modchunk.arg)
                    if frame_line not in frame:
                        frame.append(frame_line)
                else:
                    frame_line = str(modchunk.id) + "-" + modchunk.ctype
                    if frame_line not in frame:
                        frame.append(frame_line)
            print("\tframe: " + ",".join(frame))
        if chunk.idiom:
            print("\tidiom: " + chunk.idiom)
            print("\tfilter: " + str(chunk.idiom_score))
            ids = sorted([str(morph.chunk.id) + "-" + str(morph.id) for morph in chunk.idiom_morph])
            print("\tidiom_id: " + ",".join(ids))

        if (chunk.phrase):
            print("\tphrase: " + ",".join(chunk.phrase))
        if (chunk.voice):
            print("\tvoice: " + chunk.voice)
        if (chunk.tense):
            print("\ttense: " + chunk.tense)
        if (chunk.sentelem):
            print("\tsentelem: " + chunk.sentelem)
        if (chunk.polarity):
            print("\tpolarity: " + chunk.polarity)
        if (chunk.mood):
            print("\tmood: " + chunk.mood)
        for morph in chunk.morphs:
            self.__outputMorph(morph)
        if (chunk.noun_agentiveL):
            print("\tnoun_adjective: " + chunk.noun_agentiveL)
        if (chunk.noun_arg):
            print("\tnoun_arg: " + chunk.noun_arg)
        if (chunk.noun_semantic):
            print("\tnoun_semantic: " + chunk.noun_semantic)
        if (chunk.noun_semrole):
            print("\tnoun_semrole: " + chunk.noun_semrole)
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
