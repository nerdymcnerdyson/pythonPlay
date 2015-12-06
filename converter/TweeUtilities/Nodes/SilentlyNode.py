#from . import NodeBase
#from . import NodeRegExes
from TweeUtilities.Nodes import *    
class SilentlyNode(NodeBase.SequenceNode):
    def __init__(self):
        #node variables here
        super().__init__()
        self.type = NodeBase.SequenceNodeType.silently
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
