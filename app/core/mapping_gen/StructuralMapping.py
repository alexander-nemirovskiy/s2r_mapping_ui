from re import search


def cleanInput(inputlist):
    oplist = []
    originallist = []
    for i in inputlist:
        singlexsd = ''.join(i[0])
        singleowl = ''.join(i[1])
        count = i[2]
        classlist = [singlexsd, singleowl, count]
        classlistorg = [[singlexsd], [singleowl], count]
        oplist.append(classlist)
        originallist.append(classlistorg)
    return sorted(oplist), sorted(originallist)


def getIndex(inputList, s):
    index = 0
    for i in inputList:
        if s == i:
            index = inputList.index(i)
    return index


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
        classlist = []
        for i in xsdSchema.types[c].content.iter_elements():
            t = i.type
            elementname, p = getElement(i)
            elementtype, prefix = getElement(t)
            if prefix == ctype:
                innerlist = [c, elementname, elementtype]
                classlist.append(innerlist)
                for i in classlist:
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


# get domains for owl and xsd
def getDomains(sourceMatchList, targetMatchList):
    domaintmp = []
    indextmp = []
    for i in sourceMatchList:
        for j in targetMatchList:
            domainlist = [i[0], j[0]]
            indexlist = [i[0], i[3], j[0], j[3]]
            domaintmp.append(domainlist)
            indextmp.append(indexlist)
    domainres = list(set(map(lambda i: tuple(i), domaintmp)))
    outputDomain = [list(i) for i in domainres]
    indexres = list(set(map(lambda i: tuple(i), indextmp)))
    outputIndex = [list(i) for i in indexres]
    return outputDomain, outputIndex


# get ranges for owl and xsd
def getRanges(inputSourceList, inputTargetList):
    rangetmpl = []
    indextmpl = []
    for i in inputSourceList:
        for j in inputTargetList:
            rangelist = [i[2], j[2]]
            indexlist = [i[2], i[3], j[2], j[3]]
            rangetmpl.append(rangelist)
            indextmpl.append(indexlist)
    rangeres = list(set(map(lambda i: tuple(i), rangetmpl)))
    outputRanges = [list(i) for i in rangeres]
    indexres = list(set(map(lambda i: tuple(i), indextmpl)))
    outputIndex = [list(i) for i in indexres]
    return outputRanges, outputIndex


def matchPairToClass(inputpair, classlist):
    classmatch = []
    for q in inputpair:
        for j in classlist:
            x = all(item in j for item in q)
            if x:
                classmatch.append(q)
    return classmatch


def getIndexForMatchedClasses(inputMatchedRanges, rangesIndexes):
    indexlist = []
    for range in inputMatchedRanges:
        for cl in rangesIndexes:
            m = all(item in cl for item in range)
            if m:
                index = [cl[1], cl[3]]
                indexlist.append(index)
    return indexlist


def getOwlXsdProperties(inputIndexList, sourceTuple, targetTuple):
    owlToXsdPropertyMatch = []
    for i in inputIndexList:
        propertyowl = sourceTuple[i[0]][1]
        propertyxsd = targetTuple[i[1]][1]
        propertyList = [propertyowl, propertyxsd]
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


def getOwlXsdDomains(inputIndexList, sourceTuple, targetTuple):
    owlToXsdDomainMatch = []
    for i in inputIndexList:
        propertyowl = sourceTuple[i[0]][0]
        propertyxsd = targetTuple[i[1]][0]
        propertyList = [propertyowl, propertyxsd]
        owlToXsdDomainMatch.append(propertyList)
    domainres = list(set(map(lambda i: tuple(i), owlToXsdDomainMatch)))
    outputDomains = [list(i) for i in domainres]
    return outputDomains


def getOwlXsdRanges(inputIndexList, sourceTuple, targetTuple):
    owlToXsdRangeMatch = []
    for i in inputIndexList:
        propertyowl = sourceTuple[i[0]][2]
        propertyxsd = targetTuple[i[1]][2]
        propertyList = [propertyowl, propertyxsd]
        owlToXsdRangeMatch.append(propertyList)
    rangeres = list(set(map(lambda i: tuple(i), owlToXsdRangeMatch)))
    outputRanges = [list(i) for i in rangeres]
    return outputRanges
