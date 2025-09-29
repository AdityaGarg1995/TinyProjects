import requests
from bs4 import BeautifulSoup

import pandas as pd

import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


## Helper Strings
MODEL_NAME = "Model Name"
MODEL_VERSION = "Model Version"
MODEL_PROVIDER_NAME = "Model Provider Name"
MODEL_LIFECYCLE_STATUS = "Model Lifecycle Status (Preview / GA)"
RECOMMENDED_REPLACEMENT_MODEL = "Recommended Replacement Model"
MODEL_RETIREMENT_DATE = "Model Retirement Date"
MODEL_RETIREMENT_DATE_90DAYS = 'Model Retiring in 90 Days?'

NO_SOONER_THAT = "No sooner that "

import GenAI_Model_Details_Constants
import GenAI_Model_Details_Assistant_Functions

from GenAI_Model_Details_Assistant_Functions import column_text_extracter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


## AWS model specific functions
def get_aws_active_models(soup: BeautifulSoup):
    ## Table ID: w471aac15c34c11c11
    return soup.find_all(id = 'w471aac15c34c11c11')

def get_aws_legacy_models(soup: BeautifulSoup):
    ## Table ID: w471aac15c34c13c11
    return soup.find_all(id = 'w471aac15c34c13c11')


def get_aws_active_models_data(aws_active_models_table) -> pd.DataFrame:
    """
    Active Models Table Columns
        <th>Provider</th> --> 0
        <th>Model name</th> --> 1
        <th>Model ID</th> --> 2
        <th>Regions supported</th>
        <th>Launch date</th>
        <th>Tentative EOL</th> --> 5
        <th>Input modalities</th>
        <th>Output modalities</th>
    """

    """ 
    AWS Bedrock active models have only tentative EOL. Hence, checks for whether a retires in next 90 days are invalid.
    """


    model_data = []

    ## Helper Strings
    TENTATIVE_MODEL_RETIREMENT_DATE = f"Tentative {MODEL_RETIREMENT_DATE}"

    for table in aws_active_models_table:
        rows = table.find_all('tr')
        # print(rows[0])
        
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all('td')

            if len(columns) >= 5:  # Ensure there are enough columns
                model_provider_name = column_text_extracter(columns[0])
                model_name = column_text_extracter(columns[1]) 
                model_version = column_text_extracter(columns[2]) 
                retirement_date = column_text_extracter(columns[5]) 
                
                model_data.append({
                    MODEL_PROVIDER_NAME : model_provider_name,
                    MODEL_NAME: model_name,
                    MODEL_VERSION: model_version,
                    TENTATIVE_MODEL_RETIREMENT_DATE: retirement_date
                })

    # Create a DataFrame from the model data
    return pd.DataFrame(model_data)


def get_aws_legacy_models_data(aws_legacy_models_table) -> pd.DataFrame:
    """
    Legacy Models Table Columns
        <th>Model version</th> --> 0
        <th>Legacy date</th>
        <th>Public extended access date</th>
        <th>EOL date</th> --> 1
        <th>Recommended model version replacement</th> --> 2
        <th>Recommended model ID</th> --> 3
    """

    model_data = []

    for table in aws_legacy_models_table:
        rows = table.find_all('tr')
        # print(rows[0])
        
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all('td')

            if len(columns) >= 5:  # Ensure there are enough columns
                model_name = column_text_extracter(columns[0])
                retirement_date = column_text_extracter(columns[1])
                recommended_replacement = f"{column_text_extracter(columns[2])} {column_text_extracter(columns[3])}"
                
                model_data.append({
                    MODEL_NAME: model_name,
                    RECOMMENDED_REPLACEMENT_MODEL: recommended_replacement,
                    MODEL_RETIREMENT_DATE: retirement_date,
                    # MODEL_RETIREMENT_DATE_90DAYS: str(retiring_in_90_days)   ## 90 day retirement logic TBC
                })

    # Create a DataFrame from the model data
    return pd.DataFrame(model_data)


def aws_model_retirement_checker():
    # Official AWS Bedrock models lifecycle page URL
    url = "https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html"

    # Fetch the webpage content
    response = requests.get(url, timeout=60)
    soup = BeautifulSoup(response.content, 'html.parser')


    aws_active_models_table = get_aws_active_models(soup)
    aws_active_models_dataframe = get_aws_active_models_data(aws_active_models_table)


    aws_legacy_models_table = get_aws_legacy_models(soup)
    aws_legacy_models_dataframe = get_aws_active_models_data(aws_legacy_models_table)

    # # Iterate through each table
    # for table in aws_active_models_table:
    #     rows = table.find_all('tr')
    #     print(rows[0])
    
    # for table in aws_legacy_models_table:
    #     rows = table.find_all('tr')
    #     print(rows[0])

    print(aws_active_models_dataframe)
    print(aws_legacy_models_dataframe)
        
    with pd.ExcelWriter('aws_bedrock_models_lifecycle.xlsx', engine='openpyxl') as writer:
        # Write each DataFrame to a different sheet
        aws_active_models_dataframe.to_excel(writer, sheet_name='Active Models Retirement Details', index=False)
        aws_legacy_models_dataframe.to_excel(writer, sheet_name='Legacy Models Retirement Details', index=False)
       
    

def save_aws_model_retirement_information(model_dataframe: pd.DataFrame, excel_file) -> None:
    # Save the DataFrame to an Excel file
    model_dataframe.to_excel(excel_file, index=False)
    print(f"Data has been saved to {excel_file}")



if __name__ == "__main__":
    # aws_model_dataframe = aws_model_retirement_checker()
    # aws_model_dataframe = aws_model_dataframe.style.apply(highlight_rows, axis=1)
    # save_aws_model_retirement_information (aws_model_dataframe, "aws_openai_models_lifecycle.xlsx")

    aws_model_retirement_checker()


   