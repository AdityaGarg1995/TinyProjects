"""
Creates reports from Titanic Dataset using following python libraries:
* Streamlit : Web UI
* pandas : data processing
* matplotlib : charts / graph creation

#####
Dataset Description

Dataset source: https://github.com/datasciencedojo/datasets/blob/master/titanic.csv

Modifications to Dataset:
For ease of understanding following columns were renamed:
* Sib/sp -->> Siblings/Spouses Aboard
* Parch -->> Parents/Children Aboard
* Pclass -->> Passenger Class

This dataset analysis program is based on the code provided by Jonathon Kindred (https://substack.com/@jonathonpkindred) 
in his post: https://databytesandinsights.substack.com/p/day-50-of-50-days-of-python-building.
"""


import pandas as pd
import streamlit as st

### List of frequently used strings

#### Dataframe Column Names
AGE = "Age"
SEX = 'Sex'
EMBARKED = "Embarked"
SIBLINGS_SPOUSE_ABOARD = "Siblings/Spouses Aboard"
PARENTS_CHILDREN_ABOARD = "Parents/Children Aboard"
SURVIVED = "Survived"
PASSENGER_CLASS = "Passenger Class"

METRICS_LIST = tuple((AGE, SEX, EMBARKED, PASSENGER_CLASS))


#### Custom Columns
FAMILY_SIZE = "FamilySize"

#### Frequently used Dataframe values
MALE = "male"
FEMALE = "female"

#### Important Statistics Strings
SURVIVAL_RATE = "Survival Rate"
AVERAGE_AGE = "Average Age"
PASSENGER_CLASS_COUNTS = "Passenger Class Counts"

#### Helper Strings
FILTER_BY = "Filter By"
ALL = "All"
SELECT = "Select"



def load_titanic_data(filepath=r'TinyProjects\Data Reporters\Titanic Dataset Reports Creator\titanic.csv'):
    return pd.read_csv(filepath)


### Null filler functions
def fillna_median(dataseries: pd.Series):
    return dataseries.fillna(dataseries.median())

def fillna_mode(dataseries: pd.Series):
    return dataseries.fillna(dataseries.mode()[0])


def preprocess(df):
    df[AGE] = fillna_median(df[AGE])

    df[EMBARKED] = fillna_mode(df[EMBARKED])
    df[EMBARKED] = df[EMBARKED].map({'S': 0, 'C': 1, 'Q': 2})
    
    df[SEX] = df[SEX].map({MALE: 0, FEMALE: 1})
    
    df[FAMILY_SIZE] = df[SIBLINGS_SPOUSE_ABOARD] + df[PARENTS_CHILDREN_ABOARD] + 1
    
    return df


def generate_metrics(df):
    avg_age = df[AGE].mean()
    pclass_counts = df[PASSENGER_CLASS].value_counts()
    return {
        AVERAGE_AGE: avg_age,
        PASSENGER_CLASS_COUNTS: pclass_counts
    }


def total_survival_rate(df: pd.DataFrame) -> str:
    return f"Total {SURVIVAL_RATE} for all passengers: {df[SURVIVED].mean()*100:.2f}%"

def filtered_survival_rate(filteredDataFrame: pd.DataFrame, filter_string) -> str:
    return f"{SURVIVAL_RATE} for {filter_string}: {filteredDataFrame[SURVIVED].mean()*100:.2f}%"


def main():
    st.title("Titanic Data Dashboard")
    df = load_titanic_data(r'TinyProjects\Data Reporters\Titanic Dataset Reports Creator\titanic.csv')
    df = preprocess(df)

    st.header("Dataset Overview")
    st.write(df.head())

    totalSurvivalRate = total_survival_rate(df)

    st.header("Survival Metrics")
    metrics = generate_metrics(df)
    st.write(totalSurvivalRate)
    st.write(f"{AVERAGE_AGE}: {metrics[AVERAGE_AGE]:.2f}")


    metrics_selection = st.selectbox("Choose a metric:", METRICS_LIST)

    st.header(f"{FILTER_BY} {metrics_selection}")
    
    if (metrics_selection == SEX):
        """
        Show statistics based on Passenger Sex metric
        """
        sex_filter = st.radio(f"{SELECT} {SEX}:", (ALL, "Males", "Females"))
        if sex_filter != ALL:
            sex_val = 0 if sex_filter == "Males" else 1
            filtered_df = df[df[SEX] == sex_val]
            st.write(filtered_df)
            st.write(filtered_survival_rate(filtered_df, sex_filter))
        else:
            st.write(df)
           
    
    elif (metrics_selection == AGE):
        """
        Show statistics based on Passenger Age metric
        """
        age_filter = st.radio(f"{SELECT} {AGE}:", 
                              (ALL, "Adults (>18 years)", "Minors (<18 years)", "Infants (0-1 years)", "Toddlers (1-3 years)", "Pre-Adolescents (3-13 years)", "Adolescents (13-18 years)"))
        
        if (age_filter != ALL):
            filtered_df = pd.Series()
            if (age_filter == "Adults (>18 years)"):
                filtered_df = df[df[AGE] > 18]
                st.write(filtered_df)
                st.write(filtered_survival_rate(filtered_df, age_filter))
            elif (age_filter == "Minors (<18 years)"):
                filtered_df = df[df[AGE] < 18]
                st.write(filtered_df)
                st.write(filtered_survival_rate(filtered_df, age_filter))
            elif (age_filter == "Infants (0-1 years)"):
                filtered_df = df[df[AGE].isin([0, 1])]
                st.write(filtered_df)
                st.write(filtered_survival_rate(filtered_df, age_filter))
            elif (age_filter == "Toddlers (1-3 years)"):
                filtered_df = df[df[AGE].isin([1, 3])]
                st.write(filtered_df)
                st.write(filtered_survival_rate(filtered_df, age_filter))
            elif (age_filter == "Pre-Adolescents (3-13 years)"):
                filtered_df = df[df[AGE].isin([3, 13])]
                st.write(filtered_df)
                st.write(filtered_survival_rate(filtered_df, age_filter))
            elif (age_filter == "Adolescents (13-18 years)"):
                filtered_df = df[df[AGE].isin([13, 18])]
                st.write(filtered_df)
                st.write(filtered_survival_rate(filtered_df, age_filter))
            
        else:
            st.write(df)
        
    
    elif (metrics_selection == EMBARKED):
        """
        Show statistics based on Passenger Embaring Port metric
        """
        embarked_filter = st.radio(f"{SELECT} Embarking Port:", (ALL, "Cherbourg", "Queenstown", "Southampton"))

        if embarked_filter != ALL:
            ##df[EMBARKED] = df[EMBARKED].map({'S': 0, 'C': 1, 'Q': 2})
            embarked_port_dict = {
                "Southampton" : 0,
                "Cherbourg" : 1, 
                "Queenstown" : 2, 
            }
            filtered_df = df[df[EMBARKED] == embarked_port_dict[embarked_filter]]
            st.write(filtered_df)
            st.write(filtered_survival_rate(filtered_df, embarked_filter))      
        else:
            st.write(df)


    elif (metrics_selection == PASSENGER_CLASS):
        """
        Show statistics based on Passenger Class metric
        """
        passenger_class_filter = st.radio(f"{SELECT} {PASSENGER_CLASS}:", (ALL, "1st class", "2nd class", "3rd class"))
        
        if (passenger_class_filter != ALL):
            passenger_class_dict = {
                "1st class" : 1, 
                "2nd class" : 2, 
                "3rd class" : 3,
            }
            filtered_df = df[df[PASSENGER_CLASS] == passenger_class_dict[passenger_class_filter]]
            st.write(filtered_df)
            st.write(filtered_survival_rate(filtered_df, passenger_class_filter))
        else:
            st.write(df)

        st.bar_chart(metrics[PASSENGER_CLASS_COUNTS], x=None, y=None, 
                     x_label="Passenger Classes", y_label="Survival Count by Passenger Class", 
                     color=None, horizontal=False, stack=None, width=None, height=None, use_container_width=True)
        
        

if __name__ == "__main__":
    main()

