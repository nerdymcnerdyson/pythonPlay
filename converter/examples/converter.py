#!/usr/bin/python3.4

import sys

sys.path.append('..')


import logging
import logging.config


from TweeUtilities import *

logging.config.fileConfig('../TweeUtilities/DefaultLogging.conf')

def main(inputFileName):
    logger = logging.getLogger(__name__)
    converter = TweeToLLJSConverter.TweeToLLJSConverter()
    converter.setInputFile(inputFileName)
    logger.info('beginning processing')
    converter.process()
    logger.info('writing to file')
    converter.outputWaypointsToFile("waypoints.converted.txt")
    converter.outputCategoriesToFile("categories.converted.txt")
    
if __name__ == '__main__':
    import sys
    inputFile = "../inputFiles/StoryData_en.txt"
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]
    main(inputFile)

