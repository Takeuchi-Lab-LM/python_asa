# 解析結果を出力するためのクラス


class Output():

    def outputAll(self, result):
        print("sentence: " + result.surface)
        for chunk in result.chunks:
            self.__outputChunk(chunk)

    def __outputChunk(self, chunk):
        print("ID: " + str(chunk.id) + " " + chunk.surface)
        print("\tlink: " + str(chunk.link))
        print("\ttype: " + chunk.ctype)
        if chunk.main != "":
            print("\tmain: " + chunk.main)
        if chunk.part != "":
            print("\tpart: " + chunk.part)
        if len(chunk.category) != 0:
            print("\tcategory: " + chunk.category[0])
        if len(chunk.semrole) != 0:
            print("\tsemrole: " + "|".join(chunk.semrole))
        if chunk.arg:
            print("\targ: " + "|".join(chunk.arg))
        if chunk.similar > 0.0:
            print("\tscore: " + chunk.similar)
        if chunk.semantic != "":
            print("\tsemantic: " + chunk.semantic)
