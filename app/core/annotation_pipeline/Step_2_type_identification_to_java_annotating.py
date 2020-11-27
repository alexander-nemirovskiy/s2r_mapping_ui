from .functions import *
from .variables import *
from os import listdir
from os.path import isfile, join

from .functions import ontology_graph_loader

""" --------------------------- ttl terms type identification --------------------------- """


def term_type_identifier(inputs_directory, input_ttl_name,
                         outputs_directory, ttl_term_type_csv_path,
                         note_file_path):
    """ Function to identify the type of the terms """

    # * Directories
    input_ttl_location = os.path.join(inputs_directory, input_ttl_name)
    # ttl_term_type_csv_location = os.path.join(outputs_directory, ttl_term_type_csv_path)
    ttl_term_type_csv_location = ttl_term_type_csv_path
    notes_location = note_file_path

    # Step1:
    # Loading the ontology file (in any format) into a graph
    graph = ontology_graph_loader(rdf_file_location=input_ttl_location)

    # Step2:
    # extract all subjects with a Class or Property object and concatenating gtfs: chars to them

    # obj_class_list, obj_property_list = rdf_object_extractor(graph=graph)
    obj_class_list, obj_property_list, notes_list = rdf_object_extractor_v2(graph=graph)
    # saving the notes into txt file to keep track of the individuals
    notes_generator(notes_location=notes_location, notes_list=notes_list)

    # Step3:
    # Saving the the extracted rdf objects into csv file
    ttl_term_type_csv: DataFrame = target_subjects_to_csv(save_loc=ttl_term_type_csv_location,
                                                          obj_class_list=obj_class_list,
                                                          obj_property_list=obj_property_list)


""" --------------------------- Finding the annotations --------------------------- """


def annotation_finder(outputs_directory, selected_csv_name,
                      inputs_directory, input_xml_name,
                      input_ttl_name, annotated_csv_name,
                      ttl_term_type_csv_path, user_specified_conversion_type):
    """ Function to find the annotations"""

    # * Directories
    selected_csv_location = os.path.join(outputs_directory, selected_csv_name)
    input_xml_location = os.path.join(inputs_directory, input_xml_name)
    input_ttl_location = os.path.join(inputs_directory, input_ttl_name)
    annotated_csv_location = os.path.join(outputs_directory, annotated_csv_name)
    ttl_term_type_csv_location = os.path.join(outputs_directory, ttl_term_type_csv_path)

    # Read the csv file which contains the selected mappings
    input_csv_file = pd.read_csv(selected_csv_location)

    # Adjust the input csv by changing the cols names and adding new col for RDF values
    annotated_df = df_col_adjuster(user_specified_conversion_type=user_specified_conversion_type,
                                   df=input_csv_file)

    # Read the csv file which contains the ttl terms and their corresponding types
    ttl_term_type_csv = pd.read_csv(ttl_term_type_csv_location)

    # Find and generate the Final annotations to be used for the java objects
    final_annotated_df = mapping_generator(annotated_dataframe=annotated_df,
                                           ttl_term_type_dataframe=ttl_term_type_csv,
                                           save_location=annotated_csv_location)


""" --------------------------- Java Files Annotating --------------------------- """


def java_annotator(outputs_directory, annotated_csv_name,
                   java_files_directory, final_java_files_directory):
    """ The function to add the annotations to the Java files """

    # * Directories
    annotated_csv_location = os.path.join(outputs_directory, annotated_csv_name)

    # Read the csv file which contains the selected mappings and their corresponding mappings
    annotated_df = pd.read_csv(annotated_csv_location)

    # Getting all the java files names in input the java files directory.
    java_files_names_list = [f for f in listdir(java_files_directory) if isfile(join(java_files_directory, f))]

    # List which contains all the java files line by line as string.
    # For each file there will be a list which each of its elements is a line of the java file
    java_files_lists = files_to_list(java_files_names_list=java_files_names_list, java_files_directory=java_files_directory)

    # Final annotated java lists
    annotated_java_files_lists = java_lists_annotator(input_annotated_df=annotated_df,
                                                      input_java_files_lists=java_files_lists)

    # Writing the final annotated java lists into java files
    annotated_java_files_writer(input_annotated_java_files_lists=annotated_java_files_lists,
                                input_java_files_names_list=java_files_names_list,
                                input_final_java_files_directory=final_java_files_directory)


""" --------------------------- Merged Steps --------------------------- """


def type_identifier_to_java_annotator(inputs_directory, input_ttl_name,
                                      outputs_directory, ttl_term_type_csv_path,
                                      note_file_path, selected_csv_name,
                                      input_xml_name, annotated_csv_name,
                                      java_files_directory,
                                      final_java_files_directory,
                                      user_specified_conversion_type):
    """ Function to execute the last three steps """

    """ --------------------------- ttl terms type identification --------------------------- """

    term_type_identifier(inputs_directory=inputs_directory, input_ttl_name=input_ttl_name,
                         outputs_directory=outputs_directory, ttl_term_type_csv_path=ttl_term_type_csv_path,
                         note_file_path=note_file_path)

    """ --------------------------- Finding the annotations --------------------------- """
    annotation_finder(outputs_directory=outputs_directory, selected_csv_name=selected_csv_name,
                      inputs_directory=inputs_directory, input_xml_name=input_xml_name,
                      input_ttl_name=input_ttl_name, annotated_csv_name=annotated_csv_name,
                      ttl_term_type_csv_path=ttl_term_type_csv_path,
                      user_specified_conversion_type=user_specified_conversion_type)

    """ --------------------------- Java Files Annotating --------------------------- """

    java_annotator(outputs_directory=outputs_directory, annotated_csv_name=annotated_csv_name,
                   java_files_directory=java_files_directory,
                   final_java_files_directory=final_java_files_directory)
