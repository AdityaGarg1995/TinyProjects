"""
    This program scrapes the official Azure OpenAI Model Lifecycle Page and generates a table regarding those models' information.
"""


import requests
from bs4 import BeautifulSoup

import pandas as pd

from datetime import datetime, timedelta

import logging


## Import Helper Strings and Helper Functions
from GenAI_Model_Details_Constants import (AZURE_OPENAI_MODEL_LIFECYCLE_PAGE_URL,
                                           MODEL_NAME,
                                           MODEL_LIFECYCLE_STATUS,
                                           MODEL_RETIREMENT_DATE,
                                           MODEL_VERSION,
                                           RECOMMENDED_REPLACEMENT_MODEL,
                                           MODEL_RETIREMENT_DATE_90DAYS,
                                           NO_EARLIER_THAN)

from GenAI_Model_Details_Assistant_Functions import column_text_extracter


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


## Helper Functions
def highlight_rows(df):
    # Highlight rows where MODEL_RETIREMENT_DATE_90DAYS column is True in Yellow
    models_retiring_in_90days = pd.Series(data=False, index=df.index)
    models_retiring_in_90days[MODEL_RETIREMENT_DATE_90DAYS] = df.loc[MODEL_RETIREMENT_DATE_90DAYS] == "True"
    return ['background-color: yellow' if models_retiring_in_90days.any() else '' for model in models_retiring_in_90days]


## Main function to extract and Azure OpenAI Models retirement information
def azure_model_retirement_information_extractor(url: str) -> pd.DataFrame:
    # Fetch the webpage content
    response = requests.get(url, timeout=60)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all tables on the page
    tables = soup.find_all('table')


    # List to store model data
    model_data = []

    # Iterate through each table
    for table in tables:
        rows = table.find_all('tr')
        
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all('td')

            if len(columns) >= 5:  # Ensure there are enough columns
                model_name = column_text_extracter(columns[0]) #columns[0].text.strip()
                model_version = column_text_extracter(columns[1]) #columns[1].text.strip()
                lifecycle_status = column_text_extracter(columns[2]) #columns[2].text.strip()
                retirement_date = column_text_extracter(columns[3]) #columns[3].text.strip()
                recommended_replacement = column_text_extracter(columns[4]) #columns[4].text.strip()


                # Check if the model is retiring in 90 days -->> Keep retiring_in_90_days as False by default
                ### This variable can be renamed according to desired threshold retirement date interval (here it is 90 days).
                retiring_in_90_days = False

                ## If retirement date value exists and doesn't contain the phrase "No earlier than " proceed further
                if retirement_date:
                    if (NO_EARLIER_THAN not in retirement_date):
                        try:
                            ## collapse multiple spaces to one space, then parse the date value.
                            ### "%B %d, %Y" format checks for date format of the form "Month-name Day, Year".
                            retirement_date_cleaned = " ".join(retirement_date.split())
                            retirement_date_obj = datetime.strptime(retirement_date_cleaned, "%B %d, %Y")

                            ## Check retirement date is within next 90 days. If yes, mark retiring_in_90_days as True.
                            if retirement_date_obj <= datetime.now() + timedelta(days=90):
                                retiring_in_90_days = True
                        except ValueError as e:
                            print(e)

                
                model_data.append({
                    MODEL_NAME: model_name,
                    MODEL_VERSION: model_version,
                    MODEL_LIFECYCLE_STATUS: lifecycle_status,
                    RECOMMENDED_REPLACEMENT_MODEL: recommended_replacement,
                    MODEL_RETIREMENT_DATE: retirement_date,
                    MODEL_RETIREMENT_DATE_90DAYS: str(retiring_in_90_days)
                })

    # Create a DataFrame from the model data
    return pd.DataFrame(model_data)
    

def save_azure_model_retirement_information(model_dataframe: pd.DataFrame, excel_file) -> None:
    # Save the DataFrame to an Excel file
    model_dataframe.to_excel(excel_file, index=False)

    print(f"Data has been saved to {excel_file}")



if __name__ == "__main__":
    azure_model_dataframe = azure_model_retirement_information_extractor(AZURE_OPENAI_MODEL_LIFECYCLE_PAGE_URL)
    azure_model_dataframe = azure_model_dataframe.style.apply(highlight_rows, axis=1)
    save_azure_model_retirement_information (azure_model_dataframe, "azure_openai_models_lifecycle.xlsx")