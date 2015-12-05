from . import NodeBase
from . import NodeRegExes

from NodeRegExes import *
from NodeBase import *
    
class SilentlyNode(SequenceNode):
    def __init__(self):
        #node variables here
        super().__init__()
        self.type = SequenceNodeType.silently
        self.typeString = "void"
        
        
    #factory method.. returns instance of class or None
    @staticmethod
    def tryIsNodeType(inputString):
        result = silentRegex.match(inputString)
        if result:
            return SilentlyNode()

    #instance method
    def javascriptOutputString(self):
        return '{"type":"void", "js":"gGameData.silently = true;"}'
