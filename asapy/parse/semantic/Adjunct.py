#
# 追加詞を付与するためのクラス
#
from asapy.result.Chunk import Chunk


class Adjunct():

    def parse(self, modifiedlinks: list) -> None:
        for modchunk in modifiedlinks:
            modchunk.adjunct = self.__getAdjunct(modchunk)
            if modchunk.adjunct:
                if not modchunk.semrole or not (modchunk.similar > 2.0):
                    modchunk.semrole = [modchunk.adjunct]

    def __getAdjunct(self, chunk: Chunk) -> str:
        adjunct = ""
        if not adjunct:
            adjunct = self.__parseTime(chunk)
        if not adjunct:
            adjunct = self.__parseLocation(chunk)
        if not adjunct:
            adjunct = self.__parseScene(chunk)
        if not adjunct:
            adjunct = self.__parseInstrument(chunk)
        # if not adjunct:
        #     adjunct = self.__parseAs(chunk)  # 追加詞の変更により削除
        # if not adjunct:
        #     adjunct = self.__parseAround(chunk)  # 追加詞の変更により削除
        if not adjunct:
            adjunct = self.__parseReason(chunk)
        if not adjunct:
            adjunct = self.__parseLimit(chunk)
        if not adjunct:
            adjunct = self.__parsePremise(chunk)  # 未定義
        # if not adjunct:
        #    adjunct = self.__parseCitation(chunk)  # 追加詞の変更により削除
        if not adjunct:
            adjunct = self.__parsePurpose(chunk)
        if not adjunct:
            adjunct = self.__parseModificand(chunk)  # 未定義
        if not adjunct:
            adjunct = self.__parseManner(chunk)  # 未定義
        return adjunct

    def __parseTime(self, chunk: Chunk) -> str:
        time = ''
        head = chunk.category[0] if chunk.category else ''
        if head == '時間':
            if any([True if '間' in m.surface else False for m in chunk.morphs]):
                time = '場所（時）（間）'
            else:
                time = '場所（時）（点）'
        elif head == '動作':
            if any([True if '間' in m.surface else False for m in chunk.morphs]):
                time = '場所（時）（間）'
            elif any([True if m.base == '前' or m.base == '後' or m.base == 'まで' or m.base == 'から' else False for m in chunk.morphs]):
                time = '場所（時）（点）'
        return time

    def __parseLocation(self, chunk: Chunk) -> str:
        location = '場所' if '場所' in chunk.category else ''
        return location

    def __parseScene(self, chunk: Chunk) -> str:
        scene = ''
        if '動作' in chunk.category:
            if any([True if c.surface == 'に' or c.surface == 'で' else False for c in chunk.morphs]):
                scene = '場所（抽出）'
        return scene

    def __parseInstrument(self, chunk: Chunk) -> str:
        instrument = ''
        if 'モノ' in chunk.category:
            if any([True if m.surface == 'で' else False for m in chunk.morphs]):
                instrument = '手段'
        return instrument

    def __parseAs(self, chunk: Chunk) -> str:
        as_ = ''
        if any([True if m.surface == 'として' else False for m in chunk.morphs]):
            as_ = "As"
        return as_

    def __parseAround(self, chunk: Chunk) -> str:
        around = ''
        if chunk.surface == 'ことを':
            for modifiedchunk in chunk.modifiedchunks:
                if modifiedchunk.morphs[-1].surface == 'の':
                    modifiedchunk.semrole = ['Around']
            around = "Around"
        elif any([True if m.surface == 'について' else False for m in chunk.morphs]):
            around = 'Around'
        return around

    def __parseReason(self, chunk: Chunk) -> str:
        reason = ''
        for morph in chunk.morphs:
            if morph.surface == "ので" or morph.surface == "で":
                reason = "原因"
        return reason

    def __parseLimit(self, chunk: Chunk) -> str:
        limit = ''
        if '数値' in chunk.category:
            if any([True if m.surface == 'で' else False for m in chunk.morphs]):
                limit = "限界"
        return limit

    def __parsePremise(self, chunk: Chunk) -> str:
        premise = ""
        return premise

    def __parseCitation(self, chunk: Chunk) -> str:
        citation = ''
        if any([True if '引用' else False for m in chunk.morphs]):
            citation = 'Citation'
        return citation

    def __parsePurpose(self, chunk: Chunk) -> str:
        purpose = ''
        if any([True if m.surface == 'ため' else False for m in chunk.morphs]):
            for modifiedchunk in chunk.modifiedchunks:
                if any([True if m.surface == 'の' else False for m in modifiedchunk.morphs]):
                    modifiedchunk.semrole = ["目的"]
                purpose = "目的"
        return purpose

    def __parseModificand(self, chunk: Chunk) -> str:
        modify = ""
        return modify

    def __parseManner(self, chunk: Chunk) -> str:
        manner = ""
        return manner

