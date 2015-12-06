from . import NodeRegExes


import re

def gussyUpConditional(conditional):
    newConditional = re.sub(NodeRegExes.variableNameReplacementRegEx,NodeRegExes.variableReplaceWith,conditional)
    newConditional = re.sub('[\s]+is[\s]+', ' == ', newConditional)
    return newConditional
