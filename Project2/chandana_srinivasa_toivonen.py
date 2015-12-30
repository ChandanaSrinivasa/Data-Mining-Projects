from sys import argv
import random
import collections
import itertools
import ast

def candidateSetGeneration(freqItemset, numbr):
    #print freqItemset
    mergedFreqISet = list(set(itertools.chain(*[n[0] if len(n) == 1 else n for n in freqItemset])))
    candidateSet = []
    #print mergedFreqISet
    mergedListCombinations = list(itertools.combinations(sorted(mergedFreqISet), int(numbr)))
    mergedListCombinations = [x[0] if len(x) == 1 else list(x) for x in mergedListCombinations]
    #print mergedListCombinations
    for eachMergedListCombination in mergedListCombinations:
        subsetsOfMergedListCombination = list(itertools.combinations(sorted(eachMergedListCombination),int(numbr-1)))
        subsetsOfMergedListCombination = [x[0] if len(x) == 1 else list(x) for x in subsetsOfMergedListCombination]
        #print subsetsOfMergedListCombination
        cntr = 0
        for eachSubsetItem in subsetsOfMergedListCombination:
            #print eachSubsetItem
            if eachSubsetItem in freqItemset:
                #print "present in freqItemset"
                cntr +=1
        if int(cntr) == len(subsetsOfMergedListCombination):
            candidateSet.append(eachMergedListCombination)
    #print(candidateSet)
    return candidateSet

def candidatePairDictWithCount(randomItemList, num):
    #print "random item list is "
    #print randomItemList
    for eachRandomSampleList in randomItemList:
        allPairsList = list(itertools.combinations(sorted(eachRandomSampleList), num))
        allPairsList = [repr(list(x)) for x in allPairsList]
        #print allPairsList
        for eachItem in sorted(allPairsList):
                if eachItem in candidatePairDict:
                    val = candidatePairDict.get(eachItem,0)
                    candidatePairDict[eachItem] = int(val) + 1
                else:
                    candidatePairDict[eachItem] = 1
    return candidatePairDict


def negativeBorderGen(list_of_freq_items,list_of_non_freq_items, prevFreqItemSet, num):
    #print "in negative border func:"
    #print "list_of_non_freq_items"
    #print list_of_non_freq_items
    #print "list_of_freq_items"
    #print list_of_freq_items
    #print "prevFreqItemSet"
    #print prevFreqItemSet
    negativeBorderList = []
    if num == 1:
        negativeBorderList = list_of_non_freq_items
    else:
        for eachItem in list_of_non_freq_items:
            subsetList = list(itertools.combinations(sorted(eachItem), num-1))
            subsetList = [x[0] if len(x) == 1 else list(x) for x in subsetList]
            #print "subList:"
            #print subsetList
            cnt = 0
            for eachSubListItem in subsetList:
                if eachSubListItem in prevFreqItemSet:
                    cnt +=1
            if cnt == len(subsetList):
                negativeBorderList.append(repr(eachItem))
    #print "Negative Border Item Sets"
    #print negativeBorderList
    combinationsDict = {}
    for eachInputList in inputList:
        inputListCombinations = list(itertools.combinations(sorted(eachInputList), num))
        inputListCombinations = [repr(x[0]) if len(x) == 1 else repr(list(x)) for x in inputListCombinations]
        #print inputListCombinations
        #print inputListCombinations
        for eachcomb in inputListCombinations:
            if eachcomb in list_of_freq_items or eachcomb in negativeBorderList:
                if eachcomb in combinationsDict:
                    val = combinationsDict.get(eachcomb,0)
                    combinationsDict[eachcomb] = val + 1
                else:
                    combinationsDict[eachcomb] = 1
    #print "combinations dict is"
    #print collections.OrderedDict(sorted(combinationsDict.items()))
    freqPairsInWholeDataList = []
    for (k,v) in combinationsDict.items():
        if v >= int(support):
            freqPairsInWholeDataList.append(k)
    #print "frequent items in whole data:"
    #print sorted(freqPairsInWholeDataList)
    cntNegBor = 0
    for eachNegBorder in negativeBorderList:
        if eachNegBorder in freqPairsInWholeDataList:
            cntNegBor +=1
    if cntNegBor == 0:
        #print "correct item set found. exit"
        return (0,[ast.literal_eval(n) for n in sorted(freqPairsInWholeDataList)]);
    else:
        #print "repeat with different sample"
        return (1,[ast.literal_eval(n) for n in sorted(freqPairsInWholeDataList)]);

lines = open(argv[1],"rb")
support = argv[2]

inputList = list()
singleItemDict_C1 = dict()
scaledSupport = int(0.5 * 0.8 * int(support))

#print "scaled support is: " + str(scaledSupport)

for line in lines:
    itemList = line.strip().split(',')
    inputList.append(list(itemList))

#print "input list is"
#print inputList

flag = 1
itrcnt = 0

while(flag):
    itrcnt += 1
    randomItemList = []
    for i in range(0,int(0.5*len(inputList))):
        randomItemList.append(inputList[random.randint(0, len(inputList)-1)])

    #print "random sampled list"
    #print randomItemList
    #print len(randomItemList)

    for eachList in sorted(randomItemList):
        for item in eachList:
            if item in singleItemDict_C1:
                val = singleItemDict_C1.get(item,0)
                singleItemDict_C1[item] = int(val) + 1
            else:
                singleItemDict_C1[item] = 1

    #print "C1"
    #print singleItemDict_C1

    singleFreqItemOrderedDict = collections.OrderedDict(sorted(singleItemDict_C1.items()))
    singleFreqItemList_L1 = []
    singleNonFreqItemList = []
    candidatePairDict = {}

    for (k,v) in singleFreqItemOrderedDict.items():
        if v >= int(scaledSupport):
            singleFreqItemList_L1.append(k)
        else:
            singleNonFreqItemList.append(k)

    #print "freq item list"
    #print singleFreqItemList_L1

    #print "non freq item list"
    #print singleNonFreqItemList

    true_freq_items_list = []

    cntOnEntireDataSet = {}

    for eachList in inputList:
        for eachItem in eachList:
            if eachItem in singleFreqItemList_L1 or eachItem in singleNonFreqItemList:
                if eachItem in cntOnEntireDataSet:
                    val = cntOnEntireDataSet.get(eachItem,0)
                    cntOnEntireDataSet[eachItem] = val + 1
                else:
                    cntOnEntireDataSet[eachItem] = 1

    #print "cnt on entire data set"
    #print cntOnEntireDataSet
    freqPairsInWholeDataList = []
    for (k,v) in cntOnEntireDataSet.items():
        if v >= int(support):
            freqPairsInWholeDataList.append(k)
    #print "frequent items in whole data:"
    #print sorted(freqPairsInWholeDataList)

    cntNegBor = 0
    for eachNegBorder in singleNonFreqItemList:
        if eachNegBorder in freqPairsInWholeDataList:
            cntNegBor +=1
    if cntNegBor == 0:
        #print "correct item set found. exit"
        true_freq_items = freqPairsInWholeDataList
        true_freq_items_list.append([list(x) for x in freqPairsInWholeDataList])
        #print [list(x) for x in true_freq_items]
        flag = 0
    else:
        #print "repeat with different sample"
        flag = 1

    i = 2
    while flag == 0 and true_freq_items != []:

        pairsList_C2 = candidateSetGeneration(true_freq_items, i)

        #print "C2"
        #print(pairsList_C2)


        candidatePairDict = candidatePairDictWithCount(randomItemList, i)

        #print "random list with count"
        #print collections.OrderedDict(candidatePairDict)
        pairsList_L2 = []
        nonFreqItemList = []
        pairsList_C2_str = [repr(n) for n in pairsList_C2]

        for eachPair in pairsList_C2_str:
            if eachPair in candidatePairDict and candidatePairDict[eachPair] >= int(scaledSupport):
                pairsList_L2.append(eachPair)
            else:
                nonFreqItemList.append(eachPair)

        #print "Frequent Item List:"
        #print pairsList_L2

        #print "Non Frequent Item List:"
        #print nonFreqItemList

        (flag,true_freq_items) = negativeBorderGen(pairsList_L2,[ast.literal_eval(n) for n in nonFreqItemList], true_freq_items,i)

        if flag == 0 and true_freq_items != []:
            #print "L2"
            #print [ast.literal_eval(n) for n in pairsList_L2]
            #print true_freq_items
            true_freq_items_list.append(true_freq_items)
            i +=1
        #candidateSetGeneration(pairsList_L2, 3)


print itrcnt
print 0.5
for eachTrueFreqList in true_freq_items_list:
    print sorted(eachTrueFreqList)
    print "\n"