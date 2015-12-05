from NodeRegExes import *
from NodeBase import *

import logging
        
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

    
