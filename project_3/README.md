# Project 3. EDA + Feature Engineering. Kaggle

## Content

[1. Project description](https://github.com/mvulf/sf_data_science/tree/main/project_3/README.md#Project-description)
[2. Case details](https://github.com/mvulf/sf_data_science/tree/main/project_3/README.md#Case-details)
[3. Data specification](https://github.com/mvulf/sf_data_science/tree/main/project_3/README.md#Data-specification)
[4. Project stages](https://github.com/mvulf/sf_data_science/tree/main/project_3/README.md#Project-stages)
[5. Results](https://github.com/mvulf/sf_data_science/tree/main/project_3/README.md#Results)
[6. Conclusion](https://github.com/mvulf/sf_data_science/tree/main/project_3/README.md#Conclusion)


### Project description

:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_3/README.md#Content)

Booking data science study case. Problem: dishonest hotels that spin their ratings. Solution: design a reviewer score prediction model. If the predictions of the model differ greatly from the actual result, then perhaps the hotel is being dishonest and worth checking out.

### Case details


**Conditions:**
The model must predict the rating of the hotel according to the Booking website based on the data available in the dataset. MAPE-metrics of this model should be increased by Exploratory data analysis methods.

**Quality metric**
MAPE (mean absolute percentage error)

**Practice:**
- Data analysis and preparation by Pandas
- Visualisation by Plotly and Seaborn
- Exploratory data analysis (EDA)
- Usage of the Random Forest Regressor from Scikit-learn
- Improving the MAPE-metric by feature engineering and selection

:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_3/README.md#Content)

### Data specification
- DataFrame with 515000 Europe hotel reviews: input/hotels_train.csv and input/hotels_test.csv
- Kaggle submission example: input/submission.csv

:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_3/README.md#Content)

### Project stages
1. Preparations

Import libraries and data. Сombining the data.

2. Preliminary data analysis and data preparation

Includes: data understanding, data preparation & cleaning, feature generating.

3. Exploratory data analysis

Consists of: Statistical hypothesis testing (normal-test), Feature Engineering (includes feature generating and feature transformation), Feature Selection (considers multicollinearity and feature importances tests)

4. ML-Modeling

Main stages: data splitting, Instant and fit model. Predict test values; Model quality assessment (MAPE); Final prediction for the output/submission.csv export.

:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_3/README.md#Content)

### Results
In total, the dataset, after data processing and feature generation, had 90 features (out of 17 initial). Then by multicollinearity and feature importances tests features count has been decreased to 53 columns. And then best 15 of them were used for the Random Forest Regressor model.

:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_3/README.md#Content)

### Conclusion

:arrow_up:[to content](https://github.com/mvulf/sf_data_science/tree/main/project_3/README.md#Content)

Thus, EDA techniques have improved MAPE from a base (_base_solution.ipynb) of 14.19%
up to 12.19% (hotels-EDA_ML.ipynb). That is, the improvement was 14% of the base value of the metric.