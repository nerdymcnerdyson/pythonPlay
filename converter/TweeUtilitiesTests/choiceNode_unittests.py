#!/usr/bin/python3.4

import unittest


from TweeUtilities import *
from TweeUtilities.TweeToLLJSConverter import *

class TestDoNotSplitVariablesFromTextNodes(unittest.TestCase):
    def id(self):
        return "DoNotSplitVariablesFromTextNodes"

    def shortDescription(self):
        return "Makes sure that the string tokenizer does not isolate variable commands"

    def test_doNotSplitVariables_first(self):
        sampleLine = "[[What was that?^What Was That Bro|what_yahhh]] | [[You okay?|okay_yahhh]]"

        sampleAnswer = ChoiceNode.tryIsNodeType(sampleLine)  

        
        self.assertNotEqual(sampleAnswer, None)


    def test_links(self):
        sampleLine = '[[delay 1h^Taylor is unconscious|awake_captured_drill_two]]'
        sampleAnswer = LinkNode.tryIsNodeType(sampleLine)
        # print(sampleAnswer.target)
        # print(sampleAnswer.delay)
        # print(sampleAnswer.text)
        # print(sampleAnswer.type)

        self.assertNotEqual(sampleAnswer, None)
        

if __name__ == '__main__':
    unittest.main()
