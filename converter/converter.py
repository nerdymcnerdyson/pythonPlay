#!/usr/bin/python3.4

import re
import sys
from enum import Enum

#import NodeClasses
from NodeClasses import *

#read file
#gather way points

def main():
    print('hello world')
    inputFile = openInputFile('StoryData_en.ll2Real.txt')

    counter = 0

    currentWaypoint = None
    waypointNodes = []
    categories = {}
    
    nodeClassList = [WaypointNode, SilentlyNode, SetNode, EndSilentlyNode, ChoiceNode, IfStartNode, ElseIfNode]    
    for line in inputFile:
        line = line.strip()
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
            else:
                if thisNode.type == SequenceNodeType.choice:
                    categories[thisNode.identifier] = thisNode.category
                waypointNodes.append(thisNode)
        else:
            node = TextNode.tryIsNodeType(line)
            waypointNodes.append(node)

            

        
        counter += 1
        if counter > 250:
            break

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
    






if __name__ == '__main__':
    main()
