from NodeRegExes import *
from NodeBase import *
from Utilities import *

class IfStartNode(SequenceNode):
    def __init__(self, conditional, remainder):
        self.conditional = gussyUpConditional(conditional)
        #self.varName = re.sub(variableNameReplacementRegEx,variableReplaceWith,varName)
        self.type = SequenceNodeType.ifStart
        self.remainder = remainder
    @staticmethod
    def tryIsNodeType(inputString):
        result = ifRegex.match(inputString)
        if result:
            return IfStartNode(result.group(1), result.group(2))
        
    #instance method
    def javascriptOutputString(self):
        return '{"type": "if_block, "js":"%s"}'%self.conditional

class ElseIfNode(SequenceNode):
    def __init__(self, conditional, remainder):
        self.conditional = gussyUpConditional(conditional)
        self.type = SequenceNodeType.ifElse
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
class ElseNode(SequenceNode):
    def __init__(self):
        self.type = SequenceNodeType.elseNode
    @staticmethod
    def tryIsNodeType(inputString):
        result = elseRegex.match(inputString)
        if result:
            return ElseNode()
    def javascriptOutputString(self):
        return '{"type": "else_block"}'

#endif node
class EndIfNode(SequenceNode):
    def __init__(self):
        self.type = SequenceNodeType.endIf
    @staticmethod
    def tryIsNodeType(inputString):
        result = endIfRegex.match(inputString)
        if result:
            return EndIfNode()
    def javascriptOutputString(self):
        return '{"type": "endif_block"}'

