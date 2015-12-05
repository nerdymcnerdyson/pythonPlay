from . import NodeRegExes

from NodeRegExes import *
import re

def gussyUpConditional(conditional):
    newConditional = re.sub(variableNameReplacementRegEx,variableReplaceWith,conditional)
    newConditional = re.sub('[\s]+is[\s]+', ' == ', newConditional)
    return newConditional