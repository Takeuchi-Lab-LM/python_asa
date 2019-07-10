import json
import os
from ..init.JsonFile import JsonFile
from ..load import frame
from ..load import noun
# from myjson import cchart
# from myjson import filter


class LoadJson():

    def __init__(self, files: JsonFile) -> None:
        self.frames = self.__loadFrames(files.dicframe, files.frame)
        self.categorys = self.__loadJson(files.category)
        self.ccharts = self.__loadJson(files.cchart)
        self.idioms = self.__loadJson(files.idiom)
        self.filters = self.__loadJson(files.filter)
        self.compoundPredicates = self.__loadJson(files.compoundPredicate)
        self.nouns = self.__loadNouns(files.noun)

    def __loadJson(self, jsonpath: str) -> dict:
        dirname = os.path.dirname(__file__)
        abspath = os.path.abspath(dirname)
        with open(os.path.join(abspath)+'/../'+jsonpath, 'r+') as f:
            return json.load(f)

    def __loadFrames(self, dic, jsonpath):
        frames = frame.Dict2(dic, self.__loadJson(jsonpath))
        return frames

    def __loadNouns(self, jsonpath):
        nouns = noun.Dict(self.__loadJson(jsonpath))
        return nouns
