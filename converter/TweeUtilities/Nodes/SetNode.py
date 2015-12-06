#from . import NodeBase
#from . import NodeRegExes
from TweeUtilities.Nodes import *
import re

class SetNode(NodeBase.SequenceNode):
    def __init__(self, varName, varValue):
        #node variables here
        super().__init__()
        self.type = NodeBase.SequenceNodeType.setter

        self.varName = re.sub(variableNameReplacementRegEx,variableReplaceWith,varName)
#        print('varvalue:', varValue, varName)
        self.varValue = varValue.replace('"','\\"')
        
        
    #factory method.. returns instance of class or None
    @staticmethod
    def tryIsNodeType(inputString):
        result = setRegex.match(inputString)
        if result:
            return SetNode(result.group(1), result.group(2))

    #instance method
    def javascriptOutputString(self):
        return '{"type":"void", "js":"'+self.varName +' = '+self.varValue+';"}'


    # {"type": "if_block", "js": "gameData.story.hasknife == 1;"},
    # {"type": "text", "js": "\"I'll use my knife!\""},
    # {"type": "else_if_block", "js" : "gameData.story.hasspoon == 1;"},
    # {"type": "text", "js": "\"What can I do with a spoon?\""},
    # {"type": "else_block"},
    # {"type": "text", "js": "\"Oh no I didn't bring any cutlery with me!\""},
    # {"type": "endif_block"},
    
