

inputFile = open('insertinput.txt', 'r')

sizeOfArray = int(inputFile.readline())

arrayOfInts = [int(x) for x in inputFile.readline().split()]

#arrayOfInts = [2, 4, 6, 8, 3]




def printArray(ar):
    for i in ar:
        print i,
    print ''

def insertionSortStep(ar):

    arrayOfInts = ar
    lastValue = arrayOfInts[-1]
    for i in xrange((len(arrayOfInts)-2),-1,-1):

        if lastValue < arrayOfInts[i]:
            arrayOfInts[i+1] = arrayOfInts[i]
            #printArray(arrayOfInts)
        else:

            i += 1
            break

    arrayOfInts[i] = lastValue
    #printArray(arrayOfInts)



def insertionSort(ar):
    for i in xrange(2,len(ar)+1):
        #printArray(ar)
        small = ar[:i]

        insertionSortStep(small)

        ar = small + ar[i:]
        printArray(ar)



    
#realSort([7,2,6,3,9])
insertionSort([1,4,3,5,6,2])


insertionSort([2,4,6,8,3])
print '\n***'
insertionSort([2,3,4,5,6,7,8,9,10,1])
print '\n***'
insertionSort([1,2,3,4,6,7,8,9,10,5])
print '\n***'
insertionSort([1,2,3,4,6,7,8,9,10])


