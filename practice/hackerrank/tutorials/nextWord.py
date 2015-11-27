












def makeNextString(inputString):
    inputList = [c for c in inputString]
#    print 'input',inputList
    if len(inputList) < 2:
        print 'no answer'
        return
    i = len(inputList)-1
    j = i - 1
    while (j >= 0):
        charA, charB = inputList[i], inputList[j]
        if charA > charB:
            #we've found the swap..
 #           print 'found swap', charB
            for k in xrange(i,len(inputList)):
                
                charC = inputList[k]
  #              print 'is ',charC,'a swappable char'
                if charC <= charB:
                    k = k - 1
                    break

   #         print 'decided on swapping for',inputList[j], 'and', inputList[k]
            inputList[j],inputList[k] = inputList[k],inputList[j] 
            leftOvers = inputList[j+1:]
            leftOvers.sort()
            inputList = inputList[:j+1]+leftOvers
            print ''.join(inputList)
            return
        i = j
        j = i - 1
    
    print 'no answer'

    




import sys
def main():

    for line in sys.stdin.readlines():
        line = line.strip()
        if line.isdigit():
            continue
        makeNextString(line)
    
    
if __name__ == '__main__':
    main()
