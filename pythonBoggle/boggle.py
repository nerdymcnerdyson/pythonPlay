import numpy
import pythonTrie
import time
#00 01 02 03
#04 05 06 07
#08 09 10 11
#12 13 14 15



class BoggleDie:
    def __init__(self):
        self.letters = []
        self.letters.append(['r','i','f','o','b','x'])
        self.letters.append(['i','f','e','h','e','y'])
        self.letters.append(['d','e','n','o','w','s'])
        self.letters.append(['u','t','o','k','n','d'])
        self.letters.append(['h','m','s','r','a','o'])
        self.letters.append(['l','u','p','e','t','s'])
        self.letters.append(['a','c','i','t','o','a'])
        self.letters.append(['y','l','g','k','u','e'])
        self.letters.append(['qu','b','m','j','o','a'])
        self.letters.append(['e','h','i','s','p','n'])
        self.letters.append(['v','e','t','i','g','n'])
        self.letters.append(['b','a','l','i','y','t'])
        self.letters.append(['e','z','a','v','n','d'])
        self.letters.append(['r','a','l','e','s','c'])
        self.letters.append(['u','w','i','l','r','g'])
        self.letters.append(['p','a','c','e','m','d'])
        

class BoggleBoard:
    def __init__(self, N, dictTrie):
        #for the first N letters, use the approved die randomly.. after.. grab another set of die Iguess?

        #shuffle die, put them on random face 
        letters = []
        dice = BoggleDie()
        diceList = dice.letters
        #numpy.random.shuffle(diceList)
        

        while len(letters) < N*N:
            numpy.random.shuffle(diceList)
            for die in diceList:
                numpy.random.shuffle(die)
                letters.append(die[0])
                if len(letters) >= N*N:
                    break
        #print letters
        self.letters = letters
        self.rows = N
        self.dictTrie =  dictTrie
        self.foundWords = {}


    def getNeighbors(self,n):
        row = n / self.rows
        col = n % self.rows
        #print row,col
        neighbors = []
        dirs = [-1,0,1]
        for dx in dirs:
            for dy in dirs:
                newRow = row + dy
                newCol = col + dx
                if newRow >= 0 and newRow < self.rows and newCol >= 0 and newCol < self.rows and (newRow != row or newCol != col):
                    #print 'adding', newCol, newRow
                    neighbors.append((newRow*self.rows) + newCol)
                    #print neighbors
        return neighbors

    def walkBoard(self, square,word, used):
        #print 'walking board for square:', square, 'with word', word, 'with used:', used
        myletter = self.letters[square]
        newWord = word+myletter
        newUsed = used+[square]
        #given this word, a) is it a word? and b) are there words with this root?
        wordId,remainingWords = self.dictTrie.getIdAndRootCountForString(newWord)
        #check word and root

        if wordId > 0 and len(newWord) > 2: 
            self.foundWords[newWord] = newUsed
        if remainingWords < 1:
            #print 'short cutting for root:', newWord, 'with remainingWords', remainingWords
            return

        



        neighbors = self.getNeighbors(square)
        for neighbor in neighbors:
            if neighbor not in used:
                self.walkBoard(neighbor, newWord,newUsed)




class Boggle:
    
    def __init__(self, n, dictTrie):
        self.n = n
        self.board = None
        self.dictTrie = dictTrie


    def createBoard(self):
        
        self.board = BoggleBoard(self.n, self.dictTrie)

    def walkBoard(self):
        for i in xrange(self.n*self.n):
            self.board.walkBoard(i,"",[])
        allWords = self.board.foundWords.keys()
        allWords.sort(key = len)
        print 'found', len(allWords), 'words'


        for word in allWords[-10:]:
            path = []
            for spot in self.board.foundWords[word]:
                path.append([spot/self.n, spot%self.n])
            print word, path

    def prettyPrintBoard(self):
        if not self.board:
            return
        for i in xrange(-1,self.n):
            if i != -1:
                spaces = '  '
                if i < 10:
                    spaces += ' '
                print i,spaces,
            else:
                print '     ',
            for j in xrange(self.n):
                if i == -1:
                    spaces = '  '
                    if j < 10:
                        spaces += ' '
                    print j,spaces,
                else:
                    letter = self.board.letters[i*self.n+j]
                    if len(letter) == 1:
                        letter += " "
                    print letter,'  ',
            print '\n'

def main():

    myTrie = pythonTrie.Trie()
    myTrie.processDict()

    boggleGame = Boggle(20, myTrie)

    for i in xrange(4):
        ts = time.time()
        boggleGame.createBoard()
        boggleGame.walkBoard()
        boggleGame.prettyPrintBoard()
        print 'processing records took', (time.time() - ts)

if __name__ == '__main__':
    main()

    
