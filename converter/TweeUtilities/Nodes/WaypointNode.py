#from . import NodeBase
#from . import NodeRegExes

from TweeUtilities.Nodes import *

class WaypointNode(SequenceNode):
    def __init__(self, waypointLabel):
        super().__init__()
        self.label = waypointLabel
        self.type = NodeBase.SequenceNodeType.waypoint
        
    @staticmethod
    def tryIsNodeType(inputString):
        result = waypointRegex.match(inputString)
        if result:
            return WaypointNode(result.group(1))
        return None

    def javascriptOutputString(self):
        return None
