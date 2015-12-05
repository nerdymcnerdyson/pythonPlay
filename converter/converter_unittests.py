#!/usr/bin/python3.4

import unittest

from converter import *

import choiceNode_unittests
import stringTokenizer_unittests
import TestStringTokenizer
        
if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromModule(TestStringTokenizer)
    suite.addTests(unittest.TestLoader().loadTestsFromModule(stringTokenizer_unittests))
    suite.addTests(unittest.TestLoader().loadTestsFromModule(choiceNode_unittests))

    unittest.TextTestRunner(verbosity=0).run(suite)
    
