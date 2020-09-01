# Todo: To be updated
# Word2Vec to Java Annotation Pipeline
This repository contains the code for automating the procedure of annotating the java classes files.
The code has been implemented as part of SPRINT project: https://projects.shift2rail.org/s2r_ip4_n.aspx?p=s2r_SPRINT


# Repository Structure:
The repository is organized in the following folders and files:

- Folders:
  - inputs: The directory for the ttl, xml and the output of w2c files.
    - It contains examples of gtfs.ttl, gtfs.xml and Sumst_MatchCountttl2xml.csv which is the output of w2v
  - inputs\java_classes: The directory of java classes to be annotated.
    - It contains examples of the java classes before the annotations.
  - outputs: The directory to keep the intermediate results of Steps 1, 2, and 3.
    - It contains examples of intermediate results.
  - outputs\final_java_classes: The directory to save the final results of annotated java classes.
    - It contains examples of the final annotated java classes.

- Files:
  - variables.py: The user-defined variables.
  - functions.py: The implemented functions for all the steps. 
  - 1_cleaner_selector.py: File containing Step 1 of the pipeline.
  - 2_ttl_term_type_identification.py: File containing Step 2 of the pipeline.
  - 3_mappings_annotations_identification.py: File containing Step 3 of the pipeline.
  - 4_java_files_annotating.py: File containing Step 5 of the pipeline.
  - pipeline_execution.py: The file to execute all the four steps of the pipeline.


# Requirements:
- Python 3
- numpy
- pandas
- csv
- xlrd
- rdflib

# How to run:
- 1- Install the requirements.
- 2- Specify the variables in the "variables.py" or simply put the input files in the "inputs".
- 3- Run "pipeline_execution.py"


# Description of the Steps:
- Step 1: "" Cleaning and Selecting ""
  - 1- Read the unstructured CSV file (The file, which is the output of W2V).
  - 2- Apply the following transformations:
    - Respecting the ttl and xml case style (The code handles both transformations).
    - Organizing into a standard data frame with three columns and save it as CSV ("input.csv").
  - 3- Selecting the top scores for each mapping to keep just one.
    - In the case of multiple results with an equal score (all Max), the first one is selected, and the rest will be ignored.
    - It can be extended to replace this step by the Human-in-the-loop approach.
    - The result is saved as ("selected.csv").

- Step 2: "" ttl terms type identification ""
  - 1- Read the input ttl file.
  - 2- Loading the the ontology file (in any format) into a graph.
  - 3- Extracting all subjects with a Class or Property object and concatenating gtfs: chars to them.
  - 4- Saving the the extracted rdf objects into csv file.

- Step 3: "" Finding the annotations ""
  - 1- Read the CSV file, which contains the selected mappings.
  - 2- Adjust the input CSV by changing the cols names and adding new col for RDF values.
  - 3- Read the CSV file, which contains the ttl terms and their corresponding types.
  - 4- Find and generate the Final annotations to be used for the java objects.

- Step 4: "" Java Files Annotating ""
  - 1- Read the CSV file, which contains the selected mappings and their corresponding mappings.
  - 2- Getting all the java files names in input the java files directory.
  - 3- For each file, there will be a list in which each of its elements is a line of the java file.
  - 4- Final annotated java lists.
  - 5- Writing the final annotated java lists into java files.

 
