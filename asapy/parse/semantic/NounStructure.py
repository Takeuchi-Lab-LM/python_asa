from asapy.result.Chunk import Chunk
from asapy.load.frame import Dict2
from asapy.load.noun import Dict


class NounStructure():

    def __init__(self, nouns: Dict, frames: Dict2):
        self.nouns = nouns
        self.frames = frames

    def parse(self, chunk: Chunk):
        frame = self.nouns.getFrame(chunk.main)
        if frame:
            nounset = []
            for instance in frame['instance']:
                similar, insts = self.__calculateSntSimilar(instance, chunk)
                agent = []
                if 'agent' in instance:
                    if len(instance['agent']):
                        agent = instance['agent'][0]
                nounset.append((similar, insts, agent))
            nounset = max(nounset, key=lambda x: x[0])
            self.__setSemantic(chunk, nounset[2])
            self.__setFrame(nounset)

    def __calculateSntSimilar(self, instance: dict, chunk: Chunk) -> tuple:
        comb = self.__calculateAllCombinations(instance, chunk)
        insts = []
        while(sum(c[0] for c in comb)):
            tmp_comb = []
            max_ = max(comb, key=lambda c: c[0])
            insts.append(max_)
            for c in comb:
                if c[1] != max_[1] and c[2] != max_[2]:
                    tmp_comb.append(c)
            comb = tmp_comb
        similar = sum(c[0] for c in insts)
        return (similar, insts)

    def __calculateAllCombinations(self, instance: dict, chunk: Chunk) -> list:
        chunks = None
        if chunk.modifyingchunk:
            chunk.modifiedchunks.append(chunk.modifyingchunk)
            chunks = chunk.modifiedchunks
        else:
            chunks = chunk.modifiedchunks
        combinations = []
        for chunk in chunks:
            for icase in instance['cases']:
                similar = self.__calculateArgSimilar(icase, chunk)
                combinations.append((similar, icase, chunk))
        return combinations

    def __calculateArgSimilar(self, icase: dict, chunk: Chunk) -> float:
        partsimilar = self.__getPartSimilar(icase, chunk)
        surfsimilar = 0
        nounsimilar = 0
        similar = partsimilar + surfsimilar + nounsimilar
        return similar

    def __getPartSimilar(self, icase: dict, chunk: Chunk) -> float:
        similar = 0.0
        if icase['part'] == 'だ' and chunk.ctype =='copula': similar = 1.0
        elif icase['part'] == 'だ' and (chunk.part == 'は' or chunk.part == 'が'): similar = 1.0
        elif icase['part'] == chunk.part: similar = 1.0
        else: similar = 0.0
        return similar

    def __setSemantic(self, chunk: Chunk, agent: dict) -> None:
        if agent:
            chunk.noun_agentiveL = agent['agentive']
            chunk.noun_semantic = agent['semantic']
        else:
            chunk.noun_semantic = "Null/Null/Null"

    def __setFrame(self, nounset: tuple) -> None:
        similar, insts, agent = nounset
        print(agent)
        for pair in insts:
            argsimilar, icase, chunk = pair
            chunk.noun_semrole = icase['semrole']
            chunk.noun_arg = icase['arg']
            arg0 = agent['arg0'] if 'arg0' in agent else ''
            arg1 = agent['arg1'] if 'arg1' in agent else ''
            arg2 = agent['arg2'] if 'arg2' in agent else ''
            if icase['arg'] == "ARG0": chunk.noun_agentiveRole = arg0
            elif icase['arg'] == "ARG1": chunk.noun_agentiveRole = arg1
            elif icase['arg'] == "ARG2": chunk.noun_agentiveRole = arg2
