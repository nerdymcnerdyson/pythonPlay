
from enum import Enum

class SequenceNodeType(Enum):
    null = -1,
    waypoint = 1,
    silently = 2,
    endsilently = 3,
    setter = 4,
    text = 5,
    choice = 6,
    ifStart = 7
    ifElse = 8,
    endIf = 9,
    elseBlock = 10,
    link = 11,
    elseNode = 12

class SequenceNode:
    def __init__(self):
        #node variables here
        self.type = SequenceNodeType.null

    #factory method.. returns instance of class or None
    @staticmethod
    def tryIsNodeType(inputString):
        
        return None

    #instance method
    def javascriptOutputString():
        return ''

    def __repr__(self):
        return str(self.type)
    def __str__(self):
        return str(self.type)
