import os
""" ------------- Variables: ---------------- """

def variables_init(raw_csv_name = "Sumst_MatchCountttl2xml.csv", input_xml_name = "gtfs.xml",
                   input_ttl_name = "gtfs.ttl", cleaned_csv_name = "cleaned_input.csv",
                   selected_csv_name = "selected_mappings.csv", ttl_term_type_csv_name = "ttl_term_type.csv",
                   annotated_csv_name = "annotated_mappings.csv", note_file_name = 'individuals.txt',
                   raw_csv_unstructured = True, automatic_selection = True, user_specified_conversion_type=0 ):

    # * File Names
    raw_csv_name = raw_csv_name  # The raw csv file name
    input_xml_name = input_xml_name  # The input xml file name
    input_ttl_name = input_ttl_name  # The input ttl file name
    cleaned_csv_name = cleaned_csv_name  # The output file name for the cleaned csv file
    selected_csv_name = selected_csv_name  # The output file name for the selected mappings csv file
    ttl_term_type_csv_name = ttl_term_type_csv_name  # The output file name for the ttl term' type
    annotated_csv_name = annotated_csv_name  # The output file name for the annotated csv file (output of step2)
    note_file_name = note_file_name  # The output file name for note file to record the individuals

    # * Directories
    inputs_directory = os.path.join('.', '../../../input')
    outputs_directory = os.path.join('.', 'outputs')
    java_files_directory = os.path.join('.', '../../../input', 'java_classes')
    final_java_files_directory = os.path.join('.', 'outputs', 'final_java_classes')


    # * Other Variables
    raw_csv_unstructured = raw_csv_unstructured  # True if the out put of the W2V is unstructured
    automatic_selection = automatic_selection  # True if the user is willing to choose just the top scored mappings.

    # Defining the type of the conversion. 0="ttl2xml"  1="xml2ttl"
    user_specified_conversion_type = user_specified_conversion_type
    input_conversion_list = ["ttl2xml", "xml2ttl"]
    input_conversion_type = input_conversion_list[user_specified_conversion_type]

    return raw_csv_name, input_xml_name, input_ttl_name, cleaned_csv_name,selected_csv_name, ttl_term_type_csv_name, \
           annotated_csv_name, note_file_name, inputs_directory, outputs_directory, java_files_directory, \
           final_java_files_directory, raw_csv_unstructured, automatic_selection, input_conversion_type, \
           user_specified_conversion_type


# Todo: The function that should be called for the variable initialization in the beginning
# raw_csv_name, input_xml_name, input_ttl_name, cleaned_csv_name,selected_csv_name, ttl_term_type_csv_name, \
# annotated_csv_name, note_file_name, inputs_directory, outputs_directory, java_files_directory, \
# final_java_files_directory, raw_csv_unstructured, automatic_selection, input_conversion_type, \
# user_specified_conversion_type = variables_init(raw_csv_name="Sumst_MatchCountttl2xml.csv", input_xml_name="gtfs.xml",
#                    input_ttl_name="gtfs.ttl", cleaned_csv_name="cleaned_input.csv",
#                    selected_csv_name="selected_mappings.csv", ttl_term_type_csv_name="ttl_term_type.csv",
#                    annotated_csv_name="annotated_mappings.csv", note_file_name='individuals.txt',
#                    raw_csv_unstructured=True, automatic_selection=True, user_specified_conversion_type=0)
