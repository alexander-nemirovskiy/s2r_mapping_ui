from pathlib import Path

import numpy as np
import csv
import xml.dom.minidom as xp
from rdflib import Graph
from re import sub, findall
import xml.etree.ElementTree as ET
from owlready2 import get_ontology, re


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


def getprefix(inputlist):
    nativedata = "xsd"
    dataprop = []
    objectprop = []
    for i in inputlist:
        prefix = re.split('[:]', i[1])[0]
        suffix = i[0]
        if prefix == nativedata:
            dataprop.append(suffix)
        else:
            objectprop.append(suffix)
    return dataprop, objectprop


def getElementandAttribute(doc, attr):
    readElement = doc.getElementsByTagName(attr)
    listElement = []
    for m in readElement:
        f = m.getAttribute('name')
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


def readXsdFile(filepath, filename):
    p = Path.cwd().joinpath(filepath, filename)
    docread = xp.parse(str(p))
    getElement = getElementandAttributeNameType(docread, 'xsd:element')
    getAttribute = getElementandAttributeNameType(docread, 'xsd:attribute')
    getComplex = getElementandAttribute(docread, 'xsd:complexType')
    getElement.extend(getAttribute)
    listofElementsAttributes = list(filter(lambda x: x != '', getElement))
    listofComplexTypes = list(filter(lambda x: x != '', getComplex))
    dataproperties, objectproperties = getprefix(listofElementsAttributes)
    finalClassList = list(dict.fromkeys(listofComplexTypes))
    finaldataproperties = list(dict.fromkeys(dataproperties))
    finalobjectproperties = list(dict.fromkeys(objectproperties))
    return sorted(finalClassList), sorted(finaldataproperties), sorted(finalobjectproperties)


def readOntology(filepath, filename):
    p = Path.cwd().joinpath(filepath, filename)
    onto = get_ontology(str(p)).load()
    clist = list(onto.classes())
    dataplist = list(onto.data_properties())
    objectplist = list(onto.object_properties())
    classlist = [str(i) for i in clist]
    datapropertylist = [str(i) for i in dataplist]
    objectpropertylist = [str(i) for i in objectplist]
    classlistprc = [re.split('[.]', w)[-1] for w in classlist]
    datapropertylistprc = [re.split('[.]', w)[-1] for w in datapropertylist]
    objectpropertylistprc = [re.split('[.]', w)[-1] for w in objectpropertylist]
    finalclasslist = list(dict.fromkeys(classlistprc))
    finaldatapropertylist = list(dict.fromkeys(datapropertylistprc))
    finalobjectpropertylist = list(dict.fromkeys(objectpropertylistprc))
    return sorted(finalclasslist), sorted(finaldatapropertylist), sorted(finalobjectpropertylist)


def readTurtle(filepath, filename):
    g = Graph()
    p = Path.cwd().joinpath(filepath, filename)
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


def checkUnderscore(i):
    CamelCase = "CamelCase"
    Space = "Space"
    Underscore = "Underscore"
    flagu = bool(re.search(r'[_]', i))
    flags = bool(re.search(r'[\s]', i))
    if flagu:
        status = Underscore
    elif flags:
        status = Space
    else:
        status = CamelCase
    return status


def getStatus(folder, filename) -> str:
    p = Path.cwd().joinpath(folder, filename)
    docread = xp.parse(str(p))
    getElement = docread.getElementsByTagName('xsd:complexType')
    name = [f.getAttribute('name') for f in getElement]
    status = checkUnderscore(name[0])
    return status
