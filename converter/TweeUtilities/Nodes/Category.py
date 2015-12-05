from Action import *

class Category:
    def __init__(self, identifier, actions):
        self.actions = actions
        self.identifier = identifier
        logger = logging.getLogger(__name__+"."+(type(self).__name__))
        
    def __str__(self):
        return "%s->%s"%(self.identifier, self.actions)

