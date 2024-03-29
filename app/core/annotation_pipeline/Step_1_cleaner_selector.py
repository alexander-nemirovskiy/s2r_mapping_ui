from .functions import *
from ...app_settings import raw_csv_unstructured
import pandas as pd

""" --------------------------- Cleaning --------------------------- """


def cleaner(inputs_directory, raw_csv_name, input_conversion_type, getXsdStatus):
    """ Function to transform the output of W2V in a standard csv format """

    # * Directories
    raw_csv_location = os.path.join(inputs_directory, raw_csv_name)

    # * Checks if the input csv is unstructured or structured
    # and transfer it into 3 lists containing, source term, mapped term and the mapping confidence score
    if raw_csv_unstructured:
        source_list, mapped_list, confidence_list = \
            unstructured_csv_merged_lists(raw_csv_location, input_conversion_type, xsdStructure=getXsdStatus)
    else:  # Future implementation if needed: implement for the structured CSV if needed
        print("Not implemented yet. Don't forget to respect the style of input_df during the implementation")

    # * Transfer the resulting lists into appropriate pandas data frame
    input_df = pd.DataFrame(list(zip(source_list, mapped_list, confidence_list)),
                            columns=['source_term', 'mapped_term', 'confidence_score'])
    return input_df


""" -------------------------- Selecting -------------------------- """


def selector(selection_criteria: bool, input_df: DataFrame, outputs_directory, selected_csv_name) -> DataFrame:
    """ The function to select individual mappings either automatically, or by the user  """
    if selection_criteria:  # selection criteria for automatic or manual process
        print("Selecting the mappings according to their scores")
        # * Getting the index of the rows with maximum confidence for each group
        idx = input_df.groupby(['source_term'])['confidence_score'].transform(max) == input_df['confidence_score']
        selected_df = input_df[idx]
        # * Attention: In case of multiple mapping for a source term with equal score as maximum,
        # all will be available in the results. Thus, we keep just one of them (the first one in the df)
        selected_df = selected_df.drop_duplicates('source_term')
        selected_df.reset_index(drop=True, inplace=True)
        selected_df.to_csv(os.path.join(outputs_directory, selected_csv_name), index=False)
    else:
        print("Selecting the mappings according to the user's choices")
        selected_df = input_df
        selected_df.reset_index(drop=True, inplace=True)
        selected_df.to_csv(os.path.join(outputs_directory, selected_csv_name), index=False)

    print("The final mappings are saved")
    return selected_df