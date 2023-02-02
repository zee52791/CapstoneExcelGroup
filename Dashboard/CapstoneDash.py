# http://127.0.0.1:8050/

# All imports for visualizations, logins, and dashboard creation

import dash
from dash import html, dcc
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
from plotly.offline import iplot
import pandas as pd
import numpy as np
import pymssql
import pyodbc

from config import database
from config import username
from config import password
from config import server
from config import driver
from config import degrees
from config import employment
from config import household
from config import household_abbr
from config import income
from config import race
from config import employment_status

DTR_path = 'assets/DecisionTreeRegressionModel.png'
KNN_path = 'assets/KNNRegressionModel.png'
LR_path = 'assets/LinearRegressionModel.png'
RR_path = 'assets/RidgeRegressionModel.png'

#Reading Data from SQL Database using two methods

conn = pymssql.connect(server,username, password, database)
conn2 = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server +
                      ';PORT=1433;DATABASE='+database+';UID='+username+';PWD=' + password)
cursor = conn.cursor()
query = f"SELECT * FROM {degrees}"
degrees = pd.read_sql(query, conn)
query2 = f"SELECT * FROM {employment}"
employment = pd.read_sql(query2, conn)
query3 = f"SELECT * FROM {household}"
household = pd.read_sql(query3, conn)
query3 = f"SELECT * FROM {household_abbr}"
household_abbr = pd.read_sql(query3, conn)
query6 = f"SELECT * FROM {employment_status}"
employment_status = pd.read_sql(query6, conn)
query4 = f"SELECT * FROM {income}"
income = pd.read_sql(query4, conn)
query5 = """select 
  record_year, 
  mean_not_high_school_graduate, 
  mean_high_school_graduate, 
  associate_degree_mean, 
  bachelor_degree_mean, 
  advanced_degree_mean 
from 
  mean_worker_earnings 
where 
  race = 'Total' 
  and gender = 'Both Sexes'
"""
query6 = """select 
  state_name, 
  avg(mean) as "average_income" 
from 
  household_income_statistics 
group by 
  state_name
"""
query7="""select 
  state_ab, 
  avg(mean) as "average_income" 
from 
  household_income_statistics 
group by 
  state_ab
"""
query8="""select 
  year(record_date) as "record_year", 
  median_household_income 
from 
  median_household_income 
where 
  year(record_date) >= 2000
"""
query9="""with CTE as (
  select 
    year(record_date) as "record_year", 
    working_age_population 
  from 
    us_workforce_data 
  where 
    year(record_date) >= 2000
) 
select 
  record_year, 
  sum(working_age_population) as total_working_population 
from 
  CTE 
group by 
  record_year
"""
query10="""WITH cte AS (
  SELECT 
    year(record_date) as record_year, 
    median_household_income AS avg_income 
  FROM 
    median_household_income 
  WHERE 
    year(record_date) > 2014 
    and year(record_date)< 2022
) 
SELECT 
  cast(cte2.record_year as varchar) + '-' + cast(cte1.record_year as varchar) as year_delta, 
  round((
    (
      cte1.avg_income - cte2.avg_income
    ) / (cte2.avg_income * 1.0)
  ) * 100,2) AS percent_change 
FROM 
  cte cte1 
  JOIN cte cte2 ON cte1.record_year = cte2.record_year + 1
"""
query11="""with cte as (
  select 
    highest_qualification, 
    record_year, 
    all_races_total 
  from 
    education_status 
  where 
    record_year > 2014 
    and record_year < 2022
), 
agg AS (
  SELECT 
    record_year, 
    highest_qualification, 
    AVG(all_races_total) AS educated_percent 
  FROM 
    cte 
  GROUP BY 
    record_year, 
    highest_qualification
), 
final as (
  select 
    record_year, 
    max(
      case when highest_qualification = 'Completed 4 Years of College or more' then educated_percent end
    ) as college_or_more, 
    max(
      case when highest_qualification = 'Completed 4 Years of High School or more' then educated_percent end
    ) as high_school_or_more 
  from 
    agg 
  group by 
    record_year
) 
SELECT 
  cast(cte2.record_year as varchar) + '-' + cast(cte1.record_year as varchar) as year_delta, 
  round(
    (
      (
        cte1.college_or_more - cte2.college_or_more
      ) / (cte2.college_or_more * 1.0)
    ) * 100, 
    2
  ) AS college_percent, 
  round(
    (
      (
        cte1.high_school_or_more - cte2.high_school_or_more
      ) / (cte2.high_school_or_more * 1.0)
    ) * 100, 
    2
  ) AS school_percent 
FROM 
  final cte1 
  JOIN final cte2 ON cte1.record_year = cte2.record_year + 1;
"""
data1 = pd.read_sql(query5, conn2)
data2 = pd.read_sql(query6, conn2)
data3 = pd.read_sql(query7, conn2)
data4 = pd.read_sql(query8, conn2)
data5 = pd.read_sql(query9, conn2)
data6 = pd.read_sql(query10, conn2)
data7 = pd.read_sql(query11, conn2)

## Cleaning, organization, and/or creation of data/visuals

# Income data and table for sexes
degrees.columns = degrees.columns.str.strip()

degrees = degrees.drop(columns =["Total5", "Not a high school graduate8", "High school graduate11", "Some college/associate's degree14", "Bachelor's degree17", "Advanced degree20"])

degrees.drop([0], inplace= True)

degrees.rename(columns={"_c2": "Year",
                    "_c0": "Race",
                    "_c1": "Sex",
                    "Total3": "Total Mean",
                    "Total4": "Total Number with Earnings",
                    "Not a high school graduate6":"Not a High School Graduate Mean",
                    "Not a high school graduate7":"Not a High School Graduate Numbers with Earnings",
                    "High school graduate9": "High School Graduate Mean",
                    "High school graduate10": "High School Graduate Numbers with Earnings",
                    "Some college/associate's degree12": "Some College/Associate's Degree Mean",
                    "Some college/associate's degree13": "Some College/Associate's Degree Numbers with Earnings",
                    "Bachelor's degree15": "Bachelor's Degree Mean",
                    "Bachelor's degree16": "Bachelor's Degree Numbers with Earnings",
                    "Advanced degree18": "Advanced Degree Mean",
                    "Advanced degree19": "Advanced Degree Numbers with Earnings"}, inplace=True)

columns_float = ["Total Mean", "Total Number with Earnings", "Not a High School Graduate Mean", "Not a High School Graduate Numbers with Earnings", "High School Graduate Mean",
                "High School Graduate Numbers with Earnings", "Some College/Associate's Degree Mean", "Some College/Associate's Degree Numbers with Earnings",
                "Bachelor's Degree Mean", "Bachelor's Degree Numbers with Earnings", "Advanced Degree Mean", "Advanced Degree Numbers with Earnings"]

for column in columns_float:
    degrees[column]=degrees[column].astype('float')

columns_integer = ["Year"]

for column in columns_integer:
    degrees[column]=degrees[column].astype('int')

columns_object = ["Race", "Sex"]

for column in columns_object:
    degrees[column]=degrees[column].astype('object')

degrees_income = degrees[["Year", "Total Mean", "Sex", "Race", "Not a High School Graduate Mean", "High School Graduate Mean", "Some College/Associate's Degree Mean", "Bachelor's Degree Mean", "Advanced Degree Mean"]]

degrees_income = degrees_income[(degrees_income['Sex'] == 'Male')|(degrees_income['Sex'] == 'Female')]

degrees_income = degrees_income[(degrees_income['Race'] =='Total')]

# Graph

sex_fig = px.bar(degrees_income, x="Sex", y=["Not a High School Graduate Mean", "High School Graduate Mean", "Some College/Associate's Degree Mean", "Bachelor's Degree Mean", "Advanced Degree Mean"], barmode='group',
animation_frame="Year", animation_group="Sex")


sex_fig.update_layout(title="Per Capita Income Average for the Different Education Attainment Levels for Males and Females",
                xaxis_title="Identified Sex", yaxis_title="Per Capita Income Average", legend=dict(title="Education Level"), paper_bgcolor='#C3F6F7', template='ggplot2')

# Income by race

degrees_income_race = degrees[["Year", "Total Mean", "Sex", "Race", "Not a High School Graduate Mean", "High School Graduate Mean", "Some College/Associate's Degree Mean", "Bachelor's Degree Mean", "Advanced Degree Mean"]]

degrees_income_race = degrees_income_race[(degrees_income_race['Sex'] == 'Both Sexes')]

degrees_income_race = degrees_income_race[(degrees_income_race['Race'] !='Total')]

# Graph 

race_fig = px.bar(degrees_income_race, x="Race", y=["Not a High School Graduate Mean", "High School Graduate Mean", "Some College/Associate's Degree Mean", "Bachelor's Degree Mean", "Advanced Degree Mean"], barmode='group',
animation_frame="Year", animation_group="Race")

race_fig.update_layout(title="Per Capita Income for the Different Education Attainment Levels by Identified Race",
                xaxis_title="Identified Race", yaxis_title="Per Capita Income Average", legend=dict(title="Education Level"), paper_bgcolor='#C3F6F7', template='ggplot2')

# Income by year

degrees_income_year = degrees[["Year", "Total Mean", "Sex", "Race", "Not a High School Graduate Mean", "High School Graduate Mean", "Some College/Associate's Degree Mean", "Bachelor's Degree Mean", "Advanced Degree Mean"]]

degrees_income_year = degrees_income_year[(degrees_income_year['Year'] == 2019)|(degrees_income_year['Year'] == 2018)|(degrees_income_year['Year'] == 2017)|(degrees_income_year['Year'] == 2016)|
(degrees_income_year['Year'] == 2015)|(degrees_income_year['Year'] == 2014)|(degrees_income_year['Year'] == 2014)|(degrees_income_year['Year'] == 2013)|(degrees_income_year['Year'] == 2012)|
(degrees_income_year['Year'] == 2011)|(degrees_income_year['Year'] == 2010)]

degrees_income_year = degrees_income_year[(degrees_income_year['Sex'] == 'Both Sexes')]

degrees_income_year = degrees_income_year[(degrees_income_year['Race'] =='Total')]


# Employment VS Unemployment

columns_float = ["Participation rate", "Employment-population ratio", "Unemployment rate", "Employed", "Unemployed"]

for column in columns_float:
    employment_status[column]=employment_status[column].astype('float')

columns_integer = ["Year", "Civilian noninstitutional population", "Civilian labor force"]

for column in columns_integer:
    employment_status[column]=employment_status[column].astype('int')

degree_employment_status = employment_status[["Year", "Education Attainment", "Civilian noninstitutional population", "Civilian labor force", "Participation rate",
"Employed", "Employment-population ratio", "Unemployed", "Unemployment rate"]] 

degree_employment_status = degree_employment_status[(degree_employment_status["Education Attainment"] !="Some college or associate degreeTotal")]
degree_employment_status = degree_employment_status[(degree_employment_status["Education Attainment"] !="Bachelor's degree and higherTotal")]

#Graph
unemployment_fig = px.line(degree_employment_status, x="Year", y="Unemployment rate",color='Education Attainment')

unemployment_fig.update_layout(title="Comparison of Unemployment Rates for the Different Educational Attainment Levels Through the Years",
                  xaxis_title="Year", yaxis_title="Unemployment Rate", paper_bgcolor='#C3F6F7', template='ggplot2')

degree_employment_rates = employment_status[["Year", "Education Attainment", "Civilian noninstitutional population", "Civilian labor force", "Participation rate",
"Employed", "Employment-population ratio", "Unemployed", "Unemployment rate"]] 

degree_employment_rates = degree_employment_rates[(degree_employment_rates["Education Attainment"] !="Some college or associate degreeTotal")]
degree_employment_rates = degree_employment_rates[(degree_employment_rates["Education Attainment"] !="Bachelor's degree and higherTotal")]
degree_employment_rates = degree_employment_rates[(degree_employment_rates["Year"] == 2020)]

# Household and States with Abbreviations data...not to be mistaken with household

household_abbr.columns = household_abbr.columns.str.strip()

household_abbr.drop([0], inplace= True)

household_abbr.rename(columns={
                "Column1": "State",
                "Median Household Income by State: Selected years 1990 through 2019": "Median Household Income by State: 1990",
                "Median Household Income by State: Selected years 1990 through 2019_1": "Median Household Income by State: 2000",
                "Median Household Income by State: Selected years 1990 through 2019_2": "Median Household Income by State: 2005",
                "Median Household Income by State: Selected years 1990 through 2019_3": "Median Household Income by State: 2010",
                "Median Household Income by State: Selected years 1990 through 2019_4": "Median Household Income by State: 2014",
                "Median Household Income by State: Selected years 1990 through 2019_5": "Median Household Income by State: 2015",
                "Median Household Income by State: Selected years 1990 through 2019_6": "Median Household Income by State: 2016",
                "Median Household Income by State: Selected years 1990 through 2019_7": "Median Household Income by State: 2017",
                "Median Household Income by State: Selected years 1990 through 2019_8": "Median Household Income by State: 2018",
                "Median Household Income by State: Selected years 1990 through 2019_9": "Median Household Income by State: 2019",}, inplace=True)

householdabbr_columns_integer = ["Median Household Income by State: 1990", "Median Household Income by State: 2000", "Median Household Income by State: 2005", 
"Median Household Income by State: 2010","Median Household Income by State: 2014", "Median Household Income by State: 2015", 
"Median Household Income by State: 2016", "Median Household Income by State: 2017","Median Household Income by State: 2018", "Median Household Income by State: 2019",]

for column in householdabbr_columns_integer:
    household_abbr[column] = household_abbr[column].astype("int")

household_abbr["State"] = household_abbr["State"].replace(["United States", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut","Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii","Idaho", "Illinois", "Indiana", "Iowa", "Kansas", 
"Kentucky", "Louisiana","Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico","New York", "North Carolina",
"North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"], 
["US", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", 
"NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])

# household income graph

houseincome = px.bar(household_abbr, x="State", y=["Median Household Income by State: 1990", "Median Household Income by State: 2000", "Median Household Income by State: 2005", 
"Median Household Income by State: 2010","Median Household Income by State: 2014", "Median Household Income by State: 2015", 
"Median Household Income by State: 2016", "Median Household Income by State: 2017","Median Household Income by State: 2018", "Median Household Income by State: 2019"])

houseincome.update_layout(title="Average Household Income by State Compared to the United States",
                  xaxis_title="Average Household Income", yaxis_title="State", showlegend = False, template='ggplot2')

houseincome.update_layout(
    updatemenus=[
        dict(
            type="dropdown",
            buttons=list([
                dict(
                    args=[{'visible': [True, False, False, False, False, False, False, False, False, False]},
                          {'title': 'Median Household Income by State: 1990'}],
                    label="1990",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, True, False, False, False, False, False, False, False, False]},
                          {'title': 'Median Household Income by State: 2000'}],
                    label="2000",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, False, True, False, False, False, False, False, False, False]},
                          {'title': 'Median Household Income by State: 2005'}],
                    label="2005",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, False, False, True, False, False, False, False, False, False]},
                          {'title': 'Median Household Income by State: 2010'}],
                    label="2010",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, False, False, False, True, False, False, False, False, False]},
                          {'title': 'Median Household Income by State: 2014'}],
                    label="2014",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, True, False, False, False, False]},
                          {'title': 'Median Household Income by State: 2015'}],
                    label="2015",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False, True, False, False, False]},
                          {'title': 'Median Household Income by State: 2016'}],
                    label="2016",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False, False, True, False, False]},
                          {'title': 'Median Household Income by State: 2017'}],
                    label="2017",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False, False, False, True, False]},
                          {'title': 'Median Household Income by State: 2018'}],
                    label="2018",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False, False, False, False, True]},
                          {'title': 'Median Household Income by State: 2019'}],
                    label="2019",
                    method="update"
                ),
            ]),
            direction="down",
            showactive=True,
            xanchor="right",
            yanchor="top"
        ),
    ]
)

# Average income by state

state_income = household_abbr[["State", "Median Household Income by State: 1990", "Median Household Income by State: 2000", "Median Household Income by State: 2005", 
"Median Household Income by State: 2010","Median Household Income by State: 2014", "Median Household Income by State: 2015", 
"Median Household Income by State: 2016", "Median Household Income by State: 2017","Median Household Income by State: 2018", "Median Household Income by State: 2019"]] 

state_income = state_income[(state_income["State"] !="US")]

years = [1990, 2000, 2005, 2010, 2014, 2015, 2016, 2017, 2018, 2019]

# cleaning the data for household dataset
household.columns = household.columns.str.strip()
household.drop([0], inplace= True)
household.rename(columns={
    "_c0": "State", 
    "Median Household Income by State: Selected years 1990 through 20191": "Median Household Income by State: 1990",
    "Median Household Income by State: Selected years 1990 through 20192": "Median Household Income by State: 2000",
    "Median Household Income by State: Selected years 1990 through 20193": "Median Household Income by State: 2005",
    "Median Household Income by State: Selected years 1990 through 20194": "Median Household Income by State: 2010",
    "Median Household Income by State: Selected years 1990 through 20195": "Median Household Income by State: 2014",
    "Median Household Income by State: Selected years 1990 through 20196": "Median Household Income by State: 2015",
    "Median Household Income by State: Selected years 1990 through 20197": "Median Household Income by State: 2016",
    "Median Household Income by State: Selected years 1990 through 20198": "Median Household Income by State: 2017",
    "Median Household Income by State: Selected years 1990 through 20199": "Median Household Income by State: 2018",
    "Median Household Income by State: Selected years 1990 through 201910": "Median Household Income by State: 2019",
}, inplace=True)

# changing the dtypes for household dataset
household_columns_integer = ["Median Household Income by State: 1990", "Median Household Income by State: 2000", "Median Household Income by State: 2005", "Median Household Income by State: 2010",
"Median Household Income by State: 2014", "Median Household Income by State: 2015", "Median Household Income by State: 2016", "Median Household Income by State: 2017",
"Median Household Income by State: 2018", "Median Household Income by State: 2019",]
for column in household_columns_integer: 
    household[column] = household[column].astype("int")

# cleaning the data for income dataset
income.columns = income.columns.str.strip()
income.drop([0], inplace= True)
income.rename(columns={
    "_c0": "Race", 
    "_c1": "Year",
    "Number(Thousands)": "Number(Thousands)",
    "Percent Distribution3": "Total Percent Distribution",
    "Percent Distribution4": "Under $15000",
    "Percent Distribution5": "$15000 to $24999",
    "Percent Distribution6": "$25000 to $34999",
    "Percent Distribution7": "$35000 to $49999",
    "Percent Distribution8": "$50000 to $74999",
    "Percent Distribution9": "$75000 to $99999",
    "Percent Distribution10": "$100000 to $149999",
    "Percent Distribution11": "$150000 to $199999",
    "Percent Distribution12": "$200000 and over",
    "Median Income13": "Median Income Estimate",
    "Median Income14": "Median Income Margin of Error",
    "Mean Income15": "Mean Income Estimate",
    "Mean Income16": "Mean Income Margin of Error"
}, inplace=True)

# changing the dtypes for income dataset
income["Year"] = income["Year"].astype(int)

#income_year dataframe
income_year = income[["Year", "Mean Income Estimate", "Race"]]
income_year = income_year[(income_year["Year"] == 2019)|(income_year["Year"] == 2018)|(income_year["Year"] == 2017)|(income_year["Year"] == 2016)|(income_year["Year"] == 2015)]
income_year = income_year[(income_year["Race"] == "All Races")]
income_year["Mean Income Estimate"] = income_year["Mean Income Estimate"].astype(float)
income_year["Race"] = income_year["Race"].astype(str)

#income_race_2019 dataframe
income_race_2019 = income[["Race", "Year", "Mean Income Estimate", "Median Income Estimate"]]
income_race_2019 = income_race_2019[(income_race_2019['Year'] == 2019)]
income_race_2019 = income_race_2019[(income_race_2019['Race'] !='Total')]
income_race_2019["Mean Income Estimate"] = income_race_2019["Mean Income Estimate"].astype(float)
income_race_2019["Median Income Estimate"] = income_race_2019["Median Income Estimate"].astype(float)
income_race_2019["Race"] = income_race_2019["Race"].astype(str)

#income_race_2018 dataframe
income_race_2018 = income[["Race", "Year", "Mean Income Estimate", "Median Income Estimate"]]
income_race_2018 = income_race_2018[(income_race_2018['Year'] == 2018)]
income_race_2018 = income_race_2018[(income_race_2018['Race'] !='Total')]
income_race_2018["Mean Income Estimate"] = income_race_2018["Mean Income Estimate"].astype(float)
income_race_2018["Median Income Estimate"] = income_race_2018["Median Income Estimate"].astype(float)
income_race_2018["Race"] = income_race_2018["Race"].astype(str)

#income_race_2017 dataframe
income_race_2017 = income[["Race", "Year", "Mean Income Estimate", "Median Income Estimate"]]
income_race_2017 = income_race_2017[(income_race_2017['Year'] == 2017)]
income_race_2017 = income_race_2017[(income_race_2017['Race'] !='Total')]
income_race_2017["Mean Income Estimate"] = income_race_2017["Mean Income Estimate"].astype(float)
income_race_2017["Median Income Estimate"] = income_race_2017["Median Income Estimate"].astype(float)
income_race_2017["Race"] = income_race_2017["Race"].astype(str)

#income_race_2016 dataframe
income_race_2016 = income[["Race", "Year", "Mean Income Estimate", "Median Income Estimate"]]
income_race_2016 = income_race_2016[(income_race_2016['Year'] == 2016)]
income_race_2016 = income_race_2016[(income_race_2016['Race'] !='Total')]
income_race_2016["Mean Income Estimate"] = income_race_2016["Mean Income Estimate"].astype(float)
income_race_2016["Median Income Estimate"] = income_race_2016["Median Income Estimate"].astype(float)
income_race_2016["Race"] = income_race_2016["Race"].astype(str)


#income_race_2015 dataframe
income_race_2015 = income[["Race", "Year", "Mean Income Estimate", "Median Income Estimate"]]
income_race_2015 = income_race_2015[(income_race_2015['Year'] == 2015)]
income_race_2015 = income_race_2015[(income_race_2015['Race'] !='Total')]
income_race_2015["Mean Income Estimate"] = income_race_2015["Mean Income Estimate"].astype(float)
income_race_2015["Median Income Estimate"] = income_race_2015["Median Income Estimate"].astype(float)
income_race_2015["Race"] = income_race_2015["Race"].astype(str)

# Dataframe for all years race income table

income_race_allyears = income[["Race", "Year", "Mean Income Estimate", "Median Income Estimate"]]
income_race_allyears = income_race_allyears[(income_race_allyears['Race'] !='Total')]
income_race_allyears["Mean Income Estimate"] = income_race_allyears["Mean Income Estimate"].astype(float)
income_race_allyears["Median Income Estimate"] = income_race_allyears["Median Income Estimate"].astype(float)
income_race_allyears["Race"] = income_race_allyears["Race"].astype(str)

# Graph

income_allyears_fig = px.bar(income_race_allyears, x="Race", y="Mean Income Estimate", barmode='group',
animation_frame="Year", animation_group="Race")

income_allyears_fig.update_layout(title="Per Capita Income for The Identified Race", xaxis_title="Identified Race", 
yaxis_title="Per Capita Income Average", paper_bgcolor='#C3F6F7', template='ggplot2')


##### household_degrees_merged and household_degrees and household_degrees2 dataframes
# fixing the indexing of the household dataset
keys = [I for I in range(0, 52)]
values = [household.iloc[i]['State'] for i in range(0, 52)]
new_index = {k:v for (k,v) in zip(keys, values)}
household.reindex(index=new_index)
household_new= household.transpose()
# renaming and resetting the index 
newcolumn = household_new.iloc[0]
household_new = household_new.iloc[1:]
household_new.rename(columns=newcolumn, inplace = True)
household_new.reset_index(inplace = True, drop = True)
# creating a new year column
household_new["Year"] = [1990, 2000, 2005, 2010, 2014, 2015, 2016, 2017, 2018, 2019]
# merging the degrees dataset with the household dataset
household_degrees_merged = degrees.merge(household_new, how = "inner", on= "Year")
# creating the household_degrees dataset and adding filters
household_degrees = household_degrees_merged[["Year", "Total Mean", "Sex", "Race", "Not a High School Graduate Mean", "High School Graduate Mean", "Some College/Associate's Degree Mean", "Bachelor's Degree Mean", "Advanced Degree Mean", "United States"]]
household_degrees = household_degrees[(household_degrees["Year"] == 2019) | (household_degrees["Year"] == 2018) | (household_degrees["Year"] == 2017) | (household_degrees["Year"] == 2016) |
(household_degrees["Year"] == 2015)]
household_degrees = household_degrees[(household_degrees["Race"] == "Total")]
household_degrees = household_degrees[(household_degrees["Sex"] == "Both Sexes")]
# changing the datatypes of household_degrees dataset
household_degrees.dtypes
household_degrees["Year"] = household_degrees["Year"].astype(int)
household_degrees["Not a High School Graduate Mean"] = household_degrees["Not a High School Graduate Mean"].astype(float)
household_degrees["High School Graduate Mean"] = household_degrees["High School Graduate Mean"].astype(float)
household_degrees["Some College/Associate's Degree Mean"]= household_degrees["Some College/Associate's Degree Mean"].astype(float)
household_degrees["Bachelor's Degree Mean"] = household_degrees["Bachelor's Degree Mean"].astype(float)
household_degrees["Advanced Degree Mean"] = household_degrees["Advanced Degree Mean"].astype(float)
# creating the household_degrees2 dataset and adding filters 
household_degrees2 = household_degrees_merged[["Year", "Total Mean", "Sex", "Race", "Not a High School Graduate Mean", "High School Graduate Mean", "Some College/Associate's Degree Mean", "Bachelor's Degree Mean", "Advanced Degree Mean", "United States"]]
household_degrees2 = household_degrees2[(household_degrees2["Year"] == 2019) | (household_degrees2["Year"] == 2018) | (household_degrees2["Year"] == 2017) | (household_degrees2["Year"] == 2016) |
(household_degrees2["Year"] == 2015)]
household_degrees2 = household_degrees2[(household_degrees2["Race"] != "Total")]
household_degrees2 = household_degrees2[(household_degrees2["Sex"] == "Both Sexes")]
# changing the datatypes of household_degrees2 dataset
household_degrees2["Not a High School Graduate Mean"] = household_degrees2["Not a High School Graduate Mean"].astype(float)
household_degrees2["High School Graduate Mean"] = household_degrees2["High School Graduate Mean"].astype(float)
household_degrees2["Some College/Associate's Degree Mean"]= household_degrees2["Some College/Associate's Degree Mean"].astype(float)
household_degrees2["Bachelor's Degree Mean"] = household_degrees2["Bachelor's Degree Mean"].astype(float)
household_degrees2["Advanced Degree Mean"] = household_degrees2["Advanced Degree Mean"].astype(float)
household_degrees2["United States"] = household_degrees2["United States"].astype(float)
household_degrees2["Total Mean"] = household_degrees2["Total Mean"].astype(float)

#Graph

houseincome_fig = px.line(household_degrees2, y=["Not a High School Graduate Mean","High School Graduate Mean", "Some College/Associate's Degree Mean", 
"Bachelor's Degree Mean","Advanced Degree Mean"], x="Year", color= "Race")

houseincome_fig.update_layout(title="Average Household Income for the Different Identified Races",
                  xaxis_title="Year", yaxis_title="Average Household Income", showlegend = True)

houseincome_fig.update_layout(xaxis = dict(tickmode = 'array',tickvals = [2015,2016,2017,2018,2019],))

houseincome_fig.update_traces(marker_size=10)
houseincome_fig.update_layout(barmode="group", template='ggplot2')

houseincome_fig.update_layout(
    updatemenus=[
        dict(
            type="dropdown",
            showactive=True,
            buttons=list([
                dict(
                    args=[{'visible': [True, False, False, False, False]},
                          {'title': "Average Household Income of Non-High School Graduates"}],
                    label="No High School",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, True, False, False, False]},
                          {'title': "Average Household Income of High School Graduates"}],
                    label="High School Graduate",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, False, True, False, False]},
                          {'title': "Average Household Income of Some College/Associate's Degree Earners"}],
                    label="Some College/Associates Degree",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, False, False, True, False]},
                          {'title': "Average Household Income of Bachelor's Degree Earners"}],
                    label="Bachelor's Degree",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, False, False, False, True]},
                          {'title': "Average Household Income of Advanced Degree Earners"}],
                    label="Advanced Degree",
                    method="update"
                ),
            ]),
            pad={'r': 10, 't': 10},
            direction="down",
            xanchor="auto",
            yanchor="top"
        ),
    ]
)

# creating degrees_years1 dataset and adding filters for exploratory question #5
degrees_years1= degrees[["Year", "Total Mean", "Sex", "Race", "Not a High School Graduate Mean", "High School Graduate Mean", "Some College/Associate's Degree Mean", "Bachelor's Degree Mean", "Advanced Degree Mean"]]
degrees_years1= degrees_years1[(degrees_years1['Year'] == 2019)|(degrees_years1['Year'] == 2018)|(degrees_years1['Year'] == 2017)|(degrees_years1['Year'] == 2016)|(degrees_years1['Year'] == 2015)]
degrees_years1 = degrees_years1[(degrees_years1['Sex'] == 'Both Sexes')]
degrees_years1 = degrees_years1[(degrees_years1['Race'] =='Total')]

# changing the datatypes for degrees_years1 dataset
degrees_years1.dtypes
degrees_years1["Total Mean"] = degrees_years1["Total Mean"].astype(float)
degrees_years1["Not a High School Graduate Mean"] = degrees_years1["Not a High School Graduate Mean"].astype(float)
degrees_years1["High School Graduate Mean"] = degrees_years1["High School Graduate Mean"].astype(float)
degrees_years1["Some College/Associate\'s Degree Mean"] = degrees_years1["Some College/Associate\'s Degree Mean"].astype(float)
degrees_years1["Bachelor\'s Degree Mean"] = degrees_years1["Bachelor\'s Degree Mean"].astype(float)
degrees_years1["Advanced Degree Mean"] = degrees_years1["Advanced Degree Mean"].astype(float)
degrees_years1["Sex"] = degrees_years1["Sex"].astype(str)
degrees_years1["Race"] = degrees_years1["Race"].astype(str)

# Does household income correlate to educational attainment? How has income changed?
# create trace1
trace1 = go.Bar(
    x=data1.record_year,
    y=data1.mean_not_high_school_graduate,
    name="Income of Non High school Graduates",
    text=data1.mean_not_high_school_graduate)
# create trace2
trace2 = go.Bar(
    x=data1.record_year,
    y=data1.mean_high_school_graduate,
    name="Income of High school Graduates",
    text=data1.mean_high_school_graduate)

# create trace3
trace3 = go.Bar(
    x=data1.record_year,
    y=data1.associate_degree_mean,
    name="Income of Associate Degree Graduates",
    text=data1.associate_degree_mean)

# create trace4
trace4 = go.Bar(
    x=data1.record_year,
    y=data1.bachelor_degree_mean,
    name="Income of Bachelor Degree Graduates",
    text=data1.bachelor_degree_mean)

# create trace5
trace5 = go.Bar(
    x=data1.record_year,
    y=data1.advanced_degree_mean,
    name="Income of Advanced Degree Graduates",
    text=data1.advanced_degree_mean)

data = [trace1, trace2, trace3, trace4, trace5]
layout = go.Layout(
    barmode="group", title="Household Income vs Education")
fig = go.Figure(data=data, layout=layout)

fig.update_layout(xaxis_title="Year", yaxis_title="Average Household Income", template='ggplot2')
# iplot(fig)

# Average state income
trace6 = go.Bar(
    x=data2.state_name,
    y=data2.average_income,
    name="States and their average incomes",
    text=data2.average_income)

layout2 = go.Layout(
    barmode="group", title="States and their average incomes", paper_bgcolor='#C3F6F7')
fig2 = go.Figure(data=trace6, layout=layout2)
# iplot(fig2)

fig3 = go.Figure(data=go.Choropleth(
    locations=data3.state_ab, # Spatial coordinates
    z = data3.average_income, # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Greens',
    autocolorscale=False,
    colorbar_title = "Average Income",
    marker_line_color='black'
))

fig3.update_layout(
    title_text = 'Average Income Based on State',
    geo_scope='usa', # limit map scope to USA
    paper_bgcolor='#C3F6F7',
    margin=dict(l=100, r=60, t=50, b=50)
)

# Creating trace
trace7 = go.Scatter(
                    x = data4.record_year,
                    y = data4.median_household_income,
                    mode = "lines",
                    name = "income",
                    text= data4.median_household_income)

layout = dict(title = 'Median Houshold Income Over the Years 2000 - 2021',
              xaxis= dict(title= 'Year',ticklen= 5,zeroline= False),paper_bgcolor='#C3F6F7', template='ggplot2'
             )
fig4 = go.Figure(data = trace7, layout = layout)

fig4.update_layout(xaxis_title="Year", yaxis_title="Average Household Income")
# Creating trace
trace8 = go.Scatter(
                    x = data5.record_year,
                    y = data5.total_working_population,
                    mode = "lines",
                    name = "income",
                    text= data5.total_working_population)

layout = dict(title = 'Total American Working Population Over the Years 2000 to 2022',
              xaxis= dict(title= 'Year',ticklen= 5,zeroline= False),paper_bgcolor='#C3F6F7', template='ggplot2'
             )
fig5 = go.Figure(data = trace8, layout = layout)

fig5.update_layout(xaxis_title="Year", yaxis_title="Working Population Count")

trace9 = go.Bar(
    x=data6.year_delta,
    y=data6.percent_change,
    name="States and their average incomes",
                text=data6.percent_change)

layout = go.Layout(
    barmode="group", title="Percent Change in Average Income from 2015 to 2021.", paper_bgcolor='#C3F6F7', template='ggplot2')
fig6 = go.Figure(data=trace9, layout=layout)

fig6.update_layout(xaxis_title="Year", yaxis_title="Total Perceent Change")

trace10 = go.Bar(
    x=data7.year_delta,
    y=data7.college_percent,
    name="Y-O-Y College Education Attainment",
    text=data7.college_percent)
# create trace2
trace11 = go.Bar(
    x=data7.year_delta,
    y=data7.school_percent,
    name="Y-O-Y High School Education Attainment",
    text=data7.school_percent)

data = [trace10, trace11]
layout = go.Layout(
    barmode="group", title="Percent Change in Educational Attainment (for Each Level) from 2015 to 2021.", paper_bgcolor='#C3F6F7', template='ggplot2')
fig7 = go.Figure(data=data, layout=layout)

fig7.update_layout(xaxis_title="Year", yaxis_title="Total Percent Change")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Dashboard
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Questions", className="display-4"),
        html.Hr(),
        html.P(
            "Explore the different graphs that answer each question.", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Question 1", href="/page-1", active="exact"),
                dbc.NavLink("Question 2", href="/page-2", active="exact"),
                dbc.NavLink("Question 3", href="/page-3", active="exact"),
                dbc.NavLink("Question 4", href="/page-4", active="exact"),
                dbc.NavLink("Question 5", href="/page-5", active="exact"),
                dbc.NavLink("Machine Learning", href="/page-6", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.H1(children='The Correlation Between Education Attainment, Employment, and Income', style = {'textAlign':'center','marginTop':40,'marginBottom':40, 'font-family':'verdana', 'font-weight':'bold', 'font-size':50, 'color':'white'}),\
            html.H3("The purpose of this dashboard is to explore datasets about Education, Income, and Unemployment Rates in the US. Our goal was to compare the different datasets and to answer any questions we had surrounding them. \
            We focused our research of the data through the various years to see how the data has changed. Questions that were answered were as follows: What is the per capita income for the different levels of education? What is the average household income per state compared to the US as a whole? \
            Does household income correlate to educational attainment? What is the unemployment rate for the different levels of education? How has educational attainment changed throughout the years in the US? How has income changed?",style = {'font-family':'verdana', 'font-size':35})
    elif pathname == "/page-1":
        return html.H2("What is the per capita income for the different levels of education?"), dcc.Graph(id='sex-income-graph',figure=sex_fig), dcc.Graph(id='race-income-graph',figure=race_fig)
    elif pathname == "/page-2":
        return html.H2("What is the average household income per state compared to the US as a whole?"), dcc.Graph(id='household-income-graph',figure=houseincome), \
            dcc.Graph(id='income-by-state-graph', figure={
        'data': [
            go.Choropleth(
                locations=state_income['State'],
                z=state_income['Median Household Income by State: 1990'],
                locationmode='USA-states',
                colorscale='reds',
                colorbar=dict(title='Median Household Income by State: 1990'),
                zmin=25000,
                zmax=max(state_income['Median Household Income by State: 1990']),
                marker=dict(line=dict(width=0.7))
            )
        ],
        'layout': go.Layout(
            title='Median Household Income by State from 1990 to 2019',
            geo=dict(
                scope='usa',
                projection=go.layout.geo.Projection(type='albers usa'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'
            ),
            updatemenus=[dict(
                type='buttons',
                showactive=True,
                buttons=[
                    dict(
                        label='Play',
                        method='animate',
                        args=[None, {'frame': {'duration': 800, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 100}}]
                    ),
                    dict(
                        label='Pause',
                        method='animate',
                        args=[
                            [None],
                            {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}
                        ]
                    )
                ]
            )]
        ),
        'frames': [go.Frame(
            data=[
                go.Choropleth(
                    locations=state_income['State'],
                    z=state_income['Median Household Income by State: {}'.format(year)].astype(float),
                    locationmode='USA-states',
                    autocolorscale=False,
                    colorbar=dict(title='Median Household Income by State: {}'.format(year)),
                )
            ]
        ) for year in years]
    })
    elif pathname == "/page-3":
        return html.H2("What is the unemployment rate for the different levels of education?"), dcc.Graph(id='working-pop-graph', figure=fig5), dcc.Graph(id='unemployment-rate-graph',figure= unemployment_fig), \
                dcc.Graph(id='employment-rate-graph',
        figure={
            'data': [
                go.Bar(x=degree_employment_rates["Education Attainment"], y=degree_employment_rates["Employment-population ratio"],name='Employment Rates'),
                go.Bar(x=degree_employment_rates["Education Attainment"], y=degree_employment_rates["Unemployment rate"],name='Unemployment Rates', base="Employed"),
            ],
            'layout': go.Layout(
                title='Unemployment VS Employment Rates for the Education Attainment Levels of a Civilian Labor Force in 2020',
                xaxis={'title': 'Educational Attainment'},
                yaxis={'title': 'Rate'},
                barmode='stack',
                paper_bgcolor='#C3F6F7',
                template='ggplot2',
                updatemenus=[
                    dict(
                        buttons=list([
                            dict(
                                args=[{'visible': [True, True]},{'title': 'Unemployment VS Employment Rates for the Education Attainment Levels of a Civilian Labor Force in 2020'}],
                                label='Both',
                                method='update'
                            ),
                            dict(
                                args=[{'visible': [True, False]},{'title': 'Employment Rates'}],
                                label='Employment Rates',
                                method='update'
                            ),
                            dict(
                                args=[{'visible': [False, True]},{'title': 'Unemployment Rates'}],
                                label='Unemployment Rates',
                                method='update'
                            )
                        ]),
                        direction='down',
                        pad={'r': 10, 't': 10},
                        showactive=True,
                        x=0.1,
                        xanchor='right',
                        y=1.1,
                        yanchor='auto'
                    ),])}),
    elif pathname == "/page-4":
        return html.H2("Does household income correlate to educational attainment?"),dcc.Graph(id='household-income-fig',figure= houseincome_fig), dcc.Graph(id='bar1', figure=fig),
    elif pathname == "/page-5":
        return html.H2("How has educational attainment changed throughout the years in the US? How has income changed?"),dcc.Graph(id='year-income-graph',
        figure={
            'data': [
                go.Scatter(name='Not a High School Graduate', y=degrees_income_year["Not a High School Graduate Mean"], x=degrees_income_year["Year"]),
                go.Scatter(name='High School Graduate', y=degrees_income_year["High School Graduate Mean"], x=degrees_income_year["Year"]),
                go.Scatter(name="Some College/Associate's Degree", y=degrees_income_year["Some College/Associate's Degree Mean"], x=degrees_income_year["Year"]),
                go.Scatter(name="Bachelor's Degree", y=degrees_income_year["Bachelor's Degree Mean"], x=degrees_income_year["Year"]),
                go.Scatter(name="Advanced Degree", y=degrees_income_year["Advanced Degree Mean"], x=degrees_income_year["Year"]),
            ],
            'layout': go.Layout(
                title='Per Capita Income for the Different Education Attainment Levels through 2010 to 2019',
                xaxis={'title': 'Year'},
                yaxis={'title': 'Per Capita Income Average'},
                barmode='group',
                template='ggplot2',
                paper_bgcolor='#C3F6F7'
            )}),dcc.Graph(id='ed-change-graph', figure=fig7),dcc.Graph(id='household_avg_fig', figure=fig4),dcc.Graph(id='income_year_graph',
        figure={
            'data': [
               go.Scatter(name='Estimated Average Income', y=income_year["Mean Income Estimate"], x=income_year["Year"]),
                
            ],
            'layout': go.Layout(
                title="Estimated Average Income for 2015 to 2019 in the US",
                xaxis = {
                    "tickmode" : 'array',
                    "tickvals" : [2015,2016,2017,2018,2019],
                    "title" : "Year"},
                yaxis={'title': 'Mean Income Estimate'},
                template = 'ggplot2',
                barmode='stack',
                paper_bgcolor='#C3F6F7'
            )}),dcc.Graph(id='percent-change-graph', figure=fig6),dcc.Graph(id='idk', figure=income_allyears_fig)
    elif pathname == "/page-6":
        return html.H2("Can we predict whether or not an individual is unemployed?"), html.Img(src=DTR_path), html.Img(src=KNN_path), html.H3("Scores: Decision Tree = 0.78, KNN = 0.57, Linear Regression: 0.54, Ridge: 0.54"),\
                html.Img(src=LR_path),\
                    html.Img(src=RR_path)
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == '__main__':
    app.run_server(debug=True)


