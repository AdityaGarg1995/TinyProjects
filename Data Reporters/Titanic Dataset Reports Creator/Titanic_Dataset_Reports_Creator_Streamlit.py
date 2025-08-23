"""
Creates reports from Titanic Dataset using following python libraries:
* Streamlit : Web UI
* pandas : data processing
* altair : charts / graph creation

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
import altair as alt

## List of frequently used strings

### Dataframe Column Names
AGE = "Age"
SEX = 'Sex'
EMBARKED = "Embarked"
SIBLINGS_SPOUSE_ABOARD = "Siblings/Spouses Aboard"
PARENTS_CHILDREN_ABOARD = "Parents/Children Aboard"
SURVIVED = "Survived"
PASSENGER_CLASS = "Passenger Class"

### Custom Columns
FAMILY_SIZE = "FamilySize"


### Important Statistics Strings
SURVIVAL_RATE = "Survival Rate"
AVERAGE_AGE = "Average Age"
PASSENGER_CLASS_COUNTS = "Passenger Class Counts"
EMBARKING_PORT_COUNTS = "Embarking Port Counts"
SEX_COUNTS = "Sex Counts"


### DataFrame Categorical Value Strings
#### Port Names
CHERBOURG = "Cherbourg"
QUEENSTOWN = "Queenstown"
SOUTHAMPTON = "Southampton"
EMBARKING_PORT = "Embarking Port"

#### Passenger Classes
FIRST_CLASS = "1st Class"
SECOND_CLASS = "2nd Class"
THIRD_CLASS = "3rd Class"


#### Sexes
MALE = "male"
FEMALE = "female"


### Helper Strings
FILTER_BY = "Filter By"
ALL = "All"
SELECT = "Select"

MALES = "Males"
FEMALES = "Females"

SEXES = "Sexes"
SEX_SELECTION = "Sex (Male/Female)"

SURVIVOR_COUNT_BY = "Survivor Count by"

## DataFrame Metrics and Values Lists

### DataFrame Metrics List
METRICS_LIST = tuple((AGE, SEX, EMBARKED, PASSENGER_CLASS))

### DataFrame Categorical Values Lists
PORT_NAMES_LIST =  tuple((ALL, CHERBOURG, QUEENSTOWN, SOUTHAMPTON))
PASSENGER_CLASSES_LIST =  tuple((ALL, FIRST_CLASS, SECOND_CLASS, THIRD_CLASS))
SEXES_LIST =  tuple((ALL, MALES, FEMALES))



## Data Operations Functions
### DataSet loading function
def load_titanic_data(filepath=r'TinyProjects\Data Reporters\Titanic Dataset Reports Creator\titanic.csv'):
    return pd.read_csv(filepath)



### Preprocessing Functions

#### Null filler functions
def fillna_median(dataseries: pd.Series):
    return dataseries.fillna(dataseries.median())

def fillna_mode(dataseries: pd.Series):
    return dataseries.fillna(dataseries.mode()[0])


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df[AGE] = fillna_median(df[AGE])

    df[EMBARKED] = fillna_mode(df[EMBARKED])
    df[EMBARKED] = df[EMBARKED].map({'S': SOUTHAMPTON, 'C': CHERBOURG, 'Q': QUEENSTOWN})
    
    # df[SEX] = df[SEX].map({MALE: 0, FEMALE: 1})
    
    df[PASSENGER_CLASS] = df[PASSENGER_CLASS].map({1: FIRST_CLASS, 2: SECOND_CLASS, 3: THIRD_CLASS})

    df[FAMILY_SIZE] = df[SIBLINGS_SPOUSE_ABOARD] + df[PARENTS_CHILDREN_ABOARD] + 1
    
    return df


### Metrics Generation Functions
def generate_metrics(df:pd.DataFrame) -> dict:
    avg_age = df[AGE].mean()
    pclass_counts = df[PASSENGER_CLASS].value_counts()
    embarking_port_counts = df[EMBARKED].value_counts()
    sex_counts = df[SEX].value_counts()

    return {
        AVERAGE_AGE : avg_age,
        PASSENGER_CLASS_COUNTS : pclass_counts,
        EMBARKING_PORT_COUNTS : embarking_port_counts,
        SEX_COUNTS : sex_counts
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

    st.html(f"<h2>{FILTER_BY} {metrics_selection}</h2>")
    
    if (metrics_selection == SEX):
        """
        Show statistics based on Passenger Sex metric
        """
        sex_filter = st.radio(f"{SELECT} {SEX}:", SEXES_LIST)
        if sex_filter != ALL:
            sex_val = MALE if sex_filter == MALES else FEMALE
            filtered_df = df[df[SEX] == sex_val]
            st.write(filtered_df)
            st.write(filtered_survival_rate(filtered_df, sex_filter))
        else:
            st.write(df)
           
        source = pd.DataFrame({
                SEXES : metrics[SEX_COUNTS].index,
                f"{SURVIVOR_COUNT_BY} {SEX_SELECTION}" : metrics[SEX_COUNTS]
            }
        )
        altair_chart = alt.Chart(source).mark_bar().encode(
            x = alt.X(SEXES, axis=alt.Axis(labelAngle=0)),
            y = f"{SURVIVOR_COUNT_BY} {SEX_SELECTION}"

        )
        st.altair_chart(altair_chart)
    

    elif (metrics_selection == EMBARKED):
        """
        Show statistics based on Passenger Embarking Port metric
        """

        embarked_filter = st.radio(f"{SELECT} {EMBARKING_PORT}:", PORT_NAMES_LIST)

        if embarked_filter != ALL:
            filtered_df = df[df[EMBARKED] == embarked_filter]
            st.write(filtered_df)
            st.write(filtered_survival_rate(filtered_df, f"Passengers Embarking at {embarked_filter}"))

        else:
            st.write(df)

        source = pd.DataFrame({
                f"{EMBARKING_PORT}" : metrics[EMBARKING_PORT_COUNTS].index,
                f"{SURVIVOR_COUNT_BY} {EMBARKING_PORT}" : metrics[EMBARKING_PORT_COUNTS]
            }
        )
        altair_chart = alt.Chart(source).mark_bar().encode(
            x = alt.X(f"{EMBARKING_PORT}", axis=alt.Axis(labelAngle=0)),
            y = f"{SURVIVOR_COUNT_BY} {EMBARKING_PORT}"
        )
        st.altair_chart(altair_chart)
        

    elif (metrics_selection == PASSENGER_CLASS):
        """
        Show statistics based on Passenger Class metric
        """
        passenger_class_filter = st.radio(f"{SELECT} {PASSENGER_CLASS}:", PASSENGER_CLASSES_LIST)
        
        if (passenger_class_filter != ALL):
            filtered_df = df[df[PASSENGER_CLASS] == passenger_class_filter]
            st.write(filtered_df)
            st.write(filtered_survival_rate(filtered_df, passenger_class_filter))
        else:
            st.write(df)

        # st.bar_chart(metrics[PASSENGER_CLASS_COUNTS], x=None, y=None, 
        #              x_label="Passenger Classes", y_label="Survival Count by Passenger Class", 
        #              color=None, horizontal=False, stack=None, width=None, height=None, use_container_width=True)
        source = pd.DataFrame({
                PASSENGER_CLASS : metrics[PASSENGER_CLASS_COUNTS].index,
                f"{SURVIVOR_COUNT_BY} {PASSENGER_CLASS}" : metrics[PASSENGER_CLASS_COUNTS]
            }
        )
        altair_chart = alt.Chart(source).mark_bar().encode(
            x = alt.X(PASSENGER_CLASS, axis=alt.Axis(labelAngle=0)),
            y = f"{SURVIVOR_COUNT_BY} {PASSENGER_CLASS}"
        )
        st.altair_chart(altair_chart)
    
    
    elif (metrics_selection == AGE):
        """
        Show statistics based on Passenger Age metric
        """

        ages_list = tuple((ALL, "Adults (>18 years)", "Minors (<18 years)", "Infants (0-1 years)", "Toddlers (1-3 years)", "Pre-Adolescents (3-13 years)", "Adolescents (13-18 years)"))

        age_filter = st.radio(f"{SELECT} {AGE}:", ages_list)
        
        if (age_filter != ALL):
            filtered_df = pd.Series()
            if (age_filter == ages_list[1]):
                filtered_df = df[df[AGE] > 18]
                st.write(filtered_df)
                st.write(filtered_survival_rate(filtered_df, age_filter))
            elif (age_filter == ages_list[2]):
                filtered_df = df[df[AGE] < 18]
                st.write(filtered_df)
                st.write(filtered_survival_rate(filtered_df, age_filter))
            elif (age_filter == ages_list[3]):
                filtered_df = df[df[AGE].isin([0, 1])]
                st.write(filtered_df)
                st.write(filtered_survival_rate(filtered_df, age_filter))
            elif (age_filter == ages_list[4]):
                filtered_df = df[df[AGE].isin([1, 3])]
                st.write(filtered_df)
                st.write(filtered_survival_rate(filtered_df, age_filter))
            elif (age_filter == ages_list[5]):
                filtered_df = df[df[AGE].isin([3, 13])]
                st.write(filtered_df)
                st.write(filtered_survival_rate(filtered_df, age_filter))
            elif (age_filter == ages_list[6]):
                filtered_df = df[df[AGE].isin([13, 18])]
                st.write(filtered_df)
                st.write(filtered_survival_rate(filtered_df, age_filter))
            
        else:
            st.write(df)
        
    
    


if __name__ == "__main__":
    main()
    # df = load_titanic_data(filepath=r'TinyProjects\Data Reporters\Titanic Dataset Reports Creator\titanic.csv')
    # df = preprocess(df)
    # metrics = generate_metrics(df)
    # print(metrics)