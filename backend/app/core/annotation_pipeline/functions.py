# import xlrd
import csv
import pandas as pd
from pathlib import Path
import numpy as np
from pandas import DataFrame

from .variables import *
import rdflib
from rdflib import Graph, URIRef, RDFS, RDF
import re


def unstructured_csv_merged_lists(raw_csv_location, input_coversion_type, xsdStructure):
    """Fix and transform the unstructured csv input to 3 lists:
    source_list: keeps the elements which have been given to be mapped
    mapped_list: keeps the elements which are the results of mapping
    confidence_list: keeps the confidence of one2one mapping
    Attention: specify the type of mapping through second input (input_conversion_type)"""
    """ raw_csv_location: the location of the CSV file to be structured
    input_conversion_type: either ttl2xml or xml2ttl """
    source_list = []
    mapped_list = []
    confidence_list = []

    # Input
    data_file = raw_csv_location
    if input_coversion_type == "ttl2xml":
        # Loop the data lines
        with open(data_file, 'r') as temp_f:
            # Read the lines
            lines = temp_f.readlines()
        for L in range(len(lines)):
            line = lines[L]
            first_col_start = False
            first_col_end = False
            second_col_start = False
            second_col_end = False

            new_line = line[0:-1]
            temp_word_source = ""
            temp_word_mapped = ""
            temp_word_confidence = ""

            for c in range(len(new_line)):
                char = new_line[c]

                if c == 0:
                    first_col_start = True

                # Check for the confidence
                if first_col_start == False and first_col_end == True and second_col_start == False and second_col_end == True:
                    if char == "[":
                        continue
                    elif char == ",":
                        continue
                    elif char == "'":
                        continue
                    elif char == " ":
                        continue
                    elif char == "]":
                        continue
                    else:
                        temp_word_confidence = temp_word_confidence + char

                # Check for the source
                elif first_col_start and not first_col_end:
                    if char == "[":
                        continue
                    elif char == ",":
                        continue
                    elif char == "'":
                        continue
                    elif char == " ":
                        continue
                    elif char == "]":
                        first_col_start = False
                        first_col_end = True
                        second_col_start = True
                    else:
                        temp_word_source = temp_word_source+char

                # Check for the mapped
                elif second_col_start and not second_col_end:
                    if char == "[":
                        continue
                    elif char == ",":
                        continue
                    elif char == "'":
                        continue
                    elif char == " ":
                        if xsdStructure == "Underscore":
                            temp_word_mapped = temp_word_mapped + "_"
                        elif xsdStructure == "Space":
                            temp_word_mapped = temp_word_mapped + " "
                        elif xsdStructure == "CamelCase":
                            temp_word_mapped = temp_word_mapped
                    elif char == "]":
                        second_col_start = False
                        second_col_end = True
                    else:
                        temp_word_mapped = temp_word_mapped + char
                    # print("temp_word_mapped : ", temp_word_mapped)
            source_list.append(temp_word_source)
            mapped_list.append(temp_word_mapped)
            confidence_list.append(int(temp_word_confidence))

        # Close file
        temp_f.close()

        return source_list, mapped_list, confidence_list

    elif input_coversion_type == "xml2ttl":
        # Loop the data lines
        with open(data_file, 'r') as temp_f:
            # Read the lines
            lines = temp_f.readlines()
        for L in range(len(lines)):
            line = lines[L]
            first_col_start = False
            first_col_end = False
            second_col_start = False
            second_col_end = False

            new_line = line[0:-1]
            temp_word_source = ""
            temp_word_mapped = ""
            temp_word_confidence = ""

            for c in range(len(new_line)):
                char = new_line[c]

                if c == 0:
                    first_col_start = True

                # Check for the confidence
                if first_col_start == False and first_col_end == True and second_col_start == False and second_col_end == True:
                    if char == "[":
                        continue
                    elif char == ",":
                        continue
                    elif char == "'":
                        continue
                    elif char == " ":
                        continue
                    elif char == "]":
                        continue
                    else:
                        temp_word_confidence = temp_word_confidence + char

                # Check for the source
                elif first_col_start and not first_col_end:
                    if char == "[":
                        continue
                    elif char == ",":
                        continue
                    elif char == "'":
                        continue
                    elif char == " ":
                        if xsdStructure == "Underscore":
                            temp_word_mapped = temp_word_mapped + "_"
                        elif xsdStructure == "Space":
                            temp_word_mapped = temp_word_mapped + " "
                        elif xsdStructure == "CamelCase":
                            temp_word_mapped = temp_word_mapped
                    elif char == "]":
                        first_col_start = False
                        first_col_end = True
                        second_col_start = True
                    else:
                        temp_word_source = temp_word_source + char

                # Check for the mapped
                elif second_col_start and not second_col_end:
                    if char == "[":
                        continue
                    elif char == ",":
                        continue
                    elif char == "'":
                        continue
                    elif char == " ":
                        continue
                    elif char == "]":
                        second_col_start = False
                        second_col_end = True
                    else:
                        temp_word_mapped = temp_word_mapped + char
                    # print("temp_word_mapped : ", temp_word_mapped)
            source_list.append(temp_word_source)
            mapped_list.append(temp_word_mapped)
            confidence_list.append(int(temp_word_confidence))

            # Close file
        temp_f.close()

        return source_list, mapped_list, confidence_list
# -----------------------End of function--------------------------------- #


# Attention: in case of using the function fix blank rows after each row
# def csv_from_excel(outputs_directory, inputs_directory, file_name):
#     """ Convert xlsx to csv """
#
#     wb = xlrd.open_workbook(inputs_directory+file_name)
#     sh = wb.sheet_by_name('Sheet1')
#     # next two lines drop the xlsx to change it to csv and keep the original name
#     new_name = file_name[: -5:]
#     new_name = new_name + ".csv"
#     your_csv_file = open(outputs_directory+new_name, 'w', encoding='utf8')
#     wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
#
#     for rownum in range(sh.nrows):
#         wr.writerow(sh.row_values(rownum))
#
#     your_csv_file.close()
# -----------------------End of function--------------------------------- #


def unstructured_csv_fixer(csv_file):
    """Fix the unstructured csv input to structured by putting null values for the uneven columns"""

    # Input
    data_file = csv_file

    # Delimiter
    data_file_delimiter = ','

    # The max column count a line in the file could have
    largest_column_count = 0

    # Loop the data lines
    with open(data_file, 'r') as temp_f:
        # Read the lines
        lines = temp_f.readlines()

        for l in lines:
            # Count the column count for the current line
            column_count = len(l.split(data_file_delimiter)) + 1

            # Set the new most column count
            largest_column_count = column_count if largest_column_count < column_count else largest_column_count

    # Close file
    temp_f.close()

    # Generate column names (will be 0, 1, 2, ..., largest_column_count - 1)
    column_names = [i for i in range(0, largest_column_count)]

    # Read csv
    df = pd.read_csv(data_file, header=None, delimiter=data_file_delimiter, names=column_names)
    # print(df)
    return df
# -----------------------End of function--------------------------------- #


def df_col_adjuster(df: DataFrame, user_specified_conversion_type):
    """Function to replace the cols name and add extra col to be filled during Annotation identification"""
    if user_specified_conversion_type == "ttl2xml":
        new_col_names = ['ttl_term', 'xml_term', 'confidence_score']
        # print("ttl2xml")
    elif user_specified_conversion_type == "xml2ttl":
        new_col_names = ['xml_term', 'ttl_term', 'confidence_score']
        # print("xml2ttl")
    else:
        raise NotImplementedError()
    # TODO check for automatic selection: might break it
    # df.drop(df.columns[0], axis=1, inplace=True)
    df.columns = new_col_names  # Replace the col names for better readability during the process.
    df["Annotation"] = "NotFound"  # Adding extra col to be filled later
    return df
# -----------------------End of function--------------------------------- #


def ttl_parser(input_ttl_file):
    """Function which takes a ttl file as input and returns list of terms and list of corresponding annotations"""
    ttl_file = input_ttl_file  # Input

    # Lists to keep the terms and annotations
    terms_list = []
    annotations_list = []

    with open(ttl_file, 'r') as temp_f:  # Loop the data lines

        lines = temp_f.readlines()  # Read the lines

        for line_number in range(len(lines)):
            line = lines[line_number]  # Reads one line
            gtfs_finder = line[0:5]  # Pick the first 5 characters of the line
            if gtfs_finder == "gtfs:":  # Checks to see if the firs 5 chars of the current line is equal to "gtfs:"
                line_elements = line.split()
                gtfs_term = line_elements[0]  # To extract the term (left side)
                term = gtfs_term[5:]  # To drop the first 5 characters to extract just the term.
                annotation = line_elements[2]  # To extract the annotation (right side)
                terms_list.append(term)  # Add the term into the terms list
                annotations_list.append(annotation)  # Add the annotation into the annotations list

    temp_f.close()  # Close file

    return terms_list, annotations_list
# -----------------------End of function--------------------------------- #


def unwanted_elements_remover(input_list):
    """Function to loop to traverse each element in list and, remove elements which are equals to the del items"""
    item_list = input_list
    # elements to be removed to be removed
    del_item1 = 'a'
    del_item2 = ';'
    del_item3 = ','

    i=0 #loop counter
    length = len(item_list)  #list length
    while(i<length):
        if(item_list[i]==del_item1 or item_list[i]==del_item2 or item_list[i]==del_item3):
            item_list.remove(item_list[i])
            # as an element is removed
            # so decrease the length by 1
            length = length - 1
            # run loop again to check element
            # at same index, when item removed
            # next item will shift to the left
            continue
        i = i+1
    # removing the attache ; and , to the end of each element
    for ii in range(len(item_list)):
        item = item_list[ii]
        if item[-1] == ',' or item[-1] == ';':  # checking the last char to find unwanted ',' and ';'
            cleaned_item = item[0:-1]  # dropping the last char
            item_list[ii] = cleaned_item  # replacing the item with the cleaned one in the list
    return item_list
# -----------------------End of function--------------------------------- #


def ttl_terms_references_extractor(input_ttl_file):
    """ Function to extract the terms from ttl file """
    ttl_file = input_ttl_file  # Input

    # Lists to keep the terms and references
    cleaned_gtfs_lines = []

    with open(ttl_file, 'r') as temp_f:  # Loop the data lines

        lines = temp_f.readlines()  # Read the lines

        for line_number in range(len(lines)):
            line = lines[line_number]  # Reads one line
            gtfs_finder = line[0:5]  # Pick the first 5 characters of the line
            if gtfs_finder == "gtfs:":  # Checks to see if the firs 5 chars of the current line is equal to "gtfs:"
                # gtfs_lines.append(line)
                line_elements = line.split()

                cleaned_gtfs_line = unwanted_elements_remover(input_list=line_elements)
                cleaned_gtfs_lines.append(cleaned_gtfs_line)

    temp_f.close()  # Close file

    return cleaned_gtfs_lines
# -----------------------End of function--------------------------------- #


def cleaned_ttl_terms_references_csv_transformer(terms_reference):
    """ Function to find the max elements inside the lists """
    lens = []

    for i in range(len(terms_reference)):
        lens.append(len(terms_reference[i]))

    max_numb = max(lens)

    # Generating the col names
    col_names = []
    for i in range(max_numb):
        col_names.append("Ref_" + str(i))
    col_names[0] = "Term"  # Change the first col name

    df = pd.DataFrame(columns=col_names, index=range(len(terms_reference)), data='-')

    for i in range(len(terms_reference)):
        item_list = terms_reference[i]
        for ii in range(len(item_list)):
            item = item_list[ii]
            df.loc[i][ii] = item

    return df
# -----------------------End of function--------------------------------- #


def ref_type_finder(df, ref):
    """ Function to find the type of each gtfs term"""
    dataframe = df
    input_ref = ref

    search = True
    s = 0
    while search:

        term = dataframe.loc[s]['Term']
        if term == input_ref:
            term_type = dataframe.loc[s][1]
            if term_type == 'rdfs:Class':
                search = False
                return term_type
            elif term_type == 'rdf:Property':
                search = False
                return term_type
            else:
                input_ref = term_type
                s = s + 1
        else:
            s = s + 1
# -----------------------End of function--------------------------------- #


def ttl_type_extractor(input_df, save_loc):
    """ Function which extract the type of ttl term"""
    df = input_df
    location = save_loc
    ref_counter = df.shape[1] - 1  # To find the number of references. Cols-1
    for i in range(len(df)):
        row = df.loc[i]
        for ii in range(ref_counter):
            col_idx = ii + 1  # To discard the firs col which contains the Terms
            ref = row[col_idx]
            if ref == '-':
                continue
            elif ref == 'rdfs:Class':
                continue
            elif ref == 'rdf:Property':
                continue
            else:
                resulting_type = ref_type_finder(df=df, ref=ref)
                df.loc[i][col_idx] = resulting_type
    df.to_csv(location, index=False)
    return df
# -----------------------End of function--------------------------------- #


def mapping_generator(annotated_dataframe, ttl_term_type_dataframe, save_location):
    """ Function to match the annotations and generate
    the appropriate syntax for Class and Property """

    annotated_df = annotated_dataframe
    ttl_term_type_csv = ttl_term_type_dataframe
    annotated_csv_location = save_location

    for ann_row in range(len(annotated_df)):
        ttl_term = annotated_df.loc[ann_row]['ttl_term']
        for ttl_row in range(len(ttl_term_type_csv)):
            gtfs_term = ttl_term_type_csv.loc[ttl_row]['Subject']
            if 'gtfs:'+ttl_term == gtfs_term:
                ref_type = ttl_term_type_csv.loc[ttl_row]['Object']
                if 'Class' in ref_type:
                    annotaion = '@RdfsClass("'+gtfs_term+'")'
                elif 'Property' in ref_type:
                    annotaion = '@RdfProperty(propertyName = "'+gtfs_term+'")'
                annotated_df.at[ann_row, 'Annotation'] = annotaion
                break

    annotated_df.to_csv(annotated_csv_location, index=False)
    return annotated_df
# -----------------------End of function--------------------------------- #


def files_to_list(java_files_names_list, java_files_directory):
    """ Function to Iterate over all the java files reading them line by line
    and for EACH file append A list to the java_files_lists"""

    java_files_names_list = java_files_names_list
    # List which contain all the java files line by line as string.
    # For each file there will be list which each of its elements is a line of the java file
    java_files_lists = []

    for file_idx in range(len(java_files_names_list)):
        # Getting the java file name inside the java_files_lists
        source_file_name = java_files_names_list[file_idx]
        # Generating the location of the java file
        source_file_location = Path.cwd().joinpath(java_files_directory, source_file_name)
        # Reading the java file
        with open(source_file_location, 'r') as source_file:
            # Read all the lines of the java file
            source_file_lines = source_file.readlines()
            # Appending the list of lines of the java file into the java_files_list
            java_files_lists.append(source_file_lines)

    return java_files_lists
# -----------------------End of function--------------------------------- #


def class_line_checker(input_xml_term, input_line):
    """ Function to validate if the java file line starts defining a class.
    If yes, validates if the class is exactly the xml_term"""
    xml_term = input_xml_term
    line = input_line

    line_validation = False
    term_validation = False
    validation = False

    # Validate if the line is the
    # if all(x in line for x in ['public', 'class']):
    if ' class ' in line:
        line_validation = True
        line_elements = line.split()
        class_name_idex = line_elements.index('class') + 1
        # Here we find the class name which is one idx after the class element.
        # And we have to make it lower case to compare it with the xml_term which is lower as well.
        class_name = line_elements[class_name_idex].lower()
        # Droping the _ char in case if it is presented in the xml_term and lowering it (to make sure)
        xml_term = xml_term.replace('_', '').lower()

        if xml_term == class_name:
            term_validation = True
        else:
            term_validation = False
    else:
        line_validation = False

    validation = term_validation and line_validation

    return validation
# -----------------------End of function--------------------------------- #


def attribute_line_checker(input_xml_term, input_line):
    """ Function to validate if the java file line starts defining an attribute.
    If yes, validates if the attribute name is exactly the xml_term"""
    xml_term = input_xml_term
    line = input_line

    line_validation = False
    term_validation = False
    validation = False

    # Validate if the line is the
    if all(x in line for x in ['@XmlAttribute(name', '=']) or all(x in line for x in ['@XmlElement(name', '=']):
        line_validation = True

        # Splitting the line, find the last element and dropping ) and " chars which are the results of JAXB.
        # We obtain the pure attribute name from the xml file
        line_elements = line.split()
        line_last_element_cleaned = line_elements[2].replace(')', '').replace('"', '').replace(',', '')

        if xml_term == line_last_element_cleaned:
            term_validation = True
        else:
            term_validation = False
    else:
        line_validation = False

    validation = term_validation and line_validation

    return validation
# -----------------------End of function--------------------------------- #


def annotation_evaluator(input_annotation, evaluation_type):
    """ The function to evaluate if the annotation type
    which can be either Class or Property is correct or not"""
    evaluation = False
    if evaluation_type == "Class":
        if "@RdfsClass" in input_annotation:
            evaluation = True
        else:
            evaluation = False
    elif evaluation_type == "Property":
        if "@RdfProperty" in input_annotation:
            evaluation = True
        else:
            evaluation = False

    return evaluation
# -----------------------End of function--------------------------------- #


def java_lists_annotator(input_annotated_df, input_java_files_lists):
    """ Function which iterating over all the mappings that are available in
    the annotated_df and add them to the java files in the form of lists
    to be used for final annotated files"""
    annotated_df = input_annotated_df
    java_files_lists = input_java_files_lists

    # Iterating over all the mappings which are available in the annotated_df
    for df_row in range(len(annotated_df)):
        # Getting the xml term of the row
        xml_term = annotated_df.loc[df_row]['xml_term']
        # Getting the annotation of the row
        annotation = annotated_df.loc[df_row]['Annotation']
        # Iterating over all the java files lists
        for java_list_idx in range(len(java_files_lists)):
            java_list = java_files_lists[java_list_idx]
            for line_idx in range(len(java_list)):
                line = java_list[line_idx]
                if class_line_checker(input_xml_term=xml_term, input_line=line):
                    # Evaluate the correctness of the Class annotation
                    if annotation_evaluator(input_annotation=annotation, evaluation_type="Class"):
                        # Insert the annotation as a new line
                        annotation_line = annotation + "\n"
                        java_list.insert(line_idx, annotation_line)
                        # Updating the java_files_lists with the new version of java_list
                        java_files_lists[java_list_idx] = java_list
                    else:
                        # Insert the commented annotation as a new line
                        annotation_line = "//"+annotation + "\n"
                        java_list.insert(line_idx, annotation_line)
                        # Updating the java_files_lists with the new version of java_list
                        java_files_lists[java_list_idx] = java_list
                    break
                elif attribute_line_checker(input_xml_term=xml_term, input_line=line):
                    # Evaluate the correctness of the Property annotation
                    if annotation_evaluator(input_annotation=annotation, evaluation_type="Property"):
                        # Insert the annotation as a new line
                        annotation_line = '\t' + annotation + "\n"
                        java_list.insert(line_idx, annotation_line)
                        # Updating the java_files_lists with the new version of java_list
                        java_files_lists[java_list_idx] = java_list
                    else:
                        # Insert the commented annotation as a new line
                        annotation_line = '\t' + "//" + annotation + "\n"
                        java_list.insert(line_idx, annotation_line)
                        # Updating the java_files_lists with the new version of java_list
                        java_files_lists[java_list_idx] = java_list
                    break
                else:
                    continue

    return java_files_lists
# -----------------------End of function--------------------------------- #


def annotated_java_files_writer(input_annotated_java_files_lists, input_java_files_names_list, input_final_java_files_directory):
    """ Function to write the final annotated java lists into java files """
    annotated_java_files_lists = input_annotated_java_files_lists
    java_files_names_list = input_java_files_names_list
    final_java_files_directory = input_final_java_files_directory

    for file_list_idx in range(len(annotated_java_files_lists)):

        final_java_file_name = java_files_names_list[file_list_idx]
        # final_java_file = final_java_files_directory + final_java_file_name
        final_java_file = os.path.join(final_java_files_directory, final_java_file_name)

        final_java_lines_list = annotated_java_files_lists[file_list_idx]
        with open(final_java_file, 'w+') as temp_f:
            for final_line in final_java_lines_list:
                # temp_f.write('%s\n' % final_line)
                temp_f.write('%s' % final_line)
# -----------------------End of function--------------------------------- #


# ----------------------------RDF-Related functions--------------------------------- #

def ontology_graph_loader(rdf_file_location):
    """ The function to Check file type and load the ontology into graph """

    f = rdflib.util.guess_format(rdf_file_location)  # Identifying the format of the input file
    g = Graph()  # Initializing the rdf graph
    g.parse(rdf_file_location, format=f)  # parsing the rdf file according to the identified format as f

    return g
# -----------------------End of function--------------------------------- #


def rdf_object_extractor(graph):
    """ The function to extract all subjects with a Class or Property object.
    Input: The ontology Graph.
    Output: Lists of subject with class and property objects """

    g = graph

    obj_class_list = []  # List containing the subjects which their object is a rdfs:Class
    obj_property_list = []  # List containing the subjects which their object is a rdf:Property

    for s, p, o in g:
        """ Iterating over all the triples to find 
        subjects with Class or Property as their object """

        if o == RDFS.Class:  # Check if the object of the current subject is a Class
            # print(s)
            class_temp = re.findall(r'#(\w+)', s)[0]
            class_temp = 'gtfs:' + class_temp  # Adding gtfs: characters
            obj_class_list.append(class_temp)  # Appending the object into the obj_class_list

        if o == RDF.Property:  # Check if the object of the current subject is a Property
            # print(s)
            property_temp = re.findall(r'#(\w+)', s)[0]
            property_temp = 'gtfs:' + property_temp  # Adding gtfs: characters
            obj_property_list.append(property_temp)  # Appending the object into the obj_property_list

    return obj_class_list, obj_property_list
# -----------------------End of function--------------------------------- #


def rdf_object_extractor_v2(graph):
    """ The function to extract all subjects with a Class or Property object.
    Input: The ontology Graph.
    Output: Lists of subject with class and property objects """

    g = graph

    obj_class_list = []  # List containing the subjects which their object is a rdfs:Class
    obj_property_list = []  # List containing the subjects which their object is a rdf:Property
    notes_list = []  # List containing the notes to be written in text file

    for s, p, o in g:
        """ Iterating over all the triples to find 
        subjects with Class or Property as their object. 
        The difference with the other version:
        Different approach to capture subClass and subProperties.
        """
        subject = re.findall(r'#(\w+)', s)
        predicate = re.findall(r'#(\w+)', p)
        object = re.findall(r'#(\w+)', o)

        if len(predicate) > 0:
            predicate_str = predicate[0]

            if predicate_str == 'type':

                if len(subject) > 0 and len(object) > 0:
                    subject_str = subject[0]
                    object_str = object[0]
                    # print("Subject: ", subject_str, " Predicate: ", predicate_str, " Object: ", object_str)
                    # counter += 1

                    if object_str == 'Class':
                        class_temp = 'gtfs:' + subject_str  # Adding gtfs: characters
                        obj_class_list.append(class_temp)  # Appending the object into the obj_class_list
                    elif object_str == 'Property':
                        property_temp = 'gtfs:' + subject_str  # Adding gtfs: characters
                        obj_property_list.append(property_temp)  # Appending the object into the obj_property_list
                    else:
                        objects_graph = graph.objects(subject=o, predicate=p)  # The object(s) graph of the given subject and predicate. Please pay attention, since we are looking for the objects(Class or Property) of the current object which refers to a gtfs term, we need to pass the current object (o) as the subject which we need to find its object(s) when the predicate = 'type'
                        note = None  # note to keep the chain of connections
                        for obj_obj in objects_graph:
                            actual_object = re.findall(r'#(\w+)', obj_obj)[0]

                            # Note: here we are writing the old subject (subject_str) into the corresponding list
                            if actual_object == 'Class':
                                # class_temp = 'gtfs:' + subject_str  # Adding gtfs: characters
                                # obj_class_list.append(class_temp)  # Appending the object into the obj_class_list
                                note = subject_str + ' | individual | ' + object_str  # Creating the note to be written separately
                            elif actual_object == 'Property':
                                # property_temp = 'gtfs:' + subject_str  # Adding gtfs: characters
                                # obj_property_list.append(property_temp)  # Appending the object into the obj_property_list
                                note = subject_str + ' | individual | ' + object_str  # Creating the note to be written separately
                            else:
                                print("Not implemented for more level of connections")

                            notes_list.append(note)

    return obj_class_list, obj_property_list, notes_list
# -----------------------End of function--------------------------------- #


def notes_generator(notes_location, notes_list):
    """ Function to write the notes into a txt file """
    with open(notes_location, 'w+') as file:
        for note in notes_list:
            file.writelines(note + '\n')
# -----------------------End of function--------------------------------- #


def target_subjects_to_csv(save_loc, obj_class_list, obj_property_list):
    """ Function to save the the extracted rdf objects into csv file """

    terms_count = len(obj_class_list) + len(obj_property_list)  # Finding the total number of terms
    col_names = ['Subject', 'Object']
    df = pd.DataFrame(columns=col_names, index=range(terms_count), data='-')  # Empty dataframe to be filled

    df_counter = 0
    for c in range(len(obj_class_list)):
        df.loc[df_counter]['Subject'] = obj_class_list[c]
        df.loc[df_counter]['Object'] = 'rdfs:Class'
        df_counter += 1

    for p in range(len(obj_property_list)):
        df.loc[df_counter]['Subject'] = obj_property_list[p]
        df.loc[df_counter]['Object'] = 'rdf:Property'
        df_counter += 1

    df.to_csv(save_loc, index=False)
    return df
# -----------------------End of function--------------------------------- #

