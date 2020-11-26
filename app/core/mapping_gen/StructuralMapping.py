from re import search

def cleanInput(inputlist):
  oplist = []
  for i in inputlist:
    singlexsd = ''.join(i[0])
    singleowl = ''.join(i[1])
    count = i[2]
    originalPairList = [singlexsd,singleowl,count]
    oplist.append(originalPairList)
  return sorted(oplist)

def getIndex(inputList, s):
   index=0
   for i in inputList:
     if s == i:
       index = inputList.index(i)
   return index

# This function extracts name of elements and type using regular expressions
def getElement(inputString):
  s = str(inputString)
  match = search(r"'([^']*)", s)[0]
  outputElement = match.split(":", 1)[-1]
  prefix = search(r"[^(]+", s)[0]
  return outputElement, prefix

 # get Elements and their types for xsd Classes
def getXsdElements(inputClasses, xsdSchema):
  ctype = "XsdComplexType"
  outerlist = []
  for c in inputClasses:
   originalPairList = []
   for i in xsdSchema.types[c].content.iter_elements():
    t = i.type
    elementname, p = getElement(i)
    elementtype, prefix = getElement(t)
    if prefix == ctype:
     innerlist = [c, elementname, elementtype]
     originalPairList.append(innerlist)
     for i in originalPairList:
      outerlist.append(i)
  res = set(tuple(x) for x in outerlist)
  outputlist = [list(i) for i in res]
  finallist = sorted(outputlist)
  return finallist

 # get object properties of owl with domain and range
def getSplitStr(inputTerm):
  getStr = str(inputTerm)
  removeBracket = getStr.strip('[]')
  splitTerm = removeBracket.split('.')[-1]
  return splitTerm

#this function takes two tuples(1st and 2nd argument), third agrmunet refers to list containing pairs/
# which will be searched in two tuples.
def getClassMatchIndexList(inputSourceList, inputTargetList, searchitem):
  srcIndexList = []
  taregtIndexList = []
  indexowl = 0
  while indexowl < len(inputSourceList):
   if searchitem[0] == inputSourceList[indexowl][0]:
    o = []
    for i in inputSourceList[indexowl]:
     o.append(i)
    o.append(indexowl)
    o.append(searchitem[2])
    srcIndexList.append(o)
   indexowl = indexowl + 1
  indexxsd = 0
  while indexxsd < len(inputTargetList):
   if searchitem[1] == inputTargetList[indexxsd][0]:
    x = []
    for q in inputTargetList[indexxsd]:
     x.append(q)
    x.append(indexxsd)
    taregtIndexList.append(x)
   indexxsd = indexxsd + 1
  return srcIndexList, taregtIndexList

def getDomains(sourceMatchList, targetMatchList):
  domaintmp = []
  indextmp = []
  for i in sourceMatchList:
   for j in targetMatchList:
    domainlist = [i[0], j[0]]
    indexlist = [i[0], i[3],i[4], j[0], j[3]]
    domaintmp.append(domainlist)
    indextmp.append(indexlist)
  domainres = list(set(map(lambda i: tuple(i), domaintmp)))
  outputDomain = [list(i) for i in domainres]
  indexres = list(set(map(lambda i: tuple(i), indextmp)))
  outputIndex = [list(i) for i in indexres]
  return outputDomain, outputIndex



 # for given proprties , this function returns pairs of domains suggested as matching pair./
 #fisrt argumnet takes source tuple, second argument takes target tuple
def getDomainswithPenalty(sourceMatchList, targetMatchList):
  domaintmp = []
  for i in sourceMatchList:
   for j in targetMatchList:
    domainlist = [i[0], j[0], (i[4])*0.6]
    domaintmp.append(domainlist)
  return domaintmp


def getRangeswithPenalty(sourceMatchList, targetMatchList):
  rangetmp = []
  for i in sourceMatchList:
   for j in targetMatchList:
    rangelist = [i[2], j[2], (i[4])*0.6]
    rangetmp.append(rangelist)
  return rangetmp

 # for given proprties , this function returns pairs of ranges suggested as matching pair./
 #fisrt argumnet takes source tuple, second argument takes target tuple
def getRanges(inputSourceList, inputTargetList):
  rangetmpl = []
  indextmpl = []
  for i in inputSourceList:
   for j in inputTargetList:
    rangelist = [i[2], j[2]]
    indexlist = [i[2], i[3],i[4], j[2], j[3]]
    rangetmpl.append(rangelist)
    indextmpl.append(indexlist)
  rangeres = list(set(map(lambda i: tuple(i), rangetmpl)))
  outputRanges = [list(i) for i in rangeres]
  indexres = list(set(map(lambda i: tuple(i), indextmpl)))
  outputIndex = [list(i) for i in indexres]
  return outputRanges, outputIndex

#this function takes 1st argument as list of pairs(made and are expected to be found in orginal list of corresponsing pairs)./
#second argument is list of all the pairs(these are either class pair list, or properties pair list)
def matchPairToOrgPair(inputpair, originalPairList):
  classmatchwithscore=[]
  for q in inputpair:
   for j in originalPairList:
    x = all(item in j for item in q)
    if x:
     classmatchwithscore.append(j)
  return classmatchwithscore


#This fucntion takes 1st argument list of pairs(those which has been already matched to their corresponding supersets/
# and second argument takes list of range pairs along with confidence score and index. This function produce out/
# indexes and confidence scores of corresponding matchedpairs.
def getIndexForMatchedPairs(matchedRangesPair, rangesIndexes):
  indexlist = []
  for range in matchedRangesPair:
   for cl in rangesIndexes:
    if (range[0]== cl[0] and range[1]== cl[3]):
     index = [cl[1], cl[4], cl[2], range[2]]
     indexlist.append(index)
  return indexlist

#for given set of matched domain and ranges this function gives proprties match/
#first argument is list containing pairs of indexes and second and third arguments are
# those in which indexes will be searched.
def getOwlXsdProperties(inputIndexList, sourceTuple, targetTuple):
  owlToXsdPropertyMatch = []
  for i in inputIndexList:
   propertysrc = sourceTuple[i[0]][1]
   propertytarget = targetTuple[i[1]][1]
   confScore= (i[2]+i[3])/2
   propertyList = [propertysrc, propertytarget, confScore]
   owlToXsdPropertyMatch.append(propertyList)
  rangeres = list(set(map(lambda i: tuple(i), owlToXsdPropertyMatch)))
  outputRanges = [list(i) for i in rangeres]
  return outputRanges

 # seatch properties
def getPropertyMatch(sourceTuple, targetTuple, searchItem):
  owlpropList = []
  xsdpropList = []
  owlindex = 0
  xsdindex = 0
  while owlindex < len(sourceTuple):
   if searchItem[0] == sourceTuple[owlindex][1]:
    o = []
    for i in sourceTuple[owlindex]:
     o.append(i)
    o.append(owlindex)
    owlpropList.append(o)
    o.append(searchItem[2])
   owlindex = owlindex + 1
  while xsdindex < len(targetTuple):
   if searchItem[1] == targetTuple[xsdindex][1]:
    x = []
    for i in targetTuple[xsdindex]:
     x.append(i)
    x.append(xsdindex)
    xsdpropList.append(x)
   xsdindex = xsdindex + 1
  return owlpropList, xsdpropList

#for given set of matched ranges and properties this function gives domain match/
#first argument is list containing pairs of indexes and second and third arguments are
# those in which indexes will be searched.
def getOwlXsdDomains(inputIndexList, sourceTuple, targetTuple):
  owlToXsdDomainMatch = []
  for i in inputIndexList:
   propertyowl = sourceTuple[i[0]][0]
   propertyxsd = targetTuple[i[1]][0]
   confScore = (i[2] + i[3])/2
   propertyList = [propertyowl, propertyxsd, confScore]
   owlToXsdDomainMatch.append(propertyList)
  domainres = list(set(map(lambda i: tuple(i), owlToXsdDomainMatch)))
  outputDomains = [list(i) for i in domainres]
  return outputDomains


#for given set of matched domain and properties this function gives ranges  match/
#first argument is list containing pairs of indexes and second and third arguments are
# those in which indexes will be searched.
def getOwlXsdRanges(inputIndexList, sourceTuple, targetTuple):
  owlToXsdRangeMatch = []
  for i in inputIndexList:
    propertyowl = sourceTuple[i[0]][2]
    propertyxsd = targetTuple[i[1]][2]
    confScore = (i[2] + i[3])/2
    propertyList = [propertyowl, propertyxsd, confScore]
    owlToXsdRangeMatch.append(propertyList)
  rangeres = list(set(map(lambda i: tuple(i), owlToXsdRangeMatch)))
  outputRanges = [list(i) for i in rangeres]
  return outputRanges

#This function take a List of pairs and return unique elements at index 0
def getUniqueElements(inputPairList):
    uniqueElements = []
    [uniqueElements.append(i[0]) for i in inputPairList]
    uniqueElements = sorted(set(uniqueElements))
    return uniqueElements

#this Function matches two strings and if they matches it returns true and index in score list in other case false and -1
def matchPair(val0, val1, scorelist):
    index=-1
    for s in scorelist:
        index=index+1
        if(s[0]==val0 and s[1]==val1):
            return True, index
    return False, -1


#This Function takes PairList(Pair List along woth confidence score) number represnts the number of terms for each term at index0/
# For given Pairs this function filter out duplicate Piars and keep only one with highest Confidence score then for each term at index0/
#this returns only upto 3 mapping terms and those with high cond=fidence are selected.
def getMaxScorePairs(inputPaitList, uniqueElementList, number):
    outPutList=[]
    for i in uniqueElementList:
     tmpl = []
     for s in inputPaitList:
         if i == s[0]:
             tmpl.append(s)
     sortedlist = sorted(tmpl, key=lambda tmpl: tmpl[2], reverse=True)
     scores = [sortedlist[0]]
     for inner in sortedlist:
         dec, ind = matchPair(inner[0], inner[1], scores)
         if dec:
             if inner[2] > scores[ind][2]:
                 scores[ind][2] = inner[2]
         else:
             scores.append(inner)
     outPutList.extend(scores[:number])
    return outPutList
