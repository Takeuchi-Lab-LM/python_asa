from result.Chunk import Chunk
from load.frame import Dict2
from load.noun import Dict


class NounStructure():

    def __init__(self, nouns: Dict, frames: Dict2):
        self.nouns = nouns
        self.frames = frames
    #type NounSet = (Option[(Chunk, noun.Case)], Option[(Chunk, noun.Case)], Option[(Chunk, noun.Case)], Option[noun.Agent])

    def __parse(self, chunk: Chunk):
        #val comp =
        frame = self.nouns.getFrame(chunk.main)
        if frame:
            #nounset =
            for instance in frame['instance']:
                    (similar, insts) = self.__calculateSntSimilar(instance, chunk)
                #    (similar, insts, instance.agent.headOption)
                #}.maxBy(_._1)
                #this.setSemantic(chunk, nounset._3)
                #this.setFrame(nounset)

    def __calculateSntSimilar(self, instance: dict, chunk: Chunk) -> tuple:
        comb = self.__calculateAllCombinations(instance, chunk)
        insts = []
        exit(0)
        '''
        while (comb.exists(_._1 > 0)) {
            val max = comb.maxBy(pairs => pairs._1)
            insts = insts :+ max
            comb = comb.filterNot { arg =>
                arg._2.eq(max._2) || arg._3.eq(max._3)
            }
        }

        val similar = insts.map(_._1).sum
        instance.agent
        return (similar, insts)
    }
    '''

    def __calculateAllCombinations(self, dict, chunk: Chunk) -> list:
        chunks = None
        if chunk.modifyingchunk:
            chunks = chunk.modifiedchunks.append(chunk.modifyingchunk)
        else:
            chunk.modifiedchunks
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

'''
    def setSemantic(chunk: Chunk, agent: Option[noun.Agent]) {
        agent match {
            case Some(age) =>
                chunk.noun_agentiveL = age.agentive
                chunk.noun_semantic = age.semantic
            case None =>
                chunk.noun_semantic = "Null/Null/Null"
        }
    }

    def setFrame(set: (Float, Seq[(Float, noun.Case, Chunk)], Option[Agent])) {
        val (similar, insts, agent) = set
        insts.foreach { pair =>
            val (argsimilar, icase, chunk) = pair
            chunk.noun_semrole = icase.semrole
            chunk.noun_arg = icase.arg
            agent match {
                case Some(age) if icase.arg.equals("ARG0") => chunk.noun_agentiveRole = age.arg0
                case Some(age) if icase.arg.equals("ARG1") => chunk.noun_agentiveRole = age.arg1
                case Some(age) if icase.arg.equals("ARG2") => chunk.noun_agentiveRole = age.arg2
                case None =>
            }
        }
    }
}
'''
