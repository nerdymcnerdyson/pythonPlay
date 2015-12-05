import unittest

from converter import *


class TestStringTokenizer(unittest.TestCase):
    def id(self):
        return "general string tokenizer tests"

    def shortDescription(self):
        return "Tests the function that separates multiple nodes on the same line of text"


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
