
# ASAで使用する辞書を指定するクラス
# 今はここに直書きだが，いい方法があれば変更したい


class JsonFile():

    def __init__(self) -> None:
        self.frame = "dict/new_argframes.json"
        self.dicframe = "dict/new_argframes.dic"
        self.cchart = "dict/ccharts.json"
        self.diccchart = "dict/ccharts.dic"
        self.verb = "dict/verbs.json"
        self.category = "dict/new_categorys.json"
        self.idiom = "dict/idioms.json"
        self.filter = "dict/filters.json"
        self.dicfilter = "dict/filters.dic"
        self.compoundPredicate = "dict/compoundPredicates.json"
        self.noun = "dict/NounTest.json"
