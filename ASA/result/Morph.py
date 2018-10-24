# 形態素の解析結果格納用


class Morph():

    def __init__(self, m_id, line):
        self.id = 0  # 形態素のid
        self.surface = ""  # 形態素の表層
        self.pos = ""  # 品詞，品詞細分類1，品詞細分類2，品詞細分類3
        self.pos1 = ""
        self.pos2 = ""
        self.pos3 = ""
        self.pos4 = ""
        self.base = ""  # 基本形
        self.read = ""  # 読み
        self.cform = ""  # 活用形
        self.ctype = ""  # 活用型
        self.ne = ""  # 固有表現解析
        self.tree = []
        self.chunk = None
        self.forms = []

        self.initMorph(m_id, line)

    def initMorph(self, m_id, line):
        div1 = line.split("\t")
        div2 = div1[1].split(",")
        self.id = m_id
        self.surface = div1[0]
        if div2[0] != "*":
            self.pos1 = div2[0]
        if div2[1] != "*":
            self.pos2 = div2[1]
        if div2[2] != "*":
            self.pos3 = div2[2]
        if div2[3] != "*":
            self.pos4 = div2[3]
        if div2[4] != "*":
            self.cform = div2[4]
        if div2[5] != "*":
            self.ctype = div2[5]
        self.pos = self.getPos()
        self.base = div2[6]
        if len(div2) >= 8:
            self.read = div2[7]
        self.ne = div1[2]

    def getPos(self):
        pos = ""
        if self.pos1 != "":
            pos = pos + self.pos1
        if self.pos2 != "":
            pos = pos + "," + self.pos2
        if self.pos3 != "":
            pos = pos + "," + self.pos3
        if self.pos4 != "":
            pos = pos + "," + self.pos4
        return pos
