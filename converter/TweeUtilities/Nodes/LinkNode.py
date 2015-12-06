#from . import NodeBase
#from . import NodeRegExes
from TweeUtilities.Nodes import *
import logging
        
class LinkNode(NodeBase.SequenceNode):
    def __init__(self, target, delay, text):
        self.type = NodeBase.SequenceNodeType.link
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
        links = NodeRegExes.LinkTokenRegex.findall(inputString)
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

    
