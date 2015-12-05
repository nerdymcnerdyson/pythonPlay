from NodeRegExes import *
from NodeBase import *

class TextNode(SequenceNode):
    def __init__(self, inputString):
        #node variables here
        super().__init__()
        self.type = SequenceNodeType.text
        self.typeString = "text"
        self.content = inputString
#factory method.. returns instance of class or None
    @staticmethod
    def tryIsNodeType(inputString):
        #content
        return TextNode(inputString)
    #instance method
    def javascriptOutputString(self):
        return '{"type":"text", "js":"\\"'+self.content+'"\\";}'
