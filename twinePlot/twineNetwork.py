



import re


waypointRegex = re.compile('^::\\s*([\\w]+)')

outwardWaypointRegex = re.compile('\[\[\s*(\w+)\]\]')
choiceRegex = re.compile('\[\[[\W|\S]*?\|\s*(\w+)\s*\]\]')

#set
setRegex         = re.compile('<<[\s]*set[\s]*(\$[\S]+)[\s]*=[\s]*([\S]+)[\s]*>>')

#if
ifRegex = re.compile('<<if([\s\S]*?)>>')

#elseif
elseIfRegex = re.compile('<<elseif([\s\S]*?)>>')

elseRegex = re.compile('<<else>>')

#endif
endifRegex = re.compile('<<endif>>')

gameoverRegex = re.compile('gameover')




class TwineNode:
    def __init__(self):
        print 'you just made a node'

        

class TwineGraph:
    #this class is a graph of a twine story
    def __init__(self):
        print 'made a twine graph'


    def addNode(self, nodeName):
        print nodeName


def main():
#    storyfile = open('llbridge.txt', 'r')
    storyfile = open('StoryData_en.txt', 'r')




    currentWaypoint = None
    edgeNumber = 1
    currentIfCond = None
    currentElseIfConds = []
    isElse = False
    
    #also consider drawing nodes with info
    currentWaypointDesc = ""

    curIsGameOver = False
    
    print 'digraph G {'
    
    for line in storyfile:
        result = waypointRegex.match(line)
        if result:
#            print 'found WAYPOINT',result.group(1)
            if currentWaypoint:
                gameoverhelper = ""
                if curIsGameOver:
                    gameoverhelper = "color=red,"
                print '%s [shape=record,%slabel="%s"];'%(currentWaypoint,gameoverhelper,currentWaypointDesc)
            #but also, drop a node here
            currentWaypoint = result.group(1)
            currentIfCond = None
            currentElseIfConds = []
            isElse = False
            curIsGameOver = False
            #print 'is else to false'
            currentWaypointDesc = result.group(1)
        outboundResult = outwardWaypointRegex.findall(line)

        ifResult = ifRegex.findall(line)
        if ifResult:
            for ifThing in ifResult:
                currentWaypointDesc += ''.join(['\\nIF ',ifThing])
                currentIfCond = ifThing


        elseifResult = elseIfRegex.findall(line)
        if elseifResult:
            for elseifThing in elseifResult:

                currentElseIfConds.append(elseifThing)
                #print currentElseIfConds
                currentWaypointDesc += ''.join(['\\nELSEIF ',elseifThing])

        #endif, else todo
        elseResult = elseRegex.findall(line)
        if elseResult:
            #print 'found some else',elseResult
            for elseThing in elseResult:
                #print 'elsefired'
                #print 'setting isElse to true'
                isElse = True
                currentWaypointDesc += '\\nELSE'

        gameoverResult = gameoverRegex.findall(line)
        if gameoverResult:
            curIsGameOver = True

        endIfResult = endifRegex.findall(line)
        if endIfResult:
            for endIfThing in endIfResult:
                #print 'setting isElse to failse'
                isElse = False
                currentIfCond = None
                currentElseIfConds = []
                currentWaypointDesc += '\\nENDIF'
                
        setResult = setRegex.findall(line)
        if setResult:
            for setThing in setResult:
                #print ('='.join(setThing))
                setValue = ('='.join(setThing)).replace('"','\\"')
                currentWaypointDesc += ''.join(['\\nSET ',setValue])
                
        
        if outboundResult:
            for outbound in outboundResult:
                myEdgeNumber = edgeNumber
                edgeNumber += 1
                if isElse:
                    #print 'else was true!!!!'
                    elseProperties = "NOT"+"\\n NOT ".join([currentIfCond]+currentElseIfConds)
#                    print 'elseprops', elseProperties
                    edgeProperties = '[color=red, label="e:%d-%s"]'%(myEdgeNumber,elseProperties)
                elif len(currentElseIfConds) > 0:
 #                   print 'current elseif cond', currentElseIfConds
                    edgeProperties = '[color=red, label="e:%d-%s"]'%(myEdgeNumber,currentElseIfConds[-1])
                elif currentIfCond:
  #                  print 'current if cond', currentIfCond
                    edgeProperties = '[color=red,label="e:%d-%s"]'%(myEdgeNumber,currentIfCond)
                else:
                    edgeProperties = '[color=blue]'

                print currentWaypoint,'->',outbound,edgeProperties,';'
                currentWaypointDesc += "\\nredir:%s (%d)"%(outbound,myEdgeNumber)

        choiceresult = choiceRegex.findall(line)
        if choiceresult:
            choiceCount = 0
            for choice in choiceresult:
                myEdgeNumber = edgeNumber
                edgeNumber += 1
                choiceCount += 1
                if isElse:
                    #print 'else was true!!!!'
                    elseProperties = "NOT"+"\\n NOT ".join([currentIfCond]+currentElseIfConds)
#                    print 'elseprops', elseProperties
                    edgeProperties = '[color=red, label="e:%d-%s"]'%(myEdgeNumber,elseProperties)
                elif len(currentElseIfConds) > 0:
 #                   print 'current elseif cond', currentElseIfConds
                    edgeProperties = '[color=red, label="e:%d-%s"]'%(myEdgeNumber,currentElseIfConds[-1])
                elif currentIfCond:
  #                  print 'current if cond', currentIfCond
                    edgeProperties = '[color=red,label="e:%d-%s"]'%(myEdgeNumber,currentIfCond)
                else:
                    edgeProperties = '[color=blue]'


                print currentWaypoint,'->',choice,edgeProperties,';'
                currentWaypointDesc += "\\nchoice%d:%s (%d)"%(choiceCount,choice,myEdgeNumber)

    print 'first_encounter->shepherd_talk [color=green, label="EITHER"] ;'
    print 'first_encounter->key_talk [color=green, label="EITHER"] ;'
    print 'first_encounter->aries_talk [color=green, label="EITHER"] ;'
    print 'first_encounter->bos_talk [color=green, label="EITHER"] ;'
    print 'first_encounter->artesa_talk [color=green, label="EITHER"] ;'
    print '}'


if __name__=='__main__':
    main()
