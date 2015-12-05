import re

# class NodeRegExes:
#     def __init__(self):
#         return

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
