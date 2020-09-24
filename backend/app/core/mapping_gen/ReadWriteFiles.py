import logging
from pathlib import Path

import numpy as np
import csv
import xml.dom.minidom as xp
from rdflib import Graph
from re import sub, findall
from re import split as re_split
import xml.etree.ElementTree as ET
from owlready2 import get_ontology


def readcsv(filepath):
    datafile = open(filepath, 'r')
    datareader = csv.reader(datafile)
    data = []
    for row in datareader:
        data.append(row)
    return data


def readTextFile(filePath):
    file = open(filePath, 'r')
    outputList = file.read().split('\n')
    return outputList


def readXmlFile(xml_path, xml_name):
    cleaned_elem_list = []
    # xml_file = xml_path + xml_name
    xml_file = Path.joinpath(xml_path, xml_name)
    tree = ET.parse(str(xml_file))
    root = tree.getroot()
    elem_list = [elem.tag for elem in root.iter()]
    for elem in elem_list:
        cleaned_elem = sub('{.*?}', '', elem)
        splitted_elem = findall('[A-Z][^A-Z]*', cleaned_elem)
        for se in splitted_elem:
            cleaned_elem_list.append(se)
    finaList = list(dict.fromkeys(cleaned_elem_list))
    return finaList


def clean_split_elem_list(elem_list):
    cleaned_elem_list = []
    for elem in elem_list:
        cleaned_elem = sub('{.*?}', '', elem)
        splitted_elem = findall('[A-Z][^A-Z]*', cleaned_elem)
        for se in splitted_elem:
            cleaned_elem_list.append(se)
    return cleaned_elem_list


def getElementandAttribute(doc, attr):
    readElement = doc.getElementsByTagName(attr)
    listElement = []
    for m in readElement:
        f = m.getAttribute('name')
        listElement.append(f)
    return listElement


def getElementandAttributeType(doc, attr):
    readElement = doc.getElementsByTagName(attr)
    listElement = []
    for m in readElement:
        f = m.getAttribute('type')
        listElement.append(f)
    return listElement


def getElementandAttributeNameType(doc, attr):
    readElement = doc.getElementsByTagName(attr)
    listElement = []
    for m in readElement:
        elName = m.getAttribute('name')
        elAttr = m.getAttribute('type')
        tmpl = [elName, elAttr]
    listElement.append(tmpl)
    return listElement


def readElementAndAttribute(filepath, filename):
    p = Path.joinpath(filepath, filename)
    docread = xp.parse(str(p))
    getElement = getElementandAttributeNameType(docread, 'xsd:element')
    getAttribute = getElementandAttributeNameType(docread, 'xsd:attribute')

    listofElements = list(filter(lambda x: x != '', getElement))
    finallistofElements = list(dict.fromkeys(listofElements))

    listofAttributes = list(filter(lambda x: x != '', getAttribute))
    finallistofAttributes = list(dict.fromkeys(listofAttributes))
    return finallistofElements, finallistofAttributes


def readXsdFile(filepath, filename):
    p = Path.cwd().joinpath(filepath, filename)
    logging.warning('ATTENTION!! Reading from: ' + str(p))

    docread = xp.parse(str(p))
    getElement1 = getElementandAttribute(docread, 'xs:element')
    getElement2 = getElementandAttribute(docread, 'xsd:element')
    getElement3 = getElementandAttribute(docread, 'xs:attribute')
    getElement4 = getElementandAttribute(docread, 'xsd:attribute')
    getElement5 = getElementandAttribute(docread, 'xsd:complexType')
    getElement1.extend(getElement2 + getElement3 + getElement4 + getElement5)
    listofElements = list(filter(lambda x: x != '', getElement1))
    finallist = list(dict.fromkeys(listofElements))
    return finallist


def readXsdFilecomplextype(filepath, filename):
    p = Path.joinpath(filepath, filename)
    docread = xp.parse(str(p))
    getElement = getElementandAttribute(docread, 'xsd:complexType')
    listofElements = list(filter(lambda x: x != '', getElement))
    finallist = list(dict.fromkeys(listofElements))
    return finallist


def readXsdFileElementAttribute(filepath, filename):
    p = Path.joinpath(filepath, filename)
    docread = xp.parse(str(p))
    getElement1 = getElementandAttribute(docread, 'xsd:element')
    getElement2 = getElementandAttribute(docread, 'xsd:attribute')
    getElement1.extend(getElement2)
    listofElements = list(filter(lambda x: x != '', getElement1))
    finallist = list(dict.fromkeys(listofElements))
    return finallist


def readOntology(filepath, filename):
    p = Path.cwd().joinpath(filepath, filename)
    onto = get_ontology(str(p)).load()
    clist1 = list(onto.classes())
    clist2 = list(onto.properties())
    strlist1 = [str(i) for i in clist1]
    strlist2 = [str(i) for i in clist2]
    final_term1 = [re_split('[.]', w)[-1] for w in strlist1]
    final_term2 = [re_split('[.]', w)[-1] for w in strlist2]
    final_term = final_term1 + final_term2
    finallist = list(dict.fromkeys(final_term))
    return finallist


def readOntologyClass(filepath, filename):
    p = Path.joinpath(filepath, filename)
    onto = get_ontology(str(p)).load()
    clist1 = list(onto.classes())
    strlist1 = [str(i) for i in clist1]
    final_term1 = [re_split('[.]', w)[-1] for w in strlist1]
    finallist = list(dict.fromkeys(final_term1))
    return finallist


def readOntologyProperty(filepath, filename):
    p = Path.joinpath(filepath, filename)
    onto = get_ontology(str(p)).load()
    clist2 = list(onto.properties())
    strlist2 = [str(i) for i in clist2]
    final_term2 = [re_split('[.]', w)[-1] for w in strlist2]
    finallist = list(dict.fromkeys(final_term2))
    return finallist


def readTurtle(filepath, filename):
    g = Graph()
    p = Path.joinpath(filepath, filename)
    g.load(str(p), format="ttl")
    flist = []
    for s, p, o in g:
        term = findall(r'#(\w+)', s)
        flist.append(term)
        mlist = []
        for i in flist:
            for m in i:
                mlist.append(m)
    newlist = sorted(set(mlist), key=lambda x: mlist.index(x))
    return newlist


def writeArray(inputArray, Opfilename):
    with open(Opfilename, "w+") as my_csv:
        csvWriter = csv.writer(my_csv)
        csvWriter.writerows(inputArray)
        print("file has been written to", Opfilename)


def writeCsv(inputArray, Opfilepath, name):
    p = Path.joinpath(Opfilepath, name)
    np.savetxt(str(p), inputArray, fmt='%s', delimiter=",")
    print("file has been saved in", name)


def readTextFile(filePath, name):
    p = Path.joinpath(filePath, name)
    file = open(str(p), 'r')
    outputList = file.read().split('\n')
    print("file has been read", name)
    return outputList


def writeList(inputList, outputFilename):
    with open(outputFilename, "w") as tmpvar:
        for key in inputList:
            tmpvar.write("%s\n" % key)
    print("file has been written to file: ", outputFilename)


# writing dictionary and save to text file
def writeDictionary(inputDictionary, outputFilename):
    with open(outputFilename, "w") as tmpvar:
        for key, value in inputDictionary.items():
            tmpvar.write('%s:%s\n' % (key, value))


# Reading from dictionary
def readDictionary(inputFileName):
    output_Dic = {}
    with open(inputFileName) as raw_data:
        for item in raw_data:
            if ':' in item:
                key, value = item.rstrip("\n").split(':', 1)
                output_Dic[key] = value
            else:
                pass  # deal with bad lines of text here'
        return output_Dic


def readDictionary2(inputFilename):
    data = {}
    finaldic = {}
    translation = {39: None}
    with open(inputFilename) as raw_data:
        for item in raw_data:
            if ':' in item:
                key, value = item.strip('\n').split(':', 1)
                data[key] = value.replace('"', '').replace("'", '')
            else:
                pass  # deal with bad lines of text here'
        finaldic = (str(data).translate(translation))
    return finaldic
