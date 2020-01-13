# python_asa
python版日本語意味役割付与システム（ASA）

## 動作環境
- Python 3.5 以上
- cabochaをpythonで使えるようにしておく
- cabochaのダウンロード https://taku910.github.io/cabocha/

## インストール
```git clone {url} ```

```pip install -e python_asa```

## 使用方法
```cd asapy```でディレクトリを移動し、
```python main.py``` で起動して標準入力を受け付けます。

## 変更点
- 2020/1/12 バグの修正．辞書構造をJsonに変更．moodなど動詞ムードなどの判定変更．semroleの場所判定の修正．願望(DESIDERATIVE)を追加．

## About ASA (Argument Structure Analyzer) and ASA python

This analyzer extracts predicate-argument structures in Japanese sentences based on the predicate frame file [Predicate Thesaurus (PT)](http://pth.cl.cs.okayama-u.ac.jp/testp/pth/Vths), which is constructed under Project of Constructing Japanese Thesaurus of Predicate-Argument Structure. Thus, ASA may fail to detect some predicate-argument structures in the cases which the predicates are not registered in PT. Although PT currently contains more than about 10,000 predicates, there may remains some bugs since the thesaurus is under construction.

This predicate-argument analyzer (ASA) detects a set of predicate-arguments based on chunk dependency. Since dependency is not phrasal based, you need to follow the dependency links when you want to get a phrase.

Here is an example. The bracket [ ] indicates a chunk, and the numbers are chunk id and its head chunk id.

> [0 1 太郎の] [1 3 本を] [2 3 健が] [3 -1 捨てた]
> 
> [0 1 Taro-[gen]{.smallcaps}]  [1 3 hon-[acc]{.smallcaps}] [2 3 ken-[nom]{.smallcaps}] [3 -1 sutet-a (dumped)]

In this example, output of ASA as a predicate-aruments  is

> [arg0 健が]  [arg1 本を]   [v 捨てた]  

Thus [太郎の] chunk is not extracted. If you want to get a correct phrase of arg1, i.e.,
[arg1   太郎の本を],  you have to extract [太郎の] chunk by following chunk dependency links.  

## Accuracy of detecting semantic role labels.
Accuracy of semantic role labeling is about 60% evaluated on [BCCWJ-PT corpus](http://pth.cl.cs.okayama-u.ac.jp/). The system uses a simple approach based on rule-based technique, then the accuracy is not high.

## Example of how we can get a set of predicate-arguments.
> Input sentence: 太郎は6時に次郎を追いかけた。

> Output ['追いかける', ['太郎は', '対象'], ['6時に', '場所（時）（点）'], ['次郎を', '']]

> getpas.py

```python
from ASA import ASA

def out_predarg(result_chunks):
    for chunk in result_chunks:
        if chunk.get('semantic') != None:
            # get a predicate-argument
            out_st = []
            out_st.append(chunk['main'])
            record_arg_chunk_ids = []
            for arg_chunk in chunk['frames']:
                arg_chunk_id = arg_chunk['id']
                if arg_chunk_id in record_arg_chunk_ids:
                    continue
                arg_surface = result_chunks[arg_chunk_id]['surface']
                arg_role = arg_chunk['semrole']
                #arg_nrole = result_chunks[arg_chunk_id]['surface']
                out_st.append([arg_surface,arg_role])
                record_arg_chunk_ids.append(arg_chunk_id)
            print(out_st)

if __name__ == '__main__':
    asa = ASA()
    sentences = ["太郎は6時に次郎を追いかけた", "昨日，太郎に会った", "太郎が買った本を売った"]
    for sent in sentences:
        asa.parse(sent) #Class resut.Result
        result_json = asa.dumpJson()
        print (result_json['surface']) # input sentence
        result_chunks = result_json['chunks']
        out_predarg(result_chunks)
```
