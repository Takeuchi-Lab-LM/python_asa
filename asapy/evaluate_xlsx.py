import time
import openpyxl #pip install openpyxl
from ASA import ASA
from asapy.result.Result import Result
from evaluate.Evaluate import Evaluate
import json

EXAMPLES = 27320 #should be changed

#これに答えを追加する
def outputJson(result: Result) -> None:
        result_json = {'chunks': [], 'surface': result.surface}
        for chunk in result.chunks:
            chunk_dic = {}
            chunk_dic['id'] = chunk.id
            chunk_dic['surface'] = chunk.surface
            chunk_dic['link'] = chunk.link
            chunk_dic['head'] = chunk.head
            chunk_dic['Arg'] = chunk.arg #追加した
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

if __name__ == '__main__':
    init_start = time.time()
    asa = ASA()
    evaluate = Evaluate()
    init_time = time.time() - init_start
    #print("起動時間:{0}".format(init_time) + "[sec]")
    
    for i in range(2,7):    
        #start = time.time()
        correct_json = {'correct':[]}
        values = evaluate.returnValue(i)
        asa.parse(values['sentence'])
        asa.selectOutput()
        result = asa.evaluate()

        tp = True
        fn = False

        for chunk in result.chunks:
            correct_chunk = evaluate.chunkType(chunk, values, tp, fn)
            tp = correct_chunk['tp']
            fn = correct_chunk['fn']
            print(correct_chunk)
            correct_json['correct'].append(correct_chunk)
        evaluate.sumup(tp,fn)
        result_json = outputJson(result)
        filename =  "diff/example_{}.json".format(i-1)
        evaluate.outputJsonfile(correct_json, result_json,filename, tp, fn)
    
    precision,recall,F_value = evaluate.calculate()
    evaluate.output(precision, recall, F_value)
    #elapsed_time = time.time() - start
    #print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    print('終了')



#TODO 評価の仕方を考える　竹内先生に助けを求める。
#TODO diffの整理整頓 nullの時に出さない
#TODO 

#参考になりそうなやつ 雲隠れ

    #    result_json = outputJson(result) #違うやつ
    #        emptyList = []
    #        emptyList.append(result_json)
    #        emptyList.append(correct_json)
    #        filename =  "diff/example_{}.json".format(i-1)
    #         with open(filename,'w') as f: #example_number(1,2)
    #            json.dump(emptyList,f,sort_keys=True,indent=4,ensure_ascii=False)