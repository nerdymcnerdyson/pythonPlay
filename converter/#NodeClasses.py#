import re
from enum import Enum


commandTokenRegex = re.compile('<<[\s\S]*?>>')

waypointRegex = re.compile('^::\\s*([\\w]+)')
silentRegex   = re.compile('<<silently>>')
endSilentRegex   = re.compile('<<endsilently>>')
setRegex         = re.compile('<<[\s]*set[\s]*\$([\S]+)[\s]*=[\s]*([\S]+)[\s]*>>')

ifRegex = re.compile('<<if([\s\S]*?)>>([\s\S]*)')
elseIfRegex = re.compile('<<elseif([\s\S]*?)>>([\s\S]*)')

#this is explicitly checking for two choices.. seems like a tricky reg ex to do otherwise
choiceRegex = re.compile('<<choice[\s]*\[\[([\s\S]*)\]\]>>[\s]*\|[\s]*<<choice[\s]*\[\[([\s\S]*)\]\]>>')


#choiceRegex      = re.compile('<<choice([\\s\\S]*)>>[\s]*|[\s]*<<choice([\\s\\S]*)>>')

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
    elseBlock = 10

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

class Action:
    def __init__(self, target, full, title, short):
        self.target = target
        self.full = full
        self.title = title
        self.short = short
    
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

        startChoiceToken = "<<choice"
        endChoiceToken = ">>"
        s = inputString
        first = startChoiceToken
        last = endChoiceToken
        
        choices = []
        try:
            while True:
                start = s.index( first ) + len( first )
                end = s.index( last, start )
                choices.append(s[start:end])
                s = s[end:]
        except ValueError:
            pass            #print('ranout of choices')

        if len(choices):
            actions = []
            for choice in choices:
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
        self.varName = varName
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
        return '{"type":"void", "js":"gGameData.story.'+self.varName +' = '+self.varValue+';"}'



class IfStartNode(SequenceNode):
    def __init__(self, conditional, remainder):
        self.conditional = conditional
        self.type = SequenceNodeType.ifStart
        self.remainder = remainder
    @staticmethod
    def tryIsNodeType(inputString):
        result = ifRegex.match(inputString)
        if result:
            return IfStartNode(result.group(1), result.group(2))
        
    #instance method
    def javascriptOutputString(self):
        return 'if conditional: %s remainder: %s'%(self.conditional, self.remainder)

class ElseIfNode(SequenceNode):
    def __init__(self, conditional, remainder):
        self.conditional = conditional
        self.type = SequenceNodeType.ifElse
        self.remainder = remainder
    @staticmethod
    def tryIsNodeType(inputString):
        result = elseIfRegex.match(inputString)
        if result:
            return ElseIfNode(result.group(1), result.group(2))
        
    #instance method
    def javascriptOutputString(self):
        return 'ifelse conditional: %s remainder: %s'%(self.conditional, self.remainder)

    
    
    
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
