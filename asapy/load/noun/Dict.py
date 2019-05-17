class Dict():

    def __init__(self, nouns: dict) -> None:
        self.nouns = nouns

    def isFrame(self, noun: str) -> bool:
        bol = False
        if noun:
            for frame in self.nouns['dict']:
                head = frame['head'] if frame['head'] else ''
                support = frame['support'] if frame['support'] else ''
                bol = (head == noun) or (head + support == noun) or (head == noun[:-1]) or (head + support == noun[:-1])
                if bol:
                    break
        return bol

    def getFrame(self, noun: str) -> dict:
        frame = None
        if noun:
            for frame_ in self.nouns['dict']:
                head = frame_['head'] if frame_['head'] else ''
                support = frame_['support'] if frame_['support'] else ''
                bol = (head == noun) or (head + support == noun) or (head == noun[:-1]) or (head + support == noun[:-1])
                if bol:
                    frame = frame_
                    break
        return frame
