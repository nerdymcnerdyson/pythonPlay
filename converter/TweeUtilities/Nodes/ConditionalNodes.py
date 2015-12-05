from . import NodeBase
from . import NodeRegExes
from . import Utilities

from NodeRegExes import *
from NodeBase import *
from Utilities import *

class IfStartNode(NodeBase.SequenceNode):
    def __init__(self, conditional, remainder):
        self.conditional = Utilities.gussyUpConditional(conditional)
        #self.varName = re.sub(variableNameReplacementRegEx,variableReplaceWith,varName)
        self.type = NodeBase.SequenceNodeType.ifStart
        self.remainder = remainder
    @staticmethod
    def tryIsNodeType(inputString):
        result = NodeRegExes.ifRegex.match(inputString)
        if result:
            return IfStartNode(result.group(1), result.group(2))
        
    #instance method
    def javascriptOutputString(self):
        return '{"type": "if_block, "js":"%s"}'%self.conditional

class ElseIfNode(BaseNode.SequenceNode):
    def __init__(self, conditional, remainder):
        self.conditional = Utilities.gussyUpConditional(conditional)
        self.type = NodeBase.SequenceNodeType.ifElse
        self.remainder = remainder
    @staticmethod
    def tryIsNodeType(inputString):
        result = elseIfRegex.match(inputString)
        if result:
            return ElseIfNode(result.group(1), result.group(2))
        
    #instance method
    def javascriptOutputString(self):
        return '{"type": "if_else_block, "js":"%s"}'%self.conditional

#else node
class ElseNode(NodeBase.SequenceNode):
    def __init__(self):
        self.type = NodeBase.SequenceNodeType.elseNode
    @staticmethod
    def tryIsNodeType(inputString):
        result = NodeRegExes.elseRegex.match(inputString)
        if result:
            return ElseNode()
    def javascriptOutputString(self):
        return '{"type": "else_block"}'

#endif node
class EndIfNode(NodeBase.SequenceNode):
    def __init__(self):
        self.type = NodeBase.SequenceNodeType.endIf
    @staticmethod
    def tryIsNodeType(inputString):
        result = NodeRegexes.endIfRegex.match(inputString)
        if result:
            return EndIfNode()
    def javascriptOutputString(self):
        return '{"type": "endif_block"}'

