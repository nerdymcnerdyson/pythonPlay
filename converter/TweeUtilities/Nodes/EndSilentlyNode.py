from . import NodeBase
from . import NodeRegExes

#from NodeRegExes import *
#from NodeBase import *
    
class EndSilentlyNode(NodeBase.SequenceNode):
    def __init__(self):
        #node variables here
        super().__init__()
        self.type = NodeBase.SequenceNodeType.endsilently
        self.typeString = "void"
        
        
    #factory method.. returns instance of class or None
    @staticmethod
    def tryIsNodeType(inputString):
        result = NodeRegExes.endSilentRegex.match(inputString)
        if result:
            return EndSilentlyNode()

    #instance method
    def javascriptOutputString(self):
        return '{"type":"void", "js":"gGameData.silently = false;"}'
