import unittest

from converter import *


class TestDoNotSplitVariablesFromTextNodes(unittest.TestCase):
    def id(self):
        return "DoNotSplitVariablesFromTextNodes"

    def shortDescription(self):
        return "Makes sure that the string tokenizer works"

    def test_doNotSplitVariables_first(self):
        sampleLine = "<<$weapon>>! it's awesome!"
        sampleAnswer = ["<<$weapon>>! it's awesome!"]
        breakUp = breakUpStringIntoListOfTwineParts(sampleLine)
        self.assertEqual(sampleAnswer, breakUp)
        
    def test_doNotSplitVariable_middle(self):
        sampleLine = "check out my shiny <<$weapon>>! it's awesome!"
        sampleAnswer = ["check out my shiny <<$weapon>>! it's awesome!"]
        breakUp = breakUpStringIntoListOfTwineParts(sampleLine)
        self.assertEqual(sampleAnswer, breakUp)

    def test_doNotSplitVariableWithIf(self):
        sampleLine = "<<if $weapon>>check out my shiny <<$weapon>>! it's awesome!<<endif>>"
        sampleAnswer = ["<<if $weapon>>","check out my shiny <<$weapon>>! it's awesome!","<<endif>>"]
        breakUp = breakUpStringIntoListOfTwineParts(sampleLine)
        self.assertEqual(sampleAnswer, breakUp)

    def test_doNotSplitVariableWithIfOnElse(self):
        sampleLine = "<<if $weapon>>check out my shiny <<$weapon>><<endif>>"
        sampleAnswer = ["<<if $weapon>>","check out my shiny <<$weapon>>","<<endif>>"]
        breakUp = breakUpStringIntoListOfTwineParts(sampleLine)
        self.assertEqual(sampleAnswer, breakUp)

    def test_doNotSplitVariableWithIfOnIf(self):
        sampleLine = "<<if $weapon>><<$weapon>>is shiny!<<endif>>"
        sampleAnswer =["<<if $weapon>>","<<$weapon>>is shiny!","<<endif>>"]
        breakUp = breakUpStringIntoListOfTwineParts(sampleLine)
        self.assertEqual(sampleAnswer, breakUp)

    def test_doNotSplitVariableWithIfOnIf(self):
        sampleLine = "<<if $weapon>><<$weapon>><<endif>>"
        sampleAnswer =["<<if $weapon>>","<<$weapon>>","<<endif>>"]
        breakUp = breakUpStringIntoListOfTwineParts(sampleLine)
        self.assertEqual(sampleAnswer, breakUp)
        
    def test_doNotSplitVariables_last(self):
        sampleLine = "check out my <<$weapon>>"
        sampleAnswer = ["check out my <<$weapon>>"]
        breakUp = breakUpStringIntoListOfTwineParts(sampleLine)
        self.assertEqual(sampleAnswer, breakUp)

    def test_splitElse(self):
        sampleLine = "<<else>>It really WAS scary."
        sampleAnswer = ["<<else>>","It really WAS scary."]
        breakUp = breakUpStringIntoListOfTwineParts(sampleLine)
        self.assertEqual(sampleAnswer, breakUp)
