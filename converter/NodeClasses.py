import re
from enum import Enum
import logging

eitherRegex = re.compile('\[\[either\(("[\w|_|,|:]",?)+\)\]\]')


commandTokenRegex = re.compile('(<<[\\s\\S]*?>>)')
LinkTokenRegex = re.compile('[<<choice]?(\[\[[\\s\\S]*?\]\])[>>]?')

commandTokenGeneralRegex = re.compile('([<<|\[\[][\s\S]*?[>>|]]])')


unlimitedChoicesRegex = re.compile('[<<choice]?(\[\[[\w|\||\^]+\]\])[>>]?\|?')

waypointRegex = re.compile('^::\\s*([\\w]+)')


variableInTextRegex = re.compile('<<(\$[\w]+)>>')

outwardWaypointRegex = re.compile('\[\[\s*(\w+)\]\]')
choiceRegex = re.compile('\[\[[\W|\S]*?\|\s*(\w+)\s*\]\]')

elseRegex   = re.compile('<<else>>')

silentRegex   = re.compile('<<silently>>')
endSilentRegex   = re.compile('<<endsilently>>')
setRegex         = re.compile('<<[\s]*set[\s]*(\$[\S]+)[\s]*=[\s]*([\S]+)[\s]*>>')

endIfRegex = re.compile('<<endif>>')

ifRegex = re.compile('<<if([\s\S]*?)>>([\s\S]*)')
elseIfRegex = re.compile('<<elseif([\s\S]*?)>>([\s\S]*)')

variableNameReplacementRegEx = re.compile('\$')
variableReplaceWith = 'gGameData.story.'

class SequenceNodeType(Enum):
    null = -1,
    waypoint = 1,
    silently = 2,
    endsilently = 3,
    setter = 4,
    text = 5,
    choice = 6,
    ifStart = 7
    ifElse = 8,
    endIf = 9,
    elseBlock = 10,
    link = 11,
    elseNode = 12

class SequenceNode:
    def __init__(self):
        #node variables here
        self.type = SequenceNodeType.null

    #factory method.. returns instance of class or None
    @staticmethod
    def tryIsNodeType(inputString):
        
        return None

    #instance method
    def javascriptOutputString():
        return ''

    def __repr__(self):
        return str(self.type)
    def __str__(self):
        return str(self.type)

class SequenceNodeTemplate:
    def __init__(self):
        #node variables here
        super().__init__()
        self.type = SequenceNodeType.null
        
    #factory method.. returns instance of class or None
    @classmethod
    def tryIsNodeType():
        return None

    #instance method
    def javascriptOutputString():
        return ''



class TextNode(SequenceNode):
    def __init__(self, inputString):
        #node variables here
        super().__init__()
        self.type = SequenceNodeType.text
        self.typeString = "text"
        self.content = inputString
#factory method.. returns instance of class or None
    @staticmethod
    def tryIsNodeType(inputString):
        #content
        return TextNode(inputString)
    #instance method
    def javascriptOutputString(self):
        return '{"type":"text", "js":"\\"'+self.content+'"\\";}'


class Category:
    def __init__(self, identifier, actions):
#        print('making category', identifier, actions)
        self.actions = actions
        self.identifier = identifier
        logger = logging.getLogger(__name__+"."+(type(self).__name__))

        # 'application' code
        # logger.debug('debug message')
        # logger.info('info message')
        # logger.warn('warn message')
        # logger.error('error message')
        # logger.critical('critical message')

        
    def __str__(self):
        return "%s->%s"%(self.identifier, self.actions)


class Action:
    def __init__(self, target, full, title, short):
        self.target = target
        self.full = full
        self.title = title
        self.short = short

    def __repr__(self):
        return '{"destructive":0, "full":"%s", "title":"%s", "short":"%s","identifier":"%s"}'%(self.title, self.full, self.short, self.target)
        
class EitherNode(SequenceNode):
    def __init__(self, targetList):
        self.type = SequenceNodeType.either
        self.targetList = targetList

    def javascriptOutputString(self):
        return '{"type":"either","js":"%s"}'%','.join(self.targetList)

    
        
class LinkNode(SequenceNode):
    def __init__(self, target, delay, text):
        self.type = SequenceNodeType.link
        self.target = target
        self.delay = delay
        self.text = text
        logger = logging.getLogger(__name__+"."+(type(self).__name__))

        # 'application' code
        # logger.debug('debug message')
        # logger.info('info message')
        # logger.warn('warn message')
        # logger.error('error message')
        # logger.critical('critical message')

        #factory method.. returns instance of class or None
    @staticmethod
    def tryIsNodeType(inputString):
        links = LinkTokenRegex.findall(inputString)
        if len(links) == 0:
            return None
        choice = links[0]
        choice = choice.strip().strip('[').strip(']')
        shortEndIndex = choice.find('^')
        short = ""
        if shortEndIndex != -1:
            short = choice[:shortEndIndex]
            choice = choice[shortEndIndex+1:]
        breakIndex = choice.find('|')
        full = choice[:breakIndex]
        #if len(short) <= 0:
            #short = full
        target = choice[breakIndex+1:]
        return LinkNode(target, short,full)

    def javascriptOutputString(self):
        return '{"type":"link","js":"%s"}'%self.target

    
class ChoiceNode(SequenceNode):
    choiceCount = 0
    def __init__(self, identifier, category):
        self.type = SequenceNodeType.choice
        self.typeString = "void"
        self.identifier = identifier
        self.category = category

        #factory method.. returns instance of class or None
    @staticmethod
    def tryIsNodeType(inputString):

        #<<choice [[Uh... that <i>what</i> worked?|whatworked]]>> | <<choice [[What&apos;s happening here?|whatshappening]]>>
        #<<choice [[Sure, I do, but...^Sure, I understand them... but I don't understand why I'm seeing them.|surebutwhy]]>> | <<choice [[Yeah, I read English.|ireadenglish]]>>
        #[[short^full|target]]
        #try non-greedy parse
        #choice start token

        # startChoiceToken = "<<choice"
        # endChoiceToken = ">>"
        # s = inputString
        # first = startChoiceToken
        # last = endChoiceToken
        
        # choices = []
        # try:
        #     while True:
        #         start = s.index( first ) + len( first )
        #         end = s.index( last, start )
        #         choices.append(s[start:end])
        #         s = s[end:]
        # except ValueError:
        #     pass            #print('ranout of choices')


        choices = LinkTokenRegex.findall(inputString)

        
        if len(choices) >= 2:
            actions = []
            for choice in choices:
                #print('processing choice: ', choice)
                choice = choice.strip().strip('[').strip(']')
                shortEndIndex = choice.find('^')
                short = ""
                if shortEndIndex != -1:
                    short = choice[:shortEndIndex]
                    choice = choice[shortEndIndex+1:]
                breakIndex = choice.find('|')
                full = choice[:breakIndex]
                if len(short) <= 0:
                    short = full
                target = choice[breakIndex+1:]
                
                # print('\n***\nshort is', short)
                # print('full is', full)
                # print('target is', target)

                actions.append(Action(target, full, short, short))
            identifier = 'lifeline2'+str(ChoiceNode.choiceCount)
            
            ChoiceNode.choiceCount += 1
            newCategory = Category(identifier, actions)
            return ChoiceNode(identifier, newCategory)
        else:
            return None
                
        
        # #try result node parse.. 
        # result = choiceRegex.match(inputString)
        # if result:
        #     print('choicenode:',result.group(1),'\nchoice', result.group(2))
        #     return ChoiceNode(result.group(1))

    #instance method
    def javascriptOutputString(self):
        return '{"type":"choice","js":"%s"}'%self.identifier

    

    
class SilentlyNode(SequenceNode):
    def __init__(self):
        #node variables here
        super().__init__()
        self.type = SequenceNodeType.silently
        self.typeString = "void"
        
        
    #factory method.. returns instance of class or None
    @staticmethod
    def tryIsNodeType(inputString):
        result = silentRegex.match(inputString)
        if result:
            return SilentlyNode()

    #instance method
    def javascriptOutputString(self):
        return '{"type":"void", "js":"gGameData.silently = true;"}'

class EndSilentlyNode(SequenceNode):
    def __init__(self):
        #node variables here
        super().__init__()
        self.type = SequenceNodeType.endsilently
        self.typeString = "void"
        
        
    #factory method.. returns instance of class or None
    @staticmethod
    def tryIsNodeType(inputString):
        result = endSilentRegex.match(inputString)
        if result:
            return EndSilentlyNode()

    #instance method
    def javascriptOutputString(self):
        return '{"type":"void", "js":"gGameData.silently = false;"}'

class SetNode(SequenceNode):
    def __init__(self, varName, varValue):
        #node variables here
        super().__init__()
        self.type = SequenceNodeType.setter

        self.varName = re.sub(variableNameReplacementRegEx,variableReplaceWith,varName)
#        print('varvalue:', varValue, varName)
        self.varValue = varValue.replace('"','\\"')
        
        
    #factory method.. returns instance of class or None
    @staticmethod
    def tryIsNodeType(inputString):
        result = setRegex.match(inputString)
        if result:
            return SetNode(result.group(1), result.group(2))

    #instance method
    def javascriptOutputString(self):
        return '{"type":"void", "js":"'+self.varName +' = '+self.varValue+';"}'


    # {"type": "if_block", "js": "gameData.story.hasknife == 1;"},
    # {"type": "text", "js": "\"I'll use my knife!\""},
    # {"type": "else_if_block", "js" : "gameData.story.hasspoon == 1;"},
    # {"type": "text", "js": "\"What can I do with a spoon?\""},
    # {"type": "else_block"},
    # {"type": "text", "js": "\"Oh no I didn't bring any cutlery with me!\""},
    # {"type": "endif_block"},
    

def gussyUpConditional(conditional):
    newConditional = re.sub(variableNameReplacementRegEx,variableReplaceWith,conditional)
    newConditional = re.sub('[\s]+is[\s]+', ' == ', newConditional)
    return newConditional
    
class IfStartNode(SequenceNode):
    def __init__(self, conditional, remainder):
        self.conditional = gussyUpConditional(conditional)
        #self.varName = re.sub(variableNameReplacementRegEx,variableReplaceWith,varName)
        self.type = SequenceNodeType.ifStart
        self.remainder = remainder
    @staticmethod
    def tryIsNodeType(inputString):
        result = ifRegex.match(inputString)
        if result:
            return IfStartNode(result.group(1), result.group(2))
        
    #instance method
    def javascriptOutputString(self):
        return '{"type": "if_block, "js":"%s"}'%self.conditional

class ElseIfNode(SequenceNode):
    def __init__(self, conditional, remainder):
        self.conditional = gussyUpConditional(conditional)
        self.type = SequenceNodeType.ifElse
        self.remainder = remainder
    @staticmethod
    def tryIsNodeType(inputString):
        result = elseIfRegex.match(inputString)
        if result:
            return ElseIfNode(result.group(1), result.group(2))
        
    #instance method
    def javascriptOutputString(self):
        return '{"type": "if_else_block, "js":"%s"}'%self.conditional

#else node
class ElseNode(SequenceNode):
    def __init__(self):
        self.type = SequenceNodeType.elseNode
    @staticmethod
    def tryIsNodeType(inputString):
        result = elseRegex.match(inputString)
        if result:
            return ElseNode()
    def javascriptOutputString(self):
        return '{"type": "else_block"}'

#endif node
class EndIfNode(SequenceNode):
    def __init__(self):
        self.type = SequenceNodeType.endIf
    @staticmethod
    def tryIsNodeType(inputString):
        result = endIfRegex.match(inputString)
        if result:
            return EndIfNode()
    def javascriptOutputString(self):
        return '{"type": "endif_block"}'


    
class WaypointNode(SequenceNode):
    def __init__(self, waypointLabel):
        super().__init__()
        self.label = waypointLabel
        self.type = SequenceNodeType.waypoint
        
    @staticmethod
    def tryIsNodeType(inputString):
        result = waypointRegex.match(inputString)
        if result:
            return WaypointNode(result.group(1))
        return None

    def javascriptOutputString(self):
        return None
