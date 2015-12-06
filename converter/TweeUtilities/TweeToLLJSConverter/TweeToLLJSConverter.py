


import logging
#from .. import Nodes

from TweeUtilities.Nodes import *


class TweeToLLJSConverter:
    def __init__(self):
        self.currentWaypoint = None
        self.waypointNodes = []
        self.categories = {}
        self.waypoints = {} # waypointName->nodelist
        
        self.nodeClassList = [
            WaypointNode,
            SilentlyNode,
            SetNode,
            EndSilentlyNode,
            ChoiceNode,
            ConditionalNodes.IfStartNode,
            ConditionalNodes.ElseIfNode,
            ConditionalNodes.ElseNode,
            ConditionalNodes.EndIfNode,
            LinkNode
        ]
        # create logger
        self.logger = logging.getLogger(__name__+"."+(type(self).__name__))

        # 'application' code
        # self.logger.debug('debug message')
        # self.logger.info('info message')
        # self.logger.warn('warn message')
        # self.logger.error('error message)
        # self.logger.critical('critical message')
        
        # self.logger.debug('boooooga')

        
    def setInputFile(self, inputFileName):
        self.logger.debug('opening input file: %s'%(inputFileName))
        self.inputFile = openInputFile(inputFileName)
        self.logger.debug('successfully opened: %s'%(inputFileName))
                
    def outputCategoriesToFile(self, outputFilename):
        self.logger.debug('outputting categories to: %s'%(outputFilename))
        outputFile = open(outputFilename, 'w')
        outputFile.write('[\n')
        isFirstCategory = True
        self.logger.info('outputting %d categories to file'%(len(self.categories)))
        for identifier, category in self.categories.items():
            self.logger.debug('writing category: %s'%(identifier))
            if not isFirstCategory:
                outputFile.write(',\n')
            isFirstCategory = False
            outputFile.write('{"actions":%s, "identifier":"%s"}'%(category.actions, category.identifier))
        outputFile.write('\n]\n')
        outputFile.close()
        
    def outputWaypointsToFile(self, outputFilename):
        outputFile = open(outputFilename,'w')
        outputFile.write('{\n')
        isFirstWaypoint = True
        for waypoint,nodelist in self.waypoints.items():
            if not isFirstWaypoint:
                outputFile.write(',\n')
            isFirstWaypoint = False
            outputFile.write('"'+waypoint+'":[\n')
            isFirstNode = True
            for node in nodelist:
                if not isFirstNode:
                    outputFile.write(',\n')
                isFirstNode = False    
                outputFile.write(str(node))
            outputFile.write('\n]')
        outputFile.write('\n}\n')
        outputFile.close()

    def process(self):
        self.logger.info("start processing")
        currentWaypoint = None
        for line in self.inputFile:
            line = line.strip()

            indexOfComments = line.find('//')
            if indexOfComments != -1:
                line = line[:indexOfComments]
            
            if len(line) == 0:
                continue
        
            
            tokenList = breakUpStringIntoListOfTwineParts(line)

            for token in tokenList:
                #print('processing token:', token)
                thisNode = None
                if len(token) <= 0:
                    continue
                for nodeClass in self.nodeClassList:
                    thisNode = nodeClass.tryIsNodeType(token)
                    if thisNode:
                        break
                if thisNode:
                    if thisNode.type == SequenceNodeType.waypoint:
                        if currentWaypoint:

                            #here check for duplicated waypoints

                            if currentWaypoint in self.waypoints.keys():
                                raise (DUPLICATEWAYPOINT,currentWaypoint,"exists twice")
                            
                            self.waypoints[currentWaypoint] = [node.javascriptOutputString() for node in waypointNodes]
                            
                            #print(currentWaypoint)
                            for node in waypointNodes:
                                #print(node.javascriptOutputString())
                                if node.type == SequenceNodeType.choice:
                                    #print category
     #                               print(node.category)
                                    self.categories[node.category.identifier] = node.category
                                    

                                    
                        currentWaypoint = thisNode.label
                        waypointNodes = []
                    else: #if this node type is waypoint
                        if thisNode.type == SequenceNodeType.choice:
                            self.categories[thisNode.identifier] = thisNode.category
                        waypointNodes.append(thisNode)
                        
                        
                else:
                    node = TextNode.tryIsNodeType(token)
                    waypointNodes.append(node)

                #if not thisNode:
                #    thisNode = TextNode.tryIsNodeType(token)
                #print('%s for:\t\t %s'%(thisNode, token))
    

        self.logger.info('End of parse..%d waypoints, %d categories'%(len(self.waypoints),len(self.categories)))


        
def openInputFile(inputFileName):
    #do some error checking here.. some day
    return open(inputFileName, 'r')
    

controlTokens = ["[[","<<", ">>","]]","::"]

def parseOutBlockWithDelimeter(inputString, delimeter):
    regex = None
    if delimeter == '[[':
        #is choice?
        #is link?
        regex = LinkTokenRegex
        pass
    elif delimeter == '<<':
        #is command?
        regex = commandTokenRegex
    result = regex.match(inputString)
    if result:
        return result.group(1)

    #we should probably freak out here
    return ''
    
def breakUpStringIntoListOfTwineParts(inputString):
    returnList = []
    commandStartTokens = {
        '<<':-1,
        '[[':-1,
    }
    #if len(inputString) <= 0:
    #    return []

    while len(inputString):
        #print('string is currently:',inputString)
        restartLoop = False
        for token in commandStartTokens.keys():
            #print('processing token:', token)
            position = inputString.find(token)
            
            if position == 0:
                restartLoop = True
                #print('found starting with token:',token)
                parsedBlock = parseOutBlockWithDelimeter(inputString, token)

                #if parsed out is empty.. what do?.. error condition
                if len(parsedBlock) == 0:
                    raise Exception("BAD PARSED BLOCK", inputString, token)
                
                #print('parsed out', parsedBlock)
                returnList.append(parsedBlock)
                #remove thing returned from string
                inputString = inputString[len(parsedBlock):]
                
            #print('found token %s at %d'%(token,position))
            commandStartTokens[token] = position
        if restartLoop:
            continue
        #print('no starting tokens')
        validPositions = [position for position in commandStartTokens.values() if position > -1]
        position = None
        if len(validPositions) == 0:
            position = len(inputString)
        else:
            position = min(validPositions)
        #print('position is:', position)
        returnList.append(inputString[:position])
        inputString = inputString[position:]

    keepGoing = True
    while keepGoing:
        keepGoing = False
        waypoints = [waypoint for waypoint in returnList if NodeRegExes.LinkTokenRegex.match(waypoint)]
        for waypoint in waypoints:
            
            waypointIndex = returnList.index(waypoint)
            if waypointIndex < (len(returnList)-2):
                stickIndex = waypointIndex + 1
                if returnList[stickIndex].strip() == '|':
                
                    nextPointIndex = stickIndex + 1
                    if returnList[nextPointIndex] in waypoints:
                  
                        keepGoing = True
                        returnList = (returnList[:waypointIndex]+
                                      [returnList[stickIndex].join([returnList[waypointIndex], returnList[nextPointIndex]])]+
                                      returnList[nextPointIndex+1:])
                        break
    
    variables = [item for item in returnList if NodeRegExes.variableInTextRegex.match(item)]

    if len(variables):
        for variable in variables:
            variableIndex = returnList.index(variable)
            if variableIndex > 0:
                preindex = variableIndex - 1
                if not (LinkTokenRegex.match(returnList[preindex])
                    or commandTokenRegex.match(returnList[preindex])):
                    #merge two things
                    
                    returnList = returnList[:preindex]+[(returnList[preindex]+returnList[variableIndex])]+returnList[variableIndex+1:]
                    #because we merged down, reduce one var index
                    variableIndex -= 1

            if variableIndex < (len(returnList)-1):
                postindex = variableIndex + 1
                #print ('in post! post is', returnList[postindex])
                
                if not (LinkTokenRegex.match(returnList[postindex])
                    or commandTokenRegex.match(returnList[postindex])):
                    #merge two things
                    #print ('POST MERGIN')
                    returnList = returnList[:variableIndex]+[(returnList[variableIndex]+returnList[postindex])]+returnList[postindex+1:]
    
            
    
    return returnList
