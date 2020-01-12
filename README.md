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

## 動く例
- 詰将棋の本を買ってきました
- タクシーを乗り逃げする

## 変更点
- 2020/1/12 バグの修正．辞書構造をJsonに変更．moodなど動詞ムードなどの判定変更．semroleの場所判定の修正．願望(DESIDERATIVE)を追加．
