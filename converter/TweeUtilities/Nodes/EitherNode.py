from NodeBase import *

class EitherNode(SequenceNode):
    def __init__(self, targetList):
        self.type = SequenceNodeType.either
        self.targetList = targetList

    def javascriptOutputString(self):
        return '{"type":"either","js":"%s"}'%','.join(self.targetList)
