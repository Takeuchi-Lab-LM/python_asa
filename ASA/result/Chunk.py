# 文節の情報を格納するクラス


class Chunk():

    def __init__(self, line: str) -> None:
        # 必須な基本情報
        self.id = 0  # 文節のid
        self.surface = ""  # 文節の表層
        self.morphs = []  # 文節内の形態素
        self.modifyingchunk = None  # 係の文節
        self.modifiedchunks = []  # 受けの文節

        # あんまりいらない情報(?)
        self.link = 0  # 係り先
        self.head = 0  # 主要語
        self.fanc = 0  # 機能語
        self.score = 0.0  # 係り関係のスコア

        # 整理により付与する情報
        self.main = ""
        self.ctype = ""
        self.verb = ""
        self.part = ""

        # 態などの情報
        self.tense = ""
        self.voice = ""
        self.polarity = ""
        self.sentelem = ""
        self.mood = ""

        # 語義や意味役割に必要な変数
        self.semantic = ""
        self.semrole = []
        # self.arg = None
        self.arg = []  # 型はリスト?
        self.category = []
        self.adjunct = ""
        self.similar = 0.0
        self.another_parts = []

        self.idiom = ""
        self.phrase = []
        self.idiom_morph = []
        self.idiom_score = []

        self.noun_agentiveL = ""
        self.noun_semantic = ""
        self.noun_semrole = ""
        self.noun_arg = ""
        self.noun_agentiveRole = ""

        self.initChunk(line)

    def initChunk(self, line):
        div1 = line.split(" ")
        div2 = div1[3].split("/")
        self.id = int(div1[1])
        self.link = int(div1[2].replace("D", ""))
        self.head = int(div2[0])
        self.fanc = int(div2[1])
        self.score = float(div1[4])

    def addMorph(self, morph):
        self.morphs.append(morph)
