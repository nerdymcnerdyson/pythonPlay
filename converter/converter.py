#!/usr/bin/python3.4


import logging
import logging.config
from TweeToLLJSConverter import *

logging.config.fileConfig('ConverterLogging.conf')

def main(inputFileName):
    converter = TweeToLLJSConverter()
    converter.setInputFile(inputFileName)
    converter.process()
    converter.outputWaypointsToFile("waypoints.converted.txt")
    converter.outputCategoriesToFile("categories.converted.txt")
    
if __name__ == '__main__':
    import sys
    inputFile = "StoryData_en.txt"
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]
    main(inputFile)

