class Result():

    def __init__(self, line):
        self.chunks = []
        self.surface = line

    def addChunk(self, chunk):
        self.chunks.append(chunk)
