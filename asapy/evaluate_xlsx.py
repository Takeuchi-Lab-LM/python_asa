import time
#import xlrd # pip install xlrd => xlsxファイルに対応しなくなったらしい
import openpyxl #pip install openpyxl
from ASA import ASA
from asapy.result.Result import Result
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
            chunk_dic['Arg'] = chunk.arg
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
    init_time = time.time() - init_start
    #print("起動時間:{0}".format(init_time) + "[sec]")
    wb = openpyxl.load_workbook('data/pth20210305.xlsx')
    sheet = wb['pth20210305-sjis']
    total_tp = 0
    total_fp = 0
    total_fn = 0
    total_nn = 0
    for i in range(2,1000):
        correct_json = {'correct':[]}
        obj = "A{}:BB{}".format(i,i)
        cell = sheet[obj]
    
        sentence = cell[0][39].value
        verb = [cell[0][2].value,cell[0][3].value]
        case1 = [cell[0][4].value,cell[0][5].value,cell[0][6].value,cell[0][7].value,cell[0][8].value,cell[0][9].value,cell[0][10].value]
        case2 = [cell[0][11].value,cell[0][12].value,cell[0][13].value,cell[0][14].value,cell[0][15].value,cell[0][16].value,cell[0][17].value]
        case3 = [cell[0][18].value,cell[0][19].value,cell[0][20].value,cell[0][21].value,cell[0][22].value,cell[0][23].value,cell[0][24].value]
        case4 = [cell[0][25].value,cell[0][26].value,cell[0][27].value,cell[0][28].value,cell[0][29].value,cell[0][30].value,cell[0][31].value]
        case5 = [cell[0][32].value,cell[0][33].value,cell[0][34].value,cell[0][35].value,cell[0][36].value,cell[0][37].value,cell[0][38].value]
        semantic = "{}-{}-{}-{}-".format(cell[0][40].value,cell[0][41].value,cell[0][42].value,cell[0][43].value)
        #start = time.time()
        asa.parse(sentence)
        asa.selectOutput()
        result = asa.evaluate()

        tp = True
        fn = False

        for chunk in result.chunks:
            correct_chunk = {}
            if chunk.ctype == "elem":
            #hasArg && hasChunk.arg Q.Argがないことはあるのか
                if chunk.arg:
                    if chunk.arg[0] in case1:
                        if chunk.surface in case1 and chunk.semrole[0] in case1 and chunk.part in case1:
                            print("kaku-1")
                        else:
                            tp = False
                            correct_chunk['Arg'] = cell[0][5].value
                            correct_chunk['surface'] = cell[0][7].value
                            correct_chunk['semrole'] = cell[0][4].value
                            correct_chunk['part'] = cell[0][6].value
                    elif chunk.arg[0] in case2:
                        if chunk.surface in case2 and chunk.semrole[0] in case2:
                            print("kaku-2")
                        else:
                            tp = False
                            correct_chunk['Arg'] = cell[0][12].value
                            correct_chunk['surface'] = cell[0][14].value
                            correct_chunk['semrole'] = cell[0][11].value
                    elif chunk.arg[0] in case3:
                        if chunk.surface in case3 and chunk.semrole[0] in case3:
                            print("kaku-3")
                        else:
                            tp = False
                            correct_chunk['Arg'] = cell[0][19].value
                            correct_chunk['surface'] = cell[0][21].value
                            correct_chunk['semrole'] = cell[0][18].value
                    elif chunk.arg[0] in case4:
                        if chunk.surface in case4 and chunk.semrole[0] in case4:
                            print("kaku-4")
                        else:
                            tp = False
                            correct_chunk['Arg'] = cell[0][26].value
                            correct_chunk['surface'] = cell[0][28].value
                            correct_chunk['semrole'] = cell[0][25].value
                    elif chunk.arg[0] in case5:
                        if chunk.surface in case5 and chunk.semrole[0] in case5:
                            print("kaku-1")
                        else:
                            tp = False
                            correct_chunk['Arg'] = cell[0][33].value
                            correct_chunk['surface'] = cell[0][35].value
                            correct_chunk['semrole'] = cell[0][32].value
                    else:
                        print("Argはあるけど正しく振られてない(fp)") #tp = FALSE retrieved = TRUE,FALSE
                        tp = False
                else:
                    print("Argが振られていない=(fn)")
                    fn = True
            if chunk.ctype == "adjective":
                print("ADJECTIVE")
            if chunk.ctype == "verb":
                string_read = ""
                for morph in chunk.morphs:
                    string_read += morph.read
                if chunk.semantic:
                    if chunk.semantic == semantic:
                        print("SEMANTIC")
                    else:
                        correct_chunk['semantic'] = semantic
                        tp = False
                else:
                    fn = True
                if chunk.main:
                    if chunk.main == verb[0]:
                        print("mainTrue")
                    else:
                        correct_chunk['verb_main'] = verb[0]
                        tp = False
                else:
                    fn = True
                if string_read == verb[1]:
                    print("YOMIKATA_TRUE")
                else:
                    correct_chunk['verb_read'] = verb[1]
                    tp = False
            correct_json['correct'].append(correct_chunk)
        if tp:
            total_tp += 1
        else:
            total_fp += 1
            result_json = outputJson(result) #違うやつ
            emptyList = []
            emptyList.append(result_json)
            emptyList.append(correct_json)
            filename =  "diff/example_{}.json".format(i-1)
            #with open(filename,'w') as f: #example_number(1,2)
            #    json.dump(emptyList,f,sort_keys=True,indent=4,ensure_ascii=False)
        if fn:
            total_fn += 1
            result_json = outputJson(result) #違うやつ
            emptyList = []
            emptyList.append(result_json)
            emptyList.append(correct_json)
            filename =  "diff/example_{}.json".format(i-1)
            #with open(filename,'w') as f: #example_number(1,2)
            #    json.dump(emptyList,f,sort_keys=True,indent=4,ensure_ascii=False)
        else:
            total_nn += 1

    print(total_tp,total_fp,total_fn,total_nn)
    precision = total_tp / (total_tp + total_fp)
    recall = total_tp / (total_tp + total_fn)
    F_value = 2 * precision * recall / (precision + recall)
    print("Precision:",precision)
    print("Recall:",recall)
    print("F_value:",F_value)
    #elapsed_time = time.time() - start
    #print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    print('終了')

    #深層系 = semrole
    #格1 = 4~10
    #格2 = 11~17
    #格3 = 18~24
    #格4 = 25~31
    #格5 = 32~38
    #例文 = 39

#TODO 評価の仕方を考える　竹内先生に助けを求める。
#TODO diffの整理整頓
#TODO 
# precision適合率 = tp / (tp + fp) https://www.cse.kyoto-su.ac.jp/~g0846020/keywords/precision.html
# recall再現率 = tp / (tp+fn) https://www.cse.kyoto-su.ac.jp/~g0846020/keywords/recall.html
# F-value = 2*precision*recall /(precision + recall)  https://www.cse.kyoto-su.ac.jp/~g0846020/keywords/tpfptnfn.html

#参考になりそうなやつ 雲隠れ