#!/usr/bin/python3.4

import re
import sys
from enum import Enum
from NodeClasses import *


class TweeToLLJSConverter:
    def __init__(self):
        self.currentWaypoint = None
        self.waypointNodes = []
        self.categories = {}

        self.nodeClassList = [WaypointNode, SilentlyNode, SetNode, EndSilentlyNode, ChoiceNode, IfStartNode, ElseIfNode, LinkNode]    
        
    def setInputFile(self, inputFileName):
        self.inputFile = openInputFile(inputFileName)
    

    def process(self):
        print('DOING ALL THE STUFF')
        for line in self.inputFile:
            line = line.strip()
        
            tokenList = breakUpStringIntoListOfTwineParts(line)

            for token in tokenList:
                thisNode = None
                if len(line) <= 0:
                    continue
                for nodeClass in self.nodeClassList:
                    thisNode = nodeClass.tryIsNodeType(line)
                    if thisNode:
                        break

                if not thisNode:
                    thisNode = TextNode.tryIsNodeType(line)
                print('%s for:\t\t %s'%(thisNode, token))
    


        

def main(inputFileName):

    converter = TweeToLLJSConverter()
    converter.setInputFile(inputFileName)
    converter.process()
    
    sys.exit()
    
    inputFile = openInputFile(inputFileName)

    currentWaypoint = None
    waypointNodes = []
    categories = {}
    
    nodeClassList = [WaypointNode, SilentlyNode, SetNode, EndSilentlyNode, ChoiceNode, IfStartNode, ElseIfNode]    
    for line in inputFile:
        line = line.strip()
        #print ('line processing:', line)
        tokenList = breakUpStringIntoListOfTwineParts(line)
        for token in tokenList:
            if len(line) <= 0:
                continue
            for nodeClass in nodeClassList:
                thisNode = nodeClass.tryIsNodeType(line)
                if thisNode:
                    break
            
            if thisNode:
                if thisNode.type == SequenceNodeType.waypoint:
                #print ('found waypoint: ', thisNode.type, thisNode.label)
                    if currentWaypoint:
                    #print('ending currentWaypoint', currentWaypoint)
                        print(currentWaypoint)
                        for node in waypointNodes:
                            print(node.javascriptOutputString())
                        
                    currentWaypoint = thisNode.label
                    waypointNodes = []
                else: #if this node type is waypoint
                    if thisNode.type == SequenceNodeType.choice:
                        categories[thisNode.identifier] = thisNode.category
                        waypointNodes.append(thisNode)
            else:
                node = TextNode.tryIsNodeType(line)
                waypointNodes.append(node)

            

        
        

    print(currentWaypoint)
    for node in waypointNodes:
        print(node.javascriptOutputString())

    print('\n\n\n and categories')
    for key,value in categories.items():
        print('\tkey', key)
        for action in value.actions:
            print('\t\t', action.title, action.target)
        
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



    #post process

    #look for variable nodes specifically

    keepGoing = True
    while keepGoing:
        keepGoing = False
        waypoints = [waypoint for waypoint in returnList if LinkTokenRegex.match(waypoint)]
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
    
    variables = [item for item in returnList if variableInTextRegex.match(item)]

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
            
            

            
        




        
    #find first command character
    #is link/choice at start?
    #are there any other control characters at start..
    #find next command token regex
    commandsOut = commandTokenGeneralRegex.split(inputString)

    
    
    

    


if __name__ == '__main__':
    import sys
    inputFile = "StoryData_en.txt"
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]
    main(inputFile)

