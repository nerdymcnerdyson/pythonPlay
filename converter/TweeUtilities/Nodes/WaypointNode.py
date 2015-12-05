from NodeRegExes import *
from NodeBase import *

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
