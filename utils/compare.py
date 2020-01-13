
from asapy.ASA import ASA

# 正解データとASAの解析結果の比較

asa = ASA()
Scount = {'all': 0, 'true': 0, 'false': 0}
Rcount = {'all': 0, 'true': 0, 'false': 0}
SemanticResult = {'true': 0.0, 'precision': 0.0, 'recall': 0.0}
RoleResult = {'true': 0.0, 'precision': 0.0, 'recall': 0.0, 'precision2': 0.0, 'recall2': 0.0}

def compareResult(result, clist):
    print(clist)
    roles = clist[1:13]
    roles = [[roles[i], roles[i+1]] for i in range(0,12,2) if roles[i+1]]  # [深層格, 事例]のリストの形にする

    Scount['all'] += 1
    SemanticResult['recall'] += 1
    Rcount['all'] += len(roles)
    RoleResult['recall'] += len(roles)

    verb = clist[0]  # 見出し語
    semantic = clist[15]  # 概念フレーム
    pred_num = int(clist[13])  # 文中に同一な述語がある場合の番号
    candicate_chunks = [c for c in asa.result.chunks if c.main == verb]
    chunk = candicate_chunks[pred_num] if len(candicate_chunks) > pred_num else None

    if chunk:
        SemanticResult['precision'] += 1
        RoleResult['precision'] += len([c for c in chunk.modifiedchunks if c.semrole])
        compareSemantic(chunk, semantic)
        compareRole(chunk, roles)


def compareSemantic(chunk, semantic):
    if semantic == chunk.semantic:
        Scount['true'] += 1
        SemanticResult['true'] += 1
    else:
        Scount['false'] += 1


def compareRole(chunk, roles):
    pairs = getMatchChunk(chunk, roles)
    for pair in pairs:
        modchunk, roles = pair
        role = roles[0].split('（')[0]
        term = roles[1]
        if role in [r.split('（')[0] for r in modchunk.semrole]:
            Rcount['true'] += 1
            RoleResult['true'] += 1
        else:
            Rcount['false'] += 1

        # bccwj, cabochaによるミスを除いたprecision recallのカウント
        RoleResult['recall2'] += 1
        if modchunk.semrole:
            RoleResult['precision2'] += 1


# ASAの解析と正解データでchunkが一致するペアを取得
def getMatchChunk(chunk, roles):
    pairs = [[(mod, role) for mod in reversed(chunk.modifiedchunks) if mod.surface in role[1]] for role in roles][0] if roles else []
    return pairs

def outputResult():
    print("全語義: " + str(Scount["all"]))
    print(" 語義の一致: " + str(Scount["true"]))
    print(" 語義の不一致: " + str(Scount["false"]))
    print(" 取れなかった動詞: " + str(Scount["all"] - Scount["true"] - Scount["false"]))
    print("precision\t" + str((SemanticResult["true"] / SemanticResult["precision"]) * 100) + "%")
    print("recall\t" + str((SemanticResult["true"] / SemanticResult["recall"]) * 100) + "%")
    print()
    print("全意味役割: " + str(Rcount["all"]))
    print(" 意味役割の一致: " + str(Rcount["true"]))
    print(" 意味役割の不一致: " + str(Rcount["false"]))
    print(" 取れなかったchunk: " + str(Rcount["all"] - Rcount["true"] - Rcount["false"]))
    print("presicion\t" + str((RoleResult["true"] / RoleResult["precision"]) * 100) + "%")
    print("recall\t" + str((RoleResult["true"] / RoleResult["recall"]) * 100) + "%")
    print("presicion2\t" + str((RoleResult["true"] / RoleResult["precision2"]) * 100) + "%")
    print("recall2\t" + str((RoleResult["true"] / RoleResult["recall2"]) * 100) + "%")


if __name__ == '__main__':
    infile = '/home1/ex/ikeda/data/wbccj20140823_correct.csv'

    with open(infile) as f:
        for cline in f.readlines()[1:]:
            clist = [e[1:-1] for e in cline.rstrip().split(',')]
            asa.parse(clist[14])
            compareResult(asa.result, clist)
    outputResult()
