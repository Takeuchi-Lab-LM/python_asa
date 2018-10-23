import json
import sys
from init.JsonFile import JsonFile
# from myjson import frame
# from myjson import cchart
# from myjson import filter


class LoadJson():

    def __init__(self, files: JsonFile) -> None:
        self.frames = self.__loadJson(files.frame)
        self.categorys = self.__loadJson(files.category)
        self.ccharts = self.__loadJson(files.cchart)
        self.idioms = self.__loadJson(files.idiom)
        self.filters = self.__loadJson(files.filter)
        self.compoundPredicates = self.__loadJson(files.compoundPredicate)
        self.nouns = self.__loadJson(files.noun)

    def __loadJson(self, jsonpath: str) -> dict:
        with open(jsonpath, 'r+') as f:
            return json.load(f)

# jsonを一気に読み込む形式にしたので、下記は全て必要なくなった
'''
    def loadFrames(self, dic, jsonpath):
        frames = frame.Dict2(dic, jsonpath)
        return frames

    def loadCategorys(self, jsonpath):
        with open(jsonpath, 'r+') as f:
            return json.load(f)

    def loadCcharts(self, dic, jsonpath):
        ccharts = cchart.Dict2(dic, jsonpath)
        return ccharts

    def loadIdioms(self, jsonpath):
        with open(jsonpath, 'r+') as f:
            return json.load(f)

    def loadFilters(self, dic, jsonpath):
        filters = filter.Dict2(dic, jsonpath)
        return filters

    def loadCompoundPredicates(self, jsonpath):
        with open(jsonpath, 'r+') as f:
            return json.load(f)

    def loadNouns(self, jsonpath):
        with open(jsonpath, 'r+') as f:
            return json.load(f)
'''
