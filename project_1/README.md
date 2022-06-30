# Project 1. hh.ru CV analysis

## Content

[1. Project description](https://github.com/mvulf/sf_data_science/tree/main/project_1/README.md#Project-description)

[2. Case details](https://github.com/mvulf/sf_data_science/tree/main/project_1/README.md#Case-details)

[3. Data specification](https://github.com/mvulf/sf_data_science/tree/main/project_1/README.md#Data-specification)

[4. Project stages](https://github.com/mvulf/sf_data_science/tree/main/project_1/README.md#Project-stages)

[5. Results](https://github.com/mvulf/sf_data_science/tree/main/project_1/README.md#Results)

[6. Conclusion](https://github.com/mvulf/sf_data_science/tree/main/project_1/README.md#Conclusion)

### Project description

Problem: some candidats do not specify desired salary in their CV on hh.ru platform.

Global target: create a ML-model for predicting candidats desired salary.

Goal of this project: analyse CV database downloaded from hh.ru.

:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_1/README.md#Content)

### Case details
Necessary to provide Data Understanding and Data Preparation stages of Data Mining.

**Practice:**
- Working with .ipynb
- Data analysis and preparation by Pandas
- Visualisation by Plotly and Seaborn

:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_1/README.md#Content)

### Data specification
- HH.ru [CV-database](https://1drv.ms/u/s!AozIrkgfTyZEgdBLn2M4oscTTgwZrg?e=qpq7Md). Main dataset for analysing.
- Exchange rates [database](https://github.com/mvulf/sf_data_science/tree/main/project_1/data/ExchangeRates.csv). For convertation other currencies to rub.

:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_1/README.md#Content)

### Project stages
1. Base data structure analysis

2. Data processing
 
3. Exploratory Data Analysis

4. Data cleaning


:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_1/README.md#Content)

### Results

- Base data structure analysis show, that there are 44744 CV with 12 object-features.
- There were a lot of features with combination of different data, as gender-age-bitrh date combination, etc. These features have been splitted to several features.
- Also there were features as "working hours type" which were processed by One Hot encoding.
- Desired salary feature was converted to rub for further analysing by using Exchange Rates.
- Exploratory data analysis results such as plots and conclusions are introduced in Project 1 file. 
- Data was cleaned from full duplicates and outliers. Missed values were filled out.

:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_1/README.md#Content)

### Conclusion

Thus, data was analysed and prepared for further modelling steps. Education, City, readiness to buisness trip and to move and Experiense are important features for desire salary prediction.

:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_1/README.md#Content)