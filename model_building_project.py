

#1. Prerequisites, Libraries and Packages

Import all basic libraries
"""

import numpy as np                          #for linear algebra
import pandas as pd                         #for data manipulation
import matplotlib.pyplot as plt             #for visualization

import seaborn as sns                       #for visualization

pd.set_option('display.max_columns',None)   #to display all columns in a data set

import warnings                             #to avoid warning flash
warnings.filterwarnings('ignore')

"""#2. Data Preparation

##2.1 Import the data

"""

df = pd.read_csv("/content/Uncleaned_Data.csv")
df.head()

"""##2.2 Brief explation of columns

| Header                   | Description                                       |
|--------------------------|---------------------------------------------------|
| age                      | Respondent’s age                                 |
| race                     | Respondent’s race                                |
| gender                   | Respondent’s gender                              |
| employment               | Respondent’s employment type                     |
| education                | Respondent’s education level                     |
| married                  | Respondent’s marital status                      |
| person_living_in_house   | Number of persons living in respondent’s house   |
| salary                   | Respondent’s monthly salary                      |
| house_type               | Type of house (with ownership status)            |
| house_value              | Current house value                              |
| vehicle                  | Type of vehicle owned by respondent              |
| house_rental_fee         | Monthly rental fee                                |
| house_loan_pmt           | Monthly installment for house loan               |
| transport_use            | Type of transportation used by respondent        |
| transport_spending       | Average monthly spending on own transportation  |
| public_transport_spending | Average monthly spending on public transportation |
| house_utility            | Average monthly spending on house utilities      |
| food_spending            | Average monthly spending on food                 |
| kids_spending            | Average monthly spending on kids’ necessities    |
| personal_loan            | Monthly installment for personal loan             |
| education_loan           | Monthly installment for education loan            |
| other_loan               | Monthly installment for other loans              |
| investment               | Average monthly spending on investment            |
"""

print("Dataset")
print(df.shape)
print("Number of rows: "+str(df.shape[0]))
print("Number of columns: "+str(df.shape[1]))

"""#3. Exploratory Data Analysis

3.01 Check descriptive statistics
"""

df.describe(include = 'all').T

df.info()

"""## 3.1 Data Cleaning

3.11 Check missing values

"""

missing_values = df.isnull().sum().sort_values(ascending=False)
percentage_missing = (missing_values / len(df)) * 100

missing_info = pd.concat([missing_values, percentage_missing], axis=1)
missing_info.columns = ['Missing Values', 'Percentage Missing']

print(missing_info)

"""As we can see, most of our columns contain misssing values

**Approach to Missing Values**

FootNote
- mean
- median
- mode
- Previous row
- Fully Drop
---
Ways
- mean
- median
- mode
- Fully Drop
---
KDEplot, Histogram
- All Features
- Do not include target

3.12 Separate for numerical features and non-numerical features
"""

df.columns

num = df.select_dtypes(include=['int64', 'float64']).columns  # numerical columns
cat = df.select_dtypes(include=['object']).columns  # non-numerical (categorical) columns

num

"""3.13 Check the distribution of each features to decide the approach for missing values imputation. **Numerical Features**


"""

# Define the number of columns for subplots
num_columns = 2
num_rows = int(np.ceil(len(num) / num_columns))

# Create a figure and axis for subplots
fig, axes = plt.subplots(num_rows, num_columns, figsize=(6, 10))

# Flatten the 2D axes array to simplify indexing
axes = axes.ravel()

# Loop through the features and create histograms
for i, feature in enumerate(num):
    ax = axes[i]
    sns.histplot(data=df, x=feature, ax=ax, kde=True)
    ax.set_title(f'{feature}')
    ax.set_xlabel('')

# Remove any empty subplots
for i in range(len(num), num_rows * num_columns):
    fig.delaxes(axes[i])

# Adjust layout
plt.tight_layout()
plt.show()

"""We have to choose either median or mean for numerical feature but we choose median here because most of our features are right-skewed, so the suitable approach is **median**.

3.14 Check the distribution of each features to decide the approach for missing values imputation. **Categorical Features - Non-numerical**
"""

cat

# Define the number of columns for subplots
num_columns = 2
num_rows = int(np.ceil(len(cat) / num_columns))

# Create a figure and axis for subplots
fig, axes = plt.subplots(num_rows, num_columns, figsize=(20, 10))

# Flatten the 2D axes array to simplify indexing
axes = axes.ravel()

# Loop through the features and create histograms
for i, feature in enumerate(cat):
    ax = axes[i]
    sns.countplot(data=df, x=feature, ax=ax)
    ax.set_title(f'{feature}')
    ax.set_xlabel('')

# Remove any empty subplots
for i in range(len(cat), num_rows * num_columns):
    fig.delaxes(axes[i])

# Adjust layout
plt.tight_layout()
plt.show()

"""The suitable approach to impute missing values for non-numerical are `mode`
we will remove `house_value` column as it approach 50% missing values

Approach for missing values imputation

1. Median - All missing numerical values
2. Mode all missing non-numerical values except `house_value` column
3.Drop Whole column - `house_value` by drop col

3.15 Create Backup Data for impute note in case we want to go back later for correction.
"""

#create a backup first before running the code to retrieve back later the original one
df_backup = df.copy()

df = df_backup.copy()

df.info()

"""3.16 Execute Imputation for missing values"""

median_impute = ['house_rental_fee',
                 'house_loan_pmt',
                 'transport_spending',
                 'public_transport_spending',
                 'house_utility',
                 'food_spending',
                 'kids_spending',
                 'personal_loan',
                 'education_loan',
                 'other_loan',
                 'investment']

mode_impute = ['employment',
               'education',
               'married',
               'person_living_in_house',
               'house_type',
               'vehicle',
               'transport_use']

drop_col = ['house_value']

# Median
for col in median_impute:
  median_values = df[col].median()
  df[col].fillna(median_values, inplace=True)

# Mode
for col in mode_impute:
  mode_values = df[col].mode()
  df[col].fillna(mode_values[0], inplace=True)

# Drop Whole Column
df = df.drop(drop_col, axis=1)

# Drop Whole Rows
df = df.dropna(subset=['salary'])

df.info()

"""3.17 Check Duplicates

"""

df[df.duplicated()].count()

df.drop_duplicates(keep='first',inplace=True)

df[df.duplicated()].count()

"""3.18 Check Inconsistencies

check logic or not whether per say age 1000 years old ,not happen here (check min and max)
"""

df.describe().T

"""It seems that our data all has consistent values

Now ,our dataset already cleaned

##3.2 Data Formatting
"""

df.head()

"""3.21 Features to be formatted.
(We have to format it so that it would be easy for machine to read)

- employment
- salary
- house_type
- vehicle
- transport_use
- married
- education
- gender
- race

Replace categorical features;
1. One Hot Encoding - Use if there is no 'ranking' between categories

Example male ,female

2. Label Encoder - Use if there is 'ranking' between categories

Example : cold ,average, hot

Footnote
Dictionary : {key:value}
List: []

**person_living_in_house**
"""

df.person_living_in_house.value_counts()

"""Change "10 or more" to "10" and change the dtype to int."""

df['person_living_in_house'] = df['person_living_in_house'].replace('10 or more','10').astype(int)

df.person_living_in_house.value_counts()

"""**age**

"""

df.age.value_counts()

"""Group together as group category:

0-9,10-19,...,80-89
"""

bins = [20,29,39,49,59,69,79,89]
labels = ['20-29','30-39','40-49','50-59','60-69','70-79','80-89']

# create age_class column based on age class ranges
df['age_class'] = pd.cut(df['age'],bins=bins ,labels=labels ,right=False)

# Drop "age"  column
df.drop(columns=['age'],inplace=True)

bin_value = df['age_class'].nunique()

# Create a histogram of the 'tenure' column
plt.figure(figsize=(4, 2))
sns.histplot(data=df, x='age_class', bins=bin_value,kde=True)
plt.title('Distribution of Age')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

df.age_class.value_counts()

age_class = { '20-29' : 0,
              '30-39' : 1,
              '40-49' : 2,
              '50-59' : 3,
              '60-69' : 4,
              '70-79' : 5,
              '80-89' : 6,
            }

"""**employment**"""

df.employment.value_counts() #label encoding (unemployed=0, others=1, self-employed=2, Private sector retiree=3, gov retiree=4, employed=5)

employment = {'Unemployed':0,
              'Others':1,
              'Self-employed':2,
              'Private sector retiree':3,
              'Government retiree':4,
              'Employed':5
              }

"""**salary**"""

df.salary.value_counts() #label encoding for B=0 , M= 1

"""Salary less than 5k is 0(B) ,while salary more than 5k is 1(M)"""

salary = {'Less than 1K': 0,
          '1K to 2K': 0,
          '2K to 3K': 0,
          '3K to 4K': 0,
          '4K to 5K': 0,
          '5K to 6K': 1,
          '10K or more': 1,
          '7K to 8K': 1,
          '9K to 10K': 1,
          '8K to 9K': 1
         }

"""**house_type**"""

df.house_type.value_counts() #one hot encoding combine based on own , rental, parent

"""Group together categories into larger group ,own ,rental and parent"""

house_type = {'Parent\'s house' : 'Parent',
              'Own house - one storey terrace' : 'Own',
              'Own house - kampung / wooden house' : 'Own',
              'Own house - double storey terrace' : 'Own',
              'Own house - flat' : 'Own',
              'Own house - bungalows' : 'Own',
              'Own house - condominiums' : 'Own',
              'Rental house - single storey' : 'Rental',
              'Rental house - flat' : 'Rental',
              'Rental house - kampung / wooden house' : 'Rental',
              'Rental house - double storey terrace' : 'Rental',
              'Rental house - condominiums' : 'Rental',
              'Rental house - bungalows' : 'Rental'
              }

"""**vehicle**"""

df.vehicle.value_counts() ##label encoding combine based on local vs import ,no vehicle

"""Combine into larger group: local,Import,motorcycle,no_vehicle"""

vehicle = {'Local brand car' : 'Local',
           'Asia brand car' : 'Import',
           'Europe brand car' : 'Import',
           'Motorcycle' : 'Motorcycle',
           'Did not own any vehicle' : 'no_vehicle'
          }

"""**transport_use**"""

df.transport_use.value_counts() #label encoding (public=0, both=1, own=2)

transport_use = {'Public transport' : 0,
                 'Own transport & Public transport' : 1,
                 'Own transport' : 2
                }

"""Make label encode: Public=0, Both=1, Own=2

**married**
"""

df.married.value_counts() #label encoding (No=0,divorce=1, yes=2)

married = {'Yes' : 2,
           'No' : 0,
           'Divorcee' : 1
          }

"""Make label encode: Public=0, Both=1, Own=2

**education**
"""

df.education.value_counts() #label encoding (high school=0,certificate=1,diploma=2, bd=3)

education = {'High School' : 0,
             'Bachelor\'s Degree' : 3,
             'Diploma' : 2,
             'Certificates' : 1
            }

"""Make label encode: High School=0, Certificates=1, Diploma=2, Bachelor's Degree=3

**gender**
"""

df.gender.value_counts() #one hot encoding

"""**race**"""

df.race.value_counts() #one hot encoding

"""3.22 Approach for encoding columns:
1. Label Encoding:
- employment
- salary
- transport_use
- married
- education

2. One-hot Encoding
- house_type
- gender
- race
- vehicle

3.23 Before we do encoding ,create backup first
"""

df_backup = df.copy()

# Label encoding features
label_encoding_features = ['employment',
                            'salary',
                            'transport_use',
                            'married',
                            'education',
                            'age_class']

# One Hot features
one_hot_features = ['house_type',
                    'gender',
                    'vehicle',
                    'race']

"""3.24 Label Encoding"""

label_encoding_mapping = {'employment' : employment,
                          'salary' : salary,
                          'vehicle' : vehicle,
                          'transport_use' : transport_use,
                          'married' : married,
                          'education' : education,
                          'age_class' : age_class
                          }

for feature in label_encoding_mapping:
  df[feature] = [label_encoding_mapping[feature][val] for val in df[feature] if not pd.isna(val)]

"""3.25 One hot Encoding

Remember to map the house_type ,vehicle first
"""

for key, val in house_type.items():
    df.loc[df['house_type'] == key, 'house_type'] = val

for key, val in house_type.items():
    df.loc[df['vehicle'] == key, 'vehicle'] = val

#check
df['house_type'].value_counts()

df['vehicle'].value_counts()

"""Now,proceed to one hot encoding"""

df = pd.get_dummies(df,columns=one_hot_features)

df.head()

df.salary.value_counts()

"""## 3.3 Data Distribution (Analytics)"""

#sns.pairplot(df,hue='salary') this one long to run
#sns.boxplot(y='married',x='salary',data=df)

"""**Ex. 1 Kids spending Vs Food Spending**"""

sns.scatterplot(x='food_spending',y='kids_spending',hue='salary',data=df)

"""As we can see, M(1) tends to spend more in their food and kid if compared to B(0)

**2. Married VS Salary(Boxplot)**
"""

sns.countplot(x='married',hue='age_class',data=df)

"""Most of our numerical features are right-skewed excdpe `age`. These right-skewed features must be transformed.

3.31 For now, we can export our cleaned data.
"""

df.to_csv('cleaned_data.csv',index=False)

"""##3.4 Data Transformation"""

df.columns

len(df.columns)

"""3.41 Separate data of this two features"""

right_skew_numerical_transform = ['house_rental_fee',
                                  'house_loan_pmt',
                                  'transport_spending',
                                  'public_transport_spending',
                                  'house_utility',
                                  'food_spending',
                                  'kids_spending',
                                  'personal_loan',
                                  'education_loan',
                                  'other_loan',
                                  'investment']

categorical_features = ['age_class',
                        'house_type_Own',
                        'house_type_Parent',
                        'house_type_Rental',
                        'gender_F',
                        'gender_M',
                        'race_Kree',
                        'race_Others',
                        'race_Sapiens',
                        'race_Skrull',
                        'vehicle_Import',
                        'vehicle_Local',
                        'vehicle_Motorcycle',
                        'vehicle_No_Vehicle',
                        'employment',
                        'transport_use',
                        'married',
                        'education',
                        'age_class']

len(right_skew_numerical_transform)+len(categorical_features)

"""3.42 We will construct a column transformer pipeline each:

1. Right skewed numerical features:

- Log Transform -> RobustScaler() -> StandardScaler()

2. Categorical features:

- Passthrough

Footnote

We do not do for symmetrical because we only have these 2 features
"""

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import FunctionTransformer

# Create a right skew pipeline to first apply Log Transform ,RobustScaler and then MinMaxScaler
preprocessing_pipeline1 = Pipeline([
    ('log1p_transform', FunctionTransformer(func=np.log1p, validate=False)), #convert from right skew to symmetrical
    ('robust_scaling', RobustScaler()), # removes outliers
    ('standard_scaling', StandardScaler()) #standardization ( create similar scale between features)
])

# Create a column transformer using the pipelines for skew and sym features
#change for the preprosseing pipeline 1
transformer = ColumnTransformer(
    transformers=[
        ('Right_skew_num', preprocessing_pipeline1, right_skew_numerical_transform),

    ],
    remainder="passthrough"
)

transformer

df.to_csv('cleaned_dataTransformed.csv',index=False)

"""# 4. Model Development

Footnote
1. Baseline Models
- Logistic Regression
- K-Nearest Neighbors (KNN)
- Support Vector Machine (SVM)

2. Ensemble Models
- Random Forest
- Gradient Boosting
  - Gradient Boosting Classifier
  - Histogram Gradient Boosting Classifier
- XGBoost (eXtreme Gradient Boosting)
- Light Gradient Boosting Machine (LightGBM)

3. Ensemble Methods
- Voting Classifier
- Stacking

4.01 Import Libraries
"""

# Metrics
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.model_selection import cross_val_score, cross_validate, StratifiedKFold

from sklearn.metrics import roc_auc_score

from sklearn.pipeline import Pipeline, make_pipeline

# Import models
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

#for hyperparameter tuning
from sklearn.model_selection import RandomizedSearchCV

"""4.02 Split into dataset into training set and testing set"""

from sklearn.model_selection import train_test_split

X = df.drop("salary", axis=1) # Features/predictor
Y = df["salary"] # Target

# Split dataset
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.10, random_state=1) # 90:10 (Train:Test)

# Check
print ('Train set:', x_train.shape,  y_train.shape)
print ('Test set:', x_test.shape,  y_test.shape)

x_train.columns

x_train.house_type_Own

x_train.head()

"""4.03 Construct model table


"""

models_table = pd.DataFrame(columns=["Model", # Algorithm
                                     "Model Alias", # Nama pendek
                                     "Detail", # Settings model
                                     "Precision",
                                     "Recall",
                                     "F1-score",
                                     "Cross-Validated AUC"]) # How good the model discriminate between classes

models_table = pd.DataFrame(columns=models_table.columns)
models_table.head()

def train_evaluate(model, x_train, y_train, x_test, y_test, X, Y):
    # Train the model
    model.fit(x_train, y_train) # Model will try to learn

    # Predict probabilities and labels
    prediction_prob = model.predict_proba(x_test) # Probability of a class
    prediction = model.predict(x_test) # Exact prediction

    # Calculate accuracy, precision, recall, F1-score, log loss
    test_accuracy = model.score(x_test, y_test)
    train_accuracy = model.score(x_train, y_train)
    precision = precision_score(y_test, prediction)
    recall = recall_score(y_test, prediction)
    f1 = f1_score(y_test, prediction)

    # Cross Validation
    # Stratified sampling instead of random sampling for equal proportion
    stratified_kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

    # Perform cross-validation on the test data and calculate mean accuracy and log loss
    results = cross_validate(model,
                              X,
                              Y,
                              cv=stratified_kf,
                              scoring='roc_auc')

    # Extract the scores
    auc_scores = results['test_score']

    # Calculate the means for each cross validated evaluation metrics
    mean_auc_scores = np.mean(auc_scores)

    # Print the evaluation metrics
    print("---------Debugging---------")
    print(f"AUC: {auc_scores}")
    print("*********Check Overfitting/Underfitting*********")
    print(f"Train Accuracy: {train_accuracy:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print("*********Evaluating Metric*********")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-score: {f1:.4f}")
    print(f"ROC: {mean_auc_scores:.4f}")

    return precision, recall, f1, mean_auc_scores

def model_tab(models_table, model_name, model_alias, model_detail, metrics):
    new_row = {
        "Model": model_name,
        "Model Alias": model_alias,
        "Detail": model_detail,
        "Precision": metrics[0],
        "Recall": metrics[1],
        "F1-score": metrics[2],
        "Cross-Validated AUC": metrics[3]
    }

    row_add = pd.DataFrame([new_row])

    models_table = pd.concat([models_table, row_add], ignore_index=True)

    return models_table

"""##4.1. Logistic Regression

"""

lor1 = Pipeline([
    ('ColumnTransformer', transformer),
    ('Model', LogisticRegression())
])

metrics = train_evaluate(lor1,
                         x_train,
                         y_train,
                         x_test,
                         y_test,
                         X,
                         Y)
metrics

model_name = "Logistic Regression"
model_alias = "lor1"
model_detail = "Default, Scaled"

models_table = model_tab(models_table,
                         model_name,
                         model_alias,
                         model_detail,
                         metrics)
models_table

"""###4.2.Random Forest Classifier"""

rf1 = Pipeline([
    ('ColumnTransformer', transformer),
    ('Model', RandomForestClassifier())
])

metrics = train_evaluate(rf1,
                         x_train,
                         y_train,
                         x_test,
                         y_test,
                         X,
                         Y)
metrics

model_name = "Random Forest"
model_alias = "rf1"
model_detail = "Default, Scaled"

models_table = model_tab(models_table,
                         model_name,
                         model_alias,
                         model_detail,
                         metrics)
models_table

"""###4.3 Support Vector Classifier (SVC)"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# svc1 = Pipeline([
#     ('ColumnTransformer', transformer),
#     ('Model', SVC(probability=True))
# ])
# 
# metrics = train_evaluate(svc1,
#                          x_train,
#                          y_train,
#                          x_test,
#                          y_test,
#                          X,
#                          Y)
# metrics
# 
# model_name = "Support Vector"
# model_alias = "svc1"
# model_detail = "Default, Scaled"
# 
# models_table = model_tab(models_table,
#                          model_name,
#                          model_alias,
#                          model_detail,
#                          metrics)
# models_table

"""###4.4. XG Boost Classifier"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# xgb1 = Pipeline([
#     ('ColumnTransformer', transformer),
#     ('Model', XGBClassifier())
# ])
# 
# metrics = train_evaluate(xgb1,
#                          x_train,
#                          y_train,
#                          x_test,
#                          y_test,
#                          X,
#                          Y)
# metrics
# 
# model_name = "XGB Classifier"
# model_alias = "xgb1"
# model_detail = "Default, Scaled"
# 
# models_table = model_tab(models_table,
#                          model_name,
#                          model_alias,
#                          model_detail,
#                          metrics)
# models_table

"""###4.5. LGBMClassifier"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# lgbm1 = Pipeline([
#     ('ColumnTransformer', transformer),
#     ('Model', LGBMClassifier())
# ])
# 
# metrics = train_evaluate(lgbm1,
#                          x_train,
#                          y_train,
#                          x_test,
#                          y_test,
#                          X,
#                          Y)
# metrics
# 
# model_name = "LGBM Classifier"
# model_alias = "lgbm1"
# model_detail = "Default, Scaled"
# 
# models_table = model_tab(models_table,
#                          model_name,
#                          model_alias,
#                          model_detail,
#                          metrics)
# models_table

import itertools
from sklearn.metrics import confusion_matrix
models_list = [lor1,rf1, svc1, xgb1,lgbm1]
models_list_title = ['lor1', 'rf1','svc1', 'xgb1','lgbm1']

# Define the number of rows and columns for the subplots
n_rows = 2
n_cols = 4
fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 10))
plt.subplots_adjust(wspace=0.5, hspace=0)

for i, model in enumerate(models_list):
    # Predict using the model
    predict = model.predict(x_test)

    # Compute the confusion matrix
    cnf_matrix = confusion_matrix(y_test, predict, labels=[0, 1])

    # Determine the subplot location based on the current index
    row_index = i // n_cols
    col_index = i % n_cols

    # Plot the confusion matrix in the appropriate subplot
    axes[row_index, col_index].imshow(cnf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
    axes[row_index, col_index].set_title(models_list_title[i])
    tick_marks = np.arange(2)
    axes[row_index, col_index].set_xticks(tick_marks)
    axes[row_index, col_index].set_yticks(tick_marks)
    #axes[row_index, col_index].set_xticklabels(['Not Pulsar', 'Pulsar'])
    #axes[row_index, col_index].set_yticklabels(['Not Pulsar', 'Pulsar'])
    thresh = cnf_matrix.max() / 2.0
    for i, j in itertools.product(range(cnf_matrix.shape[0]), range(cnf_matrix.shape[1])):
        axes[row_index, col_index].text(j, i, format(cnf_matrix[i, j], 'd'),
                 horizontalalignment="center",
                 color="white" if cnf_matrix[i, j] > thresh else "black")

# Remove any remaining empty subplots
for i in range(len(models_list), n_rows * n_cols):
    fig.delaxes(axes.flatten()[i])

# Show the subplots
plt.show()

"""# 5. Hyperparameter Tuning

5.1 Random Forest Tuning
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# # Define the hyperparameter grid for RandomForestClassifier
# rf_param_grid = {
#     'n_estimators': [25, 50, 100, 150],
#     'max_features': ['sqrt', 'log2', None],
#     'max_depth': [3, 6, 9],
#     'max_leaf_nodes': [3, 6, 9]
# }
# 
# model_rf = RandomizedSearchCV(
#     estimator=RandomForestClassifier(),
#     param_distributions=rf_param_grid,
#     scoring='roc_auc',  # Use AUC as the scoring metric
#     cv=5,
#     n_iter=200,
#     n_jobs=-1,
#     verbose=3,
# )
# 
# rf2 = Pipeline([
#     ('ColumnTransformer', transformer),
#     ('Model', model_rf)
# ])
# 
# rf2.fit(x_train, y_train)

"""5.11 XGBC Tuning"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# # Define the hyperparameter grid for XGBClassifier
# xgb_param_grid = {
#     'n_estimators': [50, 100, 150, 200],  # Number of boosting stages
#     'learning_rate': [0.001, 0.01, 0.1],  # Step size shrinkage used in update
#     'max_depth': [3, 7, 9],  # Maximum depth of trees
#     'min_child_weight': [1, 2, 4],  # Minimum sum of instance weight needed in a child
#     'gamma': [0, 0.1, 0.2, 0.3],  # Minimum loss reduction required to make a further partition on a leaf node
#     'subsample': [0.5, 0.7, 1.0],  # Fraction of samples used for fitting the trees
#     'reg_alpha': [0.0, 0.1, 0.2, 0.3],  # L1 regularization term on weights
#     'reg_lambda': [0.0, 0.1, 0.2, 0.3]  # L2 regularization term on weights
# }
# 
# model_xgb = RandomizedSearchCV(
#     estimator=XGBClassifier(),
#     param_distributions=rf_param_grid,
#     scoring='roc_auc',  # Use AUC as the scoring metric
#     cv=5,
#     n_iter=200,
#     n_jobs=-1,
#     verbose=3,
# )
# 
# xgb2 = Pipeline([
#     ('ColumnTransformer', transformer),
#     ('Model', model_xgb)
# ])
# 
# xgb2.fit(x_train, y_train)

"""## 5.2 Retrain with Tuned Hyperparameters

5.21 Random Forest Retrain
"""

best_param_rf = model_rf.best_params_

"""These are the best parameters obtained with RadomizedSearchCV"""

best_param_rf

# Commented out IPython magic to ensure Python compatibility.
# 
# %%time
# # Create a model pipeline
# rf2 = Pipeline([
#     ('ColumnTransformer', transformer),
#     ('Model', RandomForestClassifier(**best_param_rf))
#                 ])
# 
# # Function to train and evaluate the model
# metrics = train_evaluate(rf2,
#                          x_train,
#                          y_train,
#                          x_test,
#                          y_test,
#                          X,
#                          Y)
# metrics
# 
# # Note for Table
# model_name = "Random Forest"
# model_alias = "rf2"
# model_detail = "Tuned, Scaled"
# # Function to store the evaluation metrics as table
# models_table = model_tab(models_table,
#                          model_name,
#                          model_alias,
#                          model_detail,
#                          metrics)
# models_table

"""5.22 XGBC Retrain"""

best_param_xgb = model_xgb.best_params_

model_xgb.best_params_

# Commented out IPython magic to ensure Python compatibility.
# %%time
# # Create a model pipeline
# xgb2 = Pipeline([
#     ('ColumnTransformer', transformer),
#     ('Model', XGBClassifier(**best_param_xgb))
#                 ])
# 
# # Function to train and evaluate the model
# metrics = train_evaluate(xgb2,
#                          x_train,
#                          y_train,
#                          x_test,
#                          y_test,
#                          X,
#                          Y)
# metrics
# 
# # Note for Table
# model_name = "XGB Classifier"
# model_alias = "xgb2"
# model_detail = "Tuned, Scaled"
# # Function to store the evaluation metrics as table
# models_table = model_tab(models_table,
#                          model_name,
#                          model_alias,
#                          model_detail,
#                          metrics)
# models_table

"""# 6. Model Evaluation

##6.1AUC-ROC Curve

The AUC-ROC curve (Area Under the Receiver Operating Characteristic curve) is a graphical representation used to assess and compare the performance of classification models, such as binary classifiers.

1. Receiver Operating Characteristic (ROC) Curve: The ROC curve is a graph that displays the performance of a classification model across various classification thresholds. It plots the True Positive Rate (Sensitivity) against the False Positive Rate (1 - Specificity) at different threshold values. The curve shows how well the model distinguishes between the positive and negative classes.

2. Area Under the Curve (AUC): AUC measures the overall performance of a model. It represents the area under the ROC curve. A perfect model has an AUC of 1, while a random model has an AUC of 0.5. The closer the AUC is to 1, the better the model's ability to discriminate between the two classes.
"""

models_list = [lor1, svc1, rf1, xgb1, rf2, xgb2]
models_list_title = ['lor1', 'svc1',  'rf1', 'xgb', 'rf2', 'xgb2']

from sklearn.metrics import roc_curve, auc

# Create an empty list to store AUC values
auc_values = []

# Define classes and labels here
# For example: classes = [0, 1]

# Create a figure and axis for the ROC plot
plt.figure(figsize=(8, 6))

# Iterate through the models
for i, model in enumerate(models_list):
    # Get model predictions
    y_score = model.predict_proba(x_test)[:, 1]  # Adjust if necessary

    # Compute ROC curve
    fpr, tpr, _ = roc_curve(y_test, y_score)

    # Compute AUC
    roc_auc = auc(fpr, tpr)

    # Plot ROC curve with model name from models_list_title
    plt.plot(fpr, tpr, label=f'{models_list_title[i]} (AUC = {roc_auc:.5f})')

    # Store AUC value
    auc_values.append(roc_auc)

# Set plot properties
plt.plot([0, 1], [0, 1], 'k--', lw=2)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.legend(loc='lower right')
plt.show()

# Print AUC values
for i, auc_val in enumerate(auc_values):
    print(f'{models_list_title[i]}: AUC = {auc_val:.5f}')

"""The AUC values serve as a measure of how well each model can classify data. Models with higher AUC values excel in distinguishing between different classes. In our case, all of our models demonstrate strong AUC values, signifying their effectiveness in distinguishing between the classes.

##6.2 Confusion Matrix

A confusion matrix is a fundamental tool for evaluating the performance of a classification model. It helps us understand how well our model is making predictions by comparing the actual and predicted values.
"""

import itertools
from sklearn.metrics import confusion_matrix

# Define the number of rows and columns for the subplots
n_rows = 2
n_cols = 4
fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 10))
plt.subplots_adjust(wspace=0.5, hspace=0)

for i, model in enumerate(models_list):
    # Predict using the model
    predict = model.predict(x_test)

    # Compute the confusion matrix
    cnf_matrix = confusion_matrix(y_test, predict, labels=[0, 1])

    # Determine the subplot location based on the current index
    row_index = i // n_cols
    col_index = i % n_cols

    # Plot the confusion matrix in the appropriate subplot
    axes[row_index, col_index].imshow(cnf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
    axes[row_index, col_index].set_title(models_list_title[i])
    tick_marks = np.arange(2)
    axes[row_index, col_index].set_xticks(tick_marks)
    axes[row_index, col_index].set_yticks(tick_marks)
    #axes[row_index, col_index].set_xticklabels(['Not Pulsar', 'Pulsar'])
    #axes[row_index, col_index].set_yticklabels(['Not Pulsar', 'Pulsar'])
    thresh = cnf_matrix.max() / 2.0
    for i, j in itertools.product(range(cnf_matrix.shape[0]), range(cnf_matrix.shape[1])):
        axes[row_index, col_index].text(j, i, format(cnf_matrix[i, j], 'd'),
                 horizontalalignment="center",
                 color="white" if cnf_matrix[i, j] > thresh else "black")

# Remove any remaining empty subplots
for i in range(len(models_list), n_rows * n_cols):
    fig.delaxes(axes.flatten()[i])

# Show the subplots
plt.show()

"""Class 0 = B
Class 1 = M

If we want to classify the population based on their salary, we prioritize AUC because we want to create a model that can differentiate between classes B and M.
"""

models_table

xgb2

"""Question to be asked
1. Find the model with the highest AUC and F1 Score
2. Mention the AUC Value and F1 Score
3. Is hyperparameter tuning effective?

Firstly,to know whether the model is good or not, we put AUC as the number one consideration and we look at its  Train accuracy whether overfitting or not ,if not we have to consider highest F1 score after the model being tuned.

Now,we know that model that has the highest AUC obtained is from RF1,AUC = 0.930600, but RF1 has the train accuracy equal to 1.0000 which is overfitting. So , we come up with an idea to take XGB2 , because it has the highest F1 Score and AUC after rf1, thus this will be our best selected model.In this case , we consider tuning for this model and we got F1 Score = 0.629630	AUC = 0.929698

#7. Summary

Model that is selected to be the best is xgb2 with F1 Score = 0.629630	AUC = 0.929698 and train accuracy = 0.9440

##7.1 Export Model
"""

import pickle

# Save the pipeline and model to a file
with open('/content/xgbc_model.pkl', 'wb') as file:
    pickle.dump(xgb2, file)

print("Model Dumped!")

"""##7.2 Load Model

Example of how to load the pickle object
"""

# Load the saved pipeline and model
with open('/content/xgbc_model.pkl', 'rb') as file:
    loaded_pipeline = pickle.load(file)

# Make predictions
predictions_train = loaded_pipeline.predict(x_train)
predictions_test = loaded_pipeline.predict(x_test)

# Calculate accuracy, precision, recall, F1-score, log loss
test_accuracy = model.score(x_test, y_test)
train_accuracy = model.score(x_train, y_train)
precision = precision_score(y_test, predictions_test)
recall = recall_score(y_test, predictions_test)
f1 = f1_score(y_test, predictions_test)

# Cross Validation
# Stratified sampling instead of random sampling for equal proportion
stratified_kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

# Perform cross-validation on the test data and calculate mean accuracy and log loss
results = cross_validate(loaded_pipeline,
                          X,
                          Y,
                          cv=stratified_kf,
                          scoring='roc_auc')

# Extract the scores
auc_scores = results['test_score']

# Calculate the means for each cross validated evaluation metrics
mean_auc_scores = np.mean(auc_scores)

# Print the evaluation metrics
print("---------Debugging---------")
print(f"AUC: {auc_scores}")
print("*********Check Overfitting/Underfitting*********")
print(f"Train Accuracy: {train_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")
print("*********Evaluating Metric*********")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-score: {f1:.4f}")
print(f"Mean AUC: {mean_auc_scores:.4f}")
