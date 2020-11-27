from pathlib import Path
import xml.dom.minidom as xp
import re
from re import search
import xmlschema
import pandas as pd
import os


# ******************************************************* #
# ****************** YARRRML Functions ****************** #
# ******************************************************* #
def YARRRML_mapper(xsd_file_path, xsd_file_name, selector_df, conversion_type, YARRRML_output):

    """ The main function which takes as input the XSD and the selected mappings files
    and as the output generates the YARRRML decelerations """


    # ------- Extracting classes and properties from XSD --------------

    def class_property_extractor(xsd_file_path, xsd_file_name):

        """ The function that for each Class (ComplexType) term in the xsd file
        extracts their properties(Element, Attribute) """

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
            getComplex = getElementandAttribute(doc=docread, attr='xsd:complexType')
            getElement.extend(getAttribute)
            listofElementsAttributes = list(filter(lambda x: x != '', getElement))
            listofComplexTypes = list(filter(lambda x: x != '', getComplex))
            dataproperties, objectproperties = getprefix(listofElementsAttributes)
            finalClassList = list(dict.fromkeys(listofComplexTypes))
            finaldataproperties = list(dict.fromkeys(dataproperties))
            finalobjectproperties = list(dict.fromkeys(objectproperties))
            return sorted(finalClassList), sorted(finaldataproperties), sorted(finalobjectproperties)

        def getElement(inputString):
            s = str(inputString)
            match = search(r"'([^']*)", s)[0]
            outputElement = match.split(":", 1)[-1]
            # prefix = search(r"[^(]+", s)[0]
            return outputElement  # prefix

        # get Elements and their types for xsd Classes
        def getXsdElements(inputClasses, xsdSchema):
            ctype = "XsdComplexType"
            classes_list = []
            properties_list = []
            for c in inputClasses:
                classes_list.append(c)
                current_properties = []
                # extracting the elements
                for i in xsdSchema.types[c].content.iter_elements():
                    # print(i)
                    elementname = getElement(inputString=i)
                    current_properties.append(elementname)
                # extracting the attributes
                XsdAttributeGroup = list(xsdSchema.types[c].attributes)
                # combining the elements and attributes to build the list of properties for the current class
                current_properties = current_properties + XsdAttributeGroup

                properties_list.append(current_properties)
            return classes_list, properties_list

        finalClassList, finaldataproperties, finalobjectproperties = readXsdFile(filepath=xsd_file_path,
                                                                                 filename=xsd_file_name)
        input_xsd = Path.cwd().joinpath(xsd_file_path, xsd_file_name)
        schema = xmlschema.XMLSchema(str(input_xsd))
        classes_list, properties_list = getXsdElements(inputClasses=finalClassList, xsdSchema=schema)

        return classes_list, properties_list

    # ---------------- Building the YARRRML output --------------------

    def YARRRML_prefix_template_filler(prefixes_list):

        """ Function which gets the list of prefixes and
        build the YARRRML_output_list and append the required prefixes into it"""

        # List of YARRRML content to be written into a .yml file in the end of iterations
        YARRRML_output_list = []
        YARRRML_output_list.append("# Generated by SMART")
        YARRRML_output_list.append("\n")
        YARRRML_output_list.append("prefixes:")
        YARRRML_output_list.append("\n")
        for prefix in prefixes_list:
            YARRRML_output_list.append(" ")
            YARRRML_output_list.append(prefix)
            YARRRML_output_list.append("\n")

        YARRRML_output_list.append("\n")
        YARRRML_output_list.append("mappings:")
        YARRRML_output_list.append("\n")

        return YARRRML_output_list

    # ---------------------- .yml file writer --------------------------

    def YARRRML_file_writer(YARRRML_output_list, YARRRML_directory):

        """ Function to write the YARRRML list into the .yml file """

        YARRRML_output_file = os.path.join(YARRRML_directory, "mapping.yml")
        with open(YARRRML_output_file, 'w+') as temp_f:
            for final_line in YARRRML_output_list:
                # temp_f.write('%s\n' % final_line)
                temp_f.write('%s' % final_line)

    # Extracting the classes and properties from the XSD file
    classes_list, properties_list = class_property_extractor(xsd_file_path, xsd_file_name)

    # Building the selected csv file path
    # selector_csv = Path.cwd().joinpath(selector_csv_location, selector_csv_name)

    # Read csv
    # selector_df = pd.read_csv(selector_csv)

    # Determining the column of each xsd and ontology file
    if conversion_type == "xml2ttl":
        xsd_col_name = "source_term"
        ontology_col_name = "mapped_term"
    elif conversion_type == "ttl2xml":
        xsd_col_name = "mapped_term"
        ontology_col_name = "source_term"
    else:
        print("Wrong conversion type")

    # Empty list to keep the yarrrml decelerations
    YARRRML_output_list = []

    # List of prefixes to be filled manually or automatically before generating the YML file
    # todo: to be checked which prefixes are needed and how to generate them automatically if needed
    prefixes_list = ["ex: http://example.com/",
                     "It2Rail: http://www.it2rail.eu/ontology/",
                     "idlab-fn: http://example.com/idlab/function/"]

    # Building the YARRRML output list
    YARRRML_output_list = YARRRML_prefix_template_filler(prefixes_list)

    # Iterate over each class term in the classes_list
    for class_index in range(len(classes_list)):
        class_term = classes_list[class_index]
        # Iterate over each row of the df to find the current class term
        for c_row_idx in range(len(selector_df)):
            df_class_term = selector_df.loc[c_row_idx, xsd_col_name]
            if class_term == df_class_term:
                YARRRML_output_list.append(' ')
                YARRRML_output_list.append(class_term + ':')
                YARRRML_output_list.append('\n')

                YARRRML_output_list.append(' ')
                YARRRML_output_list.append(' ')
                YARRRML_output_list.append('sources:')
                YARRRML_output_list.append('\n')

                YARRRML_output_list.append(' ')
                YARRRML_output_list.append(' ')
                YARRRML_output_list.append(' ')
                class_term_xpath = "/Schema/" + class_term  # Todo: to be extended
                YARRRML_output_list.append('- [' + xsd_file_name + '~xpath, ' + class_term_xpath + ']')
                YARRRML_output_list.append('\n')

                YARRRML_output_list.append(' ')
                YARRRML_output_list.append(' ')
                YARRRML_output_list.append('s:')
                YARRRML_output_list.append('\n')

                YARRRML_output_list.append(' ')
                YARRRML_output_list.append(' ')
                YARRRML_output_list.append(' ')
                YARRRML_output_list.append('- function: idlab-fn:random')
                YARRRML_output_list.append('\n')

                # todo: to be checked if "type: iri" should be added in this way or not
                # YARRRML_output_list.append(' ')
                # YARRRML_output_list.append(' ')
                # YARRRML_output_list.append(' ')
                # YARRRML_output_list.append('type: iri')
                # YARRRML_output_list.append('\n')

                YARRRML_output_list.append(' ')
                YARRRML_output_list.append(' ')
                YARRRML_output_list.append('po:')
                YARRRML_output_list.append('\n')

                # The suggested mapping for the Class
                df_class_suggested_term = selector_df.loc[c_row_idx, ontology_col_name]
                YARRRML_output_list.append(' ')
                YARRRML_output_list.append(' ')
                YARRRML_output_list.append(' ')
                YARRRML_output_list.append('- [a, It2Rail:' + df_class_suggested_term + ']')
                YARRRML_output_list.append('\n')

                # The list of all the properties of the current class term
                class_properties_list = properties_list[class_index]
                for properties_idx in range(len(class_properties_list)):
                    property_term = class_properties_list[properties_idx]
                    # Iterate over each row of the df to find the current property term
                    for p_row_idx in range(len(selector_df)):
                        df_property_term = selector_df.loc[p_row_idx, xsd_col_name]
                        if property_term == df_property_term:
                            df_property_suggested_term = selector_df.loc[p_row_idx, ontology_col_name]
                            YARRRML_output_list.append(' ')
                            YARRRML_output_list.append(' ')
                            YARRRML_output_list.append(' ')
                            YARRRML_output_list.append(
                                '- [It2Rail:' + df_property_suggested_term + ', ' + '$(' + property_term + ')' + ']')
                            YARRRML_output_list.append('\n')
                            break
                        else:
                            continue
                break
            else:
                continue

    # Writing the YARRRML list into .yml file
    YARRRML_file_writer(YARRRML_output_list=YARRRML_output_list, YARRRML_directory=YARRRML_output)



# # --------- Directories and file names--------------
# xsd_file_path = "G:\\OneDrive - Politecnico di Milano\\DEIB\\SPRINT\\SMART_ALI\\RML_decl\\input"
# xsd_file_name = "Common.xsd"
# selector_csv_location = "G:\\OneDrive - Politecnico di Milano\\DEIB\\SPRINT\\SMART_ALI\\RML_decl\\input"
# selector_csv_name = "selector_e53a69e9.csv"
# conversion_type = "xml2ttl"
# # "ttl2xml" or "xml2ttl"
# # The path to the output of the .yml file
# YARRRML_output = "G:\\OneDrive - Politecnico di Milano\\DEIB\\SPRINT\\SMART_ALI\\RML_decl\\output\\YARRRML\\"
# # -------------------------------------------------------
#
# # Function Call
# YARRRML_mapper(xsd_file_path, xsd_file_name, selector_csv_location, selector_csv_name,
#                    conversion_type, YARRRML_output)
