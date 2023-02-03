# The Correlation Between Education Attainment, Income and Employment Rates in The US
## Authors
Zeeshan Pervaiz, Sarvani Dantuluri, Rob Dewan, Cheyenne Peterson
## Introduction
The objective of this project is to analyze and compare various datasets relating to Education, Income, and Unemployment Rates in the United States. Our aim is to gain a deeper understanding of the relationship between these factors and to answer questions that arose during our research. We carefully examined the data over the years to observe any trends or changes that have occurred. Our research focused on the following questions:

  1. What is the average per capita income for individuals with different levels of education? 
  2. How does the average household income in each state compare to the national average? 
  3. Is there a correlation between household income and educational attainment? 
  4. What is the unemployment rate among individuals with varying levels of education? 
  5. How has educational attainment evolved over time in the United States and how has the income changed accordingly?
  
Through our extensive analysis of the available data, we aim to provide insights and a thorough understanding of the complex relationships between Education, Income, and Unemployment Rates in the United States. Our hypothesis is that there is a relationship between Education, Income, and Unemployment Rates in the United States, and that this relationship has evolved over time.
## Repo Library
**Folder**  | **Contents**
------------- | -------------
Dashboard  | Python file for and code components to create Dash dashboard
Deliverables  | PDF files required to hand in for project, includes PMP, napkin drawings, presentation slides, etc.
EDA | EDA report and CSVs/PKLs that show intial data exploration and explanations
clean-csv | CSVs after intial ETL
clean-pickle | Pickle formatted files after inital ETL
data-capstone | Initial imported datasets and exploration notebooks
data-cleaning | Extra files used for ETL


## Data Processing and ETL
In this project, there were a total of four datasets that were gathered to study the relationship between education attainment, employment, individual income, and household income. These datasets were primarily obtained from the Bureau of Labor and Statistics and the U.S. Census Bureau. The data used was converted into a csv file and later transformed into a dataframe for the purpose of creating a SQL database and visualizations for the dashboard. The following is a list of the four datasets with details, and the sources are listed in the references.
Name  | Description | Columns/Data Types | Shape
------------- | ------------- | ------------- | -------------
Cpsaat_2015_2021 = SQL Table: Employment | The employment status of the civilian noninstitutional population 25 years and over by educational attainment, sex, and race. | Civilian noninstitutional population(int), Civilian labor force(int), Participation rate(float), Employed(float), Employment-population ratio(float), Unemployed(float), Unemployment rate(float), Sex(str), Race(str), Year(int) | (392,10)
Table-A2 = SQL Table: Income | Households by total money income and race of householder: 1967 to 2021 | Race(str), Year(int), Number(Thousands)(float), Total Percent Distribution(float), Under $15000(float), $15000 to $24000(float), $25000 to $34999(float), $35000 to $49000(float), $50000 to $74999(float), $75000 to $99999 (float), $100000 to $149999(float), $150000 to $199999(float), $200000 and over(float), Median Income Estimate(float), Median Income Margin of Error(float), Mean Income Estimate(float), Mean Income Margin of Error(float) | (437,17)
Tabn102-30 = SQL Table: Household | Median household income by state: selected years, 1990 through 2019 | State (str), Median Household Income by State: 1990(int), Median Household Income by State: 2000(int), Median Household Income by State: 2005(int), Median Household Income by State: 2010(int), Median Household Income by State: 2014(int), Median Household Income by State: 2015(int), Median Household Income by State: 2016(int), Median Household Income by State: 2017(int) , Median Household Income by State: 2018(int), Median Household Income by State: 2019(int) | (52,11)
Taba-3 = SQL Table: Degrees | Mean earnings of workers 18 years and over, by educational attainment, race, and sex: 1975-2020 | Race(str), Sex(str), Year(int), Total Mean(float), Total Number with Earnings(float), Not a High School Graduate Mean(float), Not a High School Graduate Numbers with Earnings(float), High School Graduate Mean(float), High School Graduate Numbers with Earnings(float), Some College/Associate’s Degree Mean(float), Some College/Associate’s Degree with Earnings(float), Bachelor’s Degree Mean(float), Bachelor’s Degree Numbers with Earnings(float), Advanced Degree Mean(float), Advanced Degree Numbers with Earnings(float) | (872,15)

## Results
[Project Report](Deliverables/CapstoneProjectTechnicalReport.pdf)

## Sources
CPS Tables :  U.S. Bureau of Labor Statistics. (2023, January 25). https://www.bls.gov/cps/tables.htm

Median household income, by state: Selected years, 1990 through 2019. (n.d.). https://nces.ed.gov/programs/digest/d21/tables/dt21_102.30.asp

Multi-Page Apps and URL Support | Dash for Python Documentation | Plotly. (n.d.). https://dash.plotly.com/urls

Styling. (n.d.). https://plotly.com/python/styling-plotly-express/

US Census Bureau. (2022, July 4). Educational Attainment. Census.gov. https://www.census.gov/topics/education/educational-attainment.html

Wan, M. (2021, December 14). Beginner’s Guide to Building a Multi-Page App using Dash, Plotly and Bootstrap. Medium. https://towardsdatascience.com/beginners-guide-to-building-a-multi-page-dashboard-using-dash-5d06dbfc7599


  
