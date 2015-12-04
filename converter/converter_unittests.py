#!/usr/bin/python3.4

import unittest

from converter import *


class TestDoNotSplitVariablesFromTextNodes(unittest.TestCase):
    def id(self):
        return "DoNotSplitVariablesFromTextNodes"

    def shortDescription(self):
        return "Makes sure that the string tokenizer does not isolate variable commands"

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


class TestStringMethods(unittest.TestCase):
    def id(self):
        return "spaces in breakup string"

    def shortDescription(self):
        return "check that the string returns empty strings"


    def test_basicTextLine(self):
        sampleLine = "Hello! herp derp! I'm Taylor!"
        sampleAnswer = [sampleLine]
        breakUp = breakUpStringIntoListOfTwineParts(sampleLine)
        self.assertEqual(sampleAnswer, breakUp)

    def test_splitElse(self):
        sampleLine = "<<else>>I don't have any weapons <<endif>>[[nextwaypoint]]"
        sampleAnswer = ["<<else>>","I don't have any weapons ","<<endif>>","[[nextwaypoint]]"]
        breakUp = breakUpStringIntoListOfTwineParts(sampleLine)
        self.assertEqual(sampleAnswer, breakUp)
                
    def test_ParseOutCommands(self):
          sampleLine = "<<else>>Gimme a minute to get dressed and make my way up to the cockpit...<<set $julia = true>> booga <<if $visited is true>>Hello mom!<<endif>>"
          sampleAnswer = ['<<else>>', 'Gimme a minute to get dressed and make my way up to the cockpit...', '<<set $julia = true>>', ' booga ', '<<if $visited is true>>', 'Hello mom!', '<<endif>>']
          breakUp = breakUpStringIntoListOfTwineParts(sampleLine)
          self.assertEqual(sampleAnswer, breakUp)


    def test_ParseOutLinks(self):
        sampleLine = "[[hI_there]]what is your name?[[othertext]]"
        sampleAnswer = ["[[hI_there]]","what is your name?","[[othertext]]"]

        breakUp = breakUpStringIntoListOfTwineParts(sampleLine)
        self.assertEqual(breakUp, sampleAnswer)

    def test_IgnoreStatusText(self):
        sampleLine = "[Taylor is sleeping] blahblah"
        sampleAnswer = ["[Taylor is sleeping] blahblah"]

        breakUp = breakUpStringIntoListOfTwineParts(sampleLine)
        self.assertEqual(breakUp, sampleAnswer)

    def test_linkInElseBlock(self):
        sampleLine = "<<else>>[[artesa_talk]]<<endif>>"
        sampleAnswer = ["<<else>>","[[artesa_talk]]","<<endif>>"]
        breakUp = breakUpStringIntoListOfTwineParts(sampleLine)
        self.assertEqual(breakUp, sampleAnswer)

    def test_incompleteLinkText(self):
        sampleLine = "[[Right. What else do you know?|freaky]] | [[They're headed toward you?|"

    def test_maintainTwoChoices(self):
        sampleLine = "[[What was that?|what_yahhh]] | [[You okay?|okay_yahhh]]"
        sampleAnswer = [sampleLine]
        breakUp = breakUpStringIntoListOfTwineParts(sampleLine)
        self.assertEqual(breakUp, sampleAnswer)

    def test_maintainThreeChoices(self):
        sampleLine = "[[What was that?|what_yahhh]] | [[You okay?|okay_yahhh]] | [[You okay_3?|okay_yahhh_2]]"
        sampleAnswer = [sampleLine]
        breakUp = breakUpStringIntoListOfTwineParts(sampleLine)
        self.assertEqual(breakUp, sampleAnswer)
        
if __name__ == '__main__':
    unittest.main()
