import json
from myjson import frame
from myjson import cchart
from myjson import filter


class LoadJson():

    def __init__(self, files):
        self.frames = self.loadFrames(files.dicframe, files.frame)
        self.categorys = self.loadCategorys(files.category)
        self.ccharts = self.loadCcharts(files.diccchart, files.cchart)
        self.idioms = self.loadIdioms(files.idiom)
        self.filters = self.loadFilters(files.dicfilter, files.filter)
        self.compoundPredicates = self.loadCompoundPredicates(files.compoundPredicate)
        self.nouns = self.loadNouns(files.noun)

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
