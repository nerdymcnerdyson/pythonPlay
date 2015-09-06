import time

# import sys
# sys.path.append('/usr/local/lib/python2.7/site-packages/')

# from graph_tool.all import *

GLOBAL_GRAPH = None

class TrieNode:
    nodeIDnum = 0
    def __init__(self, letter, parent):
        self.letter = letter
        self.parent = parent
        self.id = None
        self.children = {}
        self.kids = 0
        self.nodeId = TrieNode.nodeIDnum
        TrieNode.nodeIDnum += 1

    def processString(self, stringIn, stringId):
        if len(stringIn) == 0:
            self.id = stringId
            return
        self.children.setdefault(stringIn[0],TrieNode(stringIn[0], self))
        self.children[stringIn[0]].processString(stringIn[1:], stringId)
        self.kids += 1

    def getStringId(self, stringIn):
        if len(stringIn) == 0:
            return self.id
        childNode = self.children.get(stringIn[0], None)
        if not childNode:
            return None
        return childNode.getStringId(stringIn[1:])

    def getIdAndKidsForString(self, stringIn):
        if len(stringIn) == 0:
            return [self.id, self.kids]
        childNode = self.children.get(stringIn[0], None)
        if not childNode:
            return [-1, 0]
        return childNode.getIdAndKidsForString(stringIn[1:])

    def printReport(self,depth, startDepth):
        print self.letter
        indent = '\t' * (startDepth - depth)
        for letter in self.children.keys():
            print indent,letter, len(self.children[letter].children)
        if depth - 1 > 0:
            for child in self.children.values():
                child.printReport(depth-1, startDepth)


class Trie:
    def __init__(self):
        self.stringsIndexed = 0
        self.root = None

        
    def processString(self, stringIn, stringId):
        if len(stringIn) == 0:
            return 
        if self.root == None:
            self.root = TrieNode('*', 0)
        self.root.processString(stringIn,stringId)
        self.stringsIndexed += 1

    def getIdForString(self, stringIn):
        if self.root == None:
            return -1
        return self.root.getStringId(stringIn)


    def getIdAndRootCountForString(self, StringIn):
        if self.root == None:
            return [-1,-1]
        return self.root.getIdAndKidsForString(StringIn)



    def printRootReport(self, depth, startDepth):
        if not self.root:
            return
        self.root.printReport(depth, startDepth)
        
    def processDict(self):
        dictFile = open('pythonTrie/enable1.txt','r')
        count = 1
        ts = time.time()
        for line in dictFile:
            self.processString(line.lstrip().rstrip(), count)
            count += 1
        print 'processing records took', (time.time() - ts)
    





def getMysqlDatabaseEmails():
    import MySQLdb

    db = MySQLdb.connect(host="", # your host, usually localhost
                     user="root", # your username
                      passwd="stupidpandabear714", # your password
                      db="AMUsers") # name of the data base
    
    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor() 

    # Use all the SQL you like
    cur.execute("select email,pnum from aminno_member_email where char_length(email) > 0 limit 200000;")

    return cur


# def drawTreeWithGraphTool():
#     print 'drawing graph with', TrieNode.nodeIDnum, 'nodes'

#     global GLOBAL_GRAPH
#     GLOBAL_GRAPH = Graph()
#     #GLOBAL_GRAPH.add_vertex(TrieNode.nodeIDnum)
#     GLOBAL_GRAPH.add_vertex(12)
#     label = GLOBAL_GRAPH.new_edge_property("string")
#     e = GLOBAL_GRAPH.add_edge(0, 1)
#     label[e] = "A"
#     e = GLOBAL_GRAPH.add_edge(2, 3)
#     label[e] = "foo"
#     e = GLOBAL_GRAPH.add_edge(3, 1)
#     label[e] = "bar"
#     e = GLOBAL_GRAPH.add_edge(0, 3)
#     label[e] = "gnat"

#     graph_draw(GLOBAL_GRAPH, edge_text=label, edge_font_size=40, edge_text_distance=20, edge_marker_size=40, output="output.png")



# def main():
#     myTrie = Trie()

#     import time

#     ts = time.time()

#     DO_EMAIL = False
#     DO_DICT  = True

#     if DO_EMAIL:
#         emailList = getMysqlDatabaseEmails()
#         print 'getting email list took', (time.time() - ts)
#         ts = time.time()
    
#         for email in emailList:
#             myTrie.processString(email[0].lstrip().rstrip(), email[1])
#         print 'processing records took', (time.time() - ts)

#     elif DO_DICT:
#         dictFile = open('enable1.txt','r')
#         count = 1
#         ts = time.time()
#         for line in dictFile:
#             myTrie.processString(line.lstrip().rstrip(), count)
#             count += 1
#         print 'processing records took', (time.time() - ts)

#     drawTreeWithGraphTool()
        
            

# #     print 'this trie has processed', myTrie.stringsIndexed, 'strings'
        
# #     print 'getting ID for emailAddress bigdaddy200698@yahoo.com', myTrie.getIdForString('bigdaddy200698@yahoo.com')
# #     print 'getting ID for emailAddress pizza', myTrie.getIdForString('pizza')


# #     myTrie.printRootReport(2,2)
    
        
# if __name__ == '__main__':
#     main()
