import re
import numpy as np
from .Preprocessing import getFileExtension
from .ReadWriteFiles import readXsdFile, readOntology, readTurtle, readXmlFile


def makeCompoundList(inputList):
    splittedList = [re.split('[ ]', w) for w in inputList]
    return splittedList


def matchCompound(inputList, modelVocabList):
    output = []
    for i in inputList:
        x = all(item in modelVocabList for item in i)
        if x:
            output.append(i)
    return output


def create2dMatrix(inputList):
    Output_array = np.asarray(inputList)
    return Output_array


def makeCompound2dArray(inputList):
    output_2dArray = []
    for i in inputList:
        rs = eval(i)
        output_2dArray.append(rs)
    return output_2dArray


def splitToList(inputList):
    final_list = []
    split_space = [re.split('[_|\s]+', w) for w in inputList]
    for x in split_space:
        split_CamelCase = [re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', i)).split() for i in x]
        flatten_list = [x for sublist in split_CamelCase for x in sublist]
        final_list.append(flatten_list)
    print("Compound list has been created")
    return final_list


def getMaxScoreNelements(inputMatchList, sourceList,number):
    finalList=[]
    for searchEl in sourceList:
        tmpl=[]
        for i in inputMatchList:
            if i[0]== searchEl:
                tmpl.append(i)
        sortedlist = sorted(tmpl, key=lambda tmpl: tmpl[2], reverse=True)
        finalList.extend(sortedlist[:number])
    return finalList

def matchPair(val0, val1, scorelist):
    index=-1
    for s in scorelist:
        if(s[0]==val0 and s[1]==val1):
            return True, index
    return False, -1



def readFile(path, filename):
    owl = 'owl'
    xsd = 'xsd'
    ttl = 'ttl'
    xml = 'xml'
    ext = getFileExtension(filename)
    if (ext == xsd):
        fileread = readXsdFile(path, filename)
        return fileread
    elif (ext == xml):
        fileread = readXmlFile(path, filename)
        return fileread
    elif (ext == owl):
        fileread = readOntology(path, filename)
        return fileread
    elif (ext == ttl):
        fileread = readTurtle(path, filename)
        return fileread