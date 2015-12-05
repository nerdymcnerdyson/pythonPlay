#!/usr/bin/python3.4


import logging
import logging.config
from TweeToLLJSConverter import *

logging.config.fileConfig('ConverterLogging.conf')

def main(inputFileName):
    logger = logging.getLogger(__name__)
    converter = TweeToLLJSConverter()
    converter.setInputFile(inputFileName)
    logger.info('beginning processing')
    converter.process()
    logger.info('writing to file')
    converter.outputWaypointsToFile("waypoints.converted.txt")
    converter.outputCategoriesToFile("categories.converted.txt")
    
if __name__ == '__main__':
    import sys
    inputFile = "StoryData_en.txt"
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]
    main(inputFile)

