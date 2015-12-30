from sys import argv
import collections
import itertools
lines = open(argv[1],"rb")
support = argv[2]
bucketSize = argv[3]
singleFreqItemDict = {}
inputList = []

#Hash Function: sum of ascii values of all characters % 20
def generateHashFunc(pairList):
    hashedDict = dict()
    for eachpair in pairList:
        #print eachpair
        sumofchar = 0
        for i in range(0,len(eachpair)):
            #print eachpair[i]
            #print ord(eachpair[i])
            sumofchar += ord(eachpair[i])
        #print sumofchar
        hashedDict[repr(eachpair)] = sumofchar % int(bucketSize)
    #print "hashed dict is"
    #print hashedDict
    return hashedDict

def generateHashFunc2(pairList):
    hashedDict = dict()
    for eachpair in pairList:
        #print eachpair
        sumofchar = 1
        for i in range(0,len(eachpair)):
            #print eachpair[i]
            #print ord(eachpair[i])
            sumofchar *= int(ord(eachpair[i]))
        #print sumofchar
        hashedDict[repr(eachpair)] = sumofchar % int(bucketSize)
    #print "hashed dict is"
    #print hashedDict
    return hashedDict

def bitVectorGenerator(hashedBucketCountDict):
    for (k,v) in hashedBucketCountDict.items():
        if v >= int(support):
            bitVectorDict[k] = 1
        else:
            bitVectorDict[k] = 0
    return bitVectorDict

for line in lines:
    itemList = line.strip().split(',')
    inputList.append(list(itemList))
    for item in itemList:
        if item in singleFreqItemDict:
            val = singleFreqItemDict.get(item,0)
            singleFreqItemDict[item] = int(val) + 1
        else:
            singleFreqItemDict[item] = 1

#print singleFreqItemDict
#print inputList

singleFreqItemOrderedDict = collections.OrderedDict(sorted(singleFreqItemDict.items()))
singleFreqItemList = []

for (k,v) in singleFreqItemOrderedDict.items():
    if v >= int(support):
        singleFreqItemList.append(k)

print singleFreqItemList

def passesFunc(ctr, prevFrequentList):
    for eachInput in inputList:
        #print "each input is"
        #print sorted(eachInput)
        pairsList = list(itertools.combinations(sorted(eachInput), int(ctr)))
        pairsList = [x[0] if len(x) == 1 else list(x) for x in pairsList]
        #print "combinations are"
        #print pairsList
        for eachComb in pairsList:
            combinationsList.append(eachComb)
        hashedDict = generateHashFunc(pairsList)
        hashedDict2 = generateHashFunc2(pairsList)
        #print hashedDict
        for eachItem in hashedDict:
            if hashedDict[eachItem] in hashedBucketCountDict:
                cnt = hashedBucketCountDict.get(hashedDict[eachItem], 0)
                hashedBucketCountDict[hashedDict[eachItem]] = int(cnt) + 1
            else:
                hashedBucketCountDict[hashedDict[eachItem]] = 1

        for eachItem in hashedDict2:
            if hashedDict2[eachItem] in hashedBucketCountDict2:
                cnt = hashedBucketCountDict2.get(hashedDict2[eachItem], 0)
                hashedBucketCountDict2[hashedDict2[eachItem]] = int(cnt) + 1
            else:
                hashedBucketCountDict2[hashedDict2[eachItem]] = 1

    #print "final combinations are"
    #print sorted(combinationsList)
    #print hashedBucketCountDict


    bitVectorDict = bitVectorGenerator(hashedBucketCountDict)

    bitVectorDict2 = bitVectorGenerator(hashedBucketCountDict2)

    #print bitVectorDict
    #print "bit vector for hf2 is:"
    #print bitVectorDict2

    #pass 2
    finalFrequentList = list()
    prevCombination = []

    for eachCombination in sorted(combinationsList):
        if eachCombination not in finalFrequentList and eachCombination != prevCombination:
            prevCombination = eachCombination
            eachItemList = list(itertools.combinations(sorted(eachCombination), int(ctr)-1))
            eachItemList = [x[0] if len(x) == 1 else list(x) for x in eachItemList]
            #print eachCombination
            #print len(eachItemList)
            #print eachItemList
            cnt = 0
            for i in eachItemList:
                #print "i is"
                #print i
                if i in prevFrequentList:
                    #print "prevFreqList"
                    #print prevFrequentList
                    cnt += 1
            if cnt == len(eachItemList):  # i.e if all individuals items are also frequent
                sumofchar = 0
                prodofchar = 1
                for i in range(0,len(eachCombination)):
                    #print eachCombination[i]
                    #print ord(eachCombination[i])
                    sumofchar += ord(eachCombination[i])
                    prodofchar *= ord(eachCombination[i])
                #print sumofchar
                hashValue1 = sumofchar % int(bucketSize)
                hashValue2 = prodofchar % int(bucketSize)
                #print "hashValue is"
                #print hashValue
                if hashValue1 in bitVectorDict and hashValue2 in bitVectorDict2:
                    #print "pair is:"
                    #print eachCombination
                    bitVector1 = bitVectorDict[hashValue1]
                    bitVector2 = bitVectorDict2[hashValue2]
                    #print "bit vector is:"
                    #print bitVector
                    if int(bitVector1) == 1 and int(bitVector2) ==1:
                        cnt = sorted(combinationsList).count(eachCombination)
                        #print "its count is:"
                        #print cnt
                        if int(cnt) >= int(support):
                            #print eachCombination
                            finalFrequentList.append(eachCombination)
                            #print "final freq list appended"
                            #print finalFrequentList

    if len(finalFrequentList) == 0:
        finalFrequentList = []
    else:
        print "\n"
        print hashedBucketCountDict
        print hashedBucketCountDict2
        print finalFrequentList
    return finalFrequentList

finalFrequentList = list()
finalFrequentList = singleFreqItemList
ctr = 2

while finalFrequentList != []:
    hashedBucketCountDict = dict()
    hashedBucketCountDict2 = dict()
    combinationsList = list()
    prevFrequentList = finalFrequentList
    finalFrequentList = list()
    bitVectorDict = dict()
    bitVectorDict2 = dict()
    finalFrequentList = passesFunc(ctr,prevFrequentList)
    ctr += 1