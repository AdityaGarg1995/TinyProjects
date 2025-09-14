"""
    This program scrapes the official Azure OpenAI Model Lifecycle Page and generates a table regarding those models' information.
"""


import requests
from bs4 import BeautifulSoup

import pandas as pd
import openpyxl

from datetime import datetime, timedelta


## Helper Strings
MODEL_NAME = "Model Name"
MODEL_VERSION = "Model Version"
MODEL_LIFECYCLE_STATUS = "Model Lifecycle Status (Preview / GA)"
RECOMMENDED_REPLACEMENT_MODEL = "Recommended Replacement Model"
MODEL_RETIREMENT_DATE = "Model Retirement Date"
MODEL_RETIREMENT_DATE_90DAYS = 'Model Retiring in 90 Days?'

NO_EARLIER_THAN = "No earlier than "

## Helper Functions
def highlight_rows(df):
    # Highlight rows where MODEL_RETIREMENT_DATE_90DAYS column is True in Yellow
    models_retiring_in_90days = pd.Series(data=False, index=df.index)
    models_retiring_in_90days[MODEL_RETIREMENT_DATE_90DAYS] = df.loc[MODEL_RETIREMENT_DATE_90DAYS] == "True"
    return ['background-color: yellow' if models_retiring_in_90days.any() else '' for model in models_retiring_in_90days]


def azure_model_retirement_checker() -> pd.DataFrame:
    # URL of Official Azure OpenAI models lifecycle page
    url = "https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/model-retirements"

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
            cols = row.find_all('td')

            if len(cols) >= 5:  # Ensure there are enough columns
                model_name = cols[0].text.strip()
                model_version = cols[1].text.strip()
                lifecycle_status = cols[2].text.strip()
                retirement_date = cols[3].text.strip()
                recommended_replacement = cols[4].text.strip()


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
    azure_model_dataframe = azure_model_retirement_checker()
    azure_model_dataframe = azure_model_dataframe.style.apply(highlight_rows, axis=1)
    save_azure_model_retirement_information (azure_model_dataframe, "azure_openai_models_lifecycle.xlsx")