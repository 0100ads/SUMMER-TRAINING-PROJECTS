# -*- coding: utf-8 -*-
"""Loan prediction using machine learning algorithm.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zo3aVXKS25H8AvCpLMsx5ze5WRZ16Tw_
"""

import warnings
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os #path to file

#ploting data
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# matrix

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

sns.set(style='darkgrid', font='sans-serif', font_scale=1)

#Handling warnings
warnings.filterwarnings("ignore")

train_path = train_df = pd.read_csv('/content/train_u6lujuX_CVtuZ9i.csv',sep=',')

test_path = pd.read_csv('/content/test_Y3wMUE5_7gLdaTN (1).csv',sep=',')

# Read Train File
train_df = pd.read_csv('/content/train_u6lujuX_CVtuZ9i.csv',sep=',')

#Explore first 5 rows
train_df.head()

#Read test file
test_df = pd.read_csv('/content/test_Y3wMUE5_7gLdaTN (1).csv',sep=',')

#Explore first 5 rows
test_df.head()

# Basic info about dataset
train_df.info()

# Stats summary
train_df.describe()

# Since we don't need ID column, so we drop it in both the datasets.
train_df.drop(labels='Loan_ID', axis=1, inplace=True)
test_df.drop(labels="Loan_ID", axis=1, inplace=True)

#Explore random 10 rows
train_df.sample(10)

##Count Missing Value
train_df.isnull().sum().sort_values(ascending=False)

# Checking unique variables and dtypes in Credit_History
print(f"Unique vaiables: {train_df['Credit_History'].unique()} \n\ndtype of Credit_History: {train_df['Credit_History'].dtype}")

# Convert the Credit_History column to the object datatype
train_df['Credit_History'] = train_df['Credit_History'].astype('object')
train_df['Credit_History'].dtype

# List of columns with missing values
null_cols = ['Credit_History', 'Self_Employed', 'LoanAmount', 'Dependents', 'Loan_Amount_Term', 'Gender', 'Married']

# Imputation loop
for col in null_cols:
    if train_df[col].dtype == 'object':
        # Impute categorical variables with mode
        mode_value = train_df[col].mode()[0]
        train_df[col].fillna(mode_value, inplace=True)
        print(f"Imputed {col} with mode: {mode_value}")
    else:
        # Impute numerical variables with mean for non-binary, and mode for binary
        mean_value = train_df[col].mean()
        train_df[col].fillna(mean_value, inplace=True)
        print(f"Imputed {col} with mean: {mean_value}")

# Count Null v
train_df.isnull().sum().sort_values(ascending=False)

# Visualize the distribution of the target variable
plt.figure(figsize=(6, 4))
sns.countplot(x='Loan_Status', data=train_df)
plt.title('Loan Approval Status Distribution')
plt.show()

# Lets distribute our datatype into numerical and categorical datatype

numerical = train_df.select_dtypes('number').columns.to_list()
categorical = train_df.select_dtypes('object').columns.to_list()

loan_num = train_df[numerical]
loan_cat = train_df[categorical]

# Visualizing Distplot on numerical columns
for i in loan_num:
    plt.figure(figsize=(8, 5))
    sns.histplot(train_df[i], bins=20, kde=True)
    plt.title(f'{i} Distribution')
    plt.show()

    plt.figure(figsize=(8, 5))
    sns.boxplot(x='Loan_Status', y=i, data=train_df, palette='Set3')
    plt.title(f'{i} Distribution by Loan Status')
    plt.show()

for i in categorical[:-1]: #excluding the last element since it is Loan_Status itself
    plt.figure(figsize=(8, 5))
    sns.countplot(x=col, hue='Loan_Status', data=train_df, palette='Set2')
    plt.title(f'{i} Distribution by Loan Status')
    plt.show()

#Mapping Categorical values

label_mapping = {'Male': 1, 'Female': 0,
'Yes': 1, 'No': 0,
'0': 0, '1': 1, '2': 2, '3+': 3 ,
'Graduate': 1, 'Not Graduate': 0,
'Urban': 1, 'Semiurban': 2,'Rural': 3,
'Y': 1, 'N': 0}

# Apply label encoding to categorical columns
train_df.replace(label_mapping, inplace=True)
test_df.replace(label_mapping, inplace=True)

train_df.info()
test_df.info()

# Creating a correlation between the training dataset
corr_matrix = train_df.corr()
corr_matrix

# Plotting Heatmap for better visualization
plt.figure(figsize=(12,8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
plt.title("Heatmap for Correlation Matrix")
plt.show()

# Split training data
y = train_df['Loan_Status']
x = train_df.drop('Loan_Status', axis=1)
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.3, random_state=0)

# Data Scaling
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)
x_train

# Model Training with GridSearchCV
param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000], 'penalty': ['l1', 'l2']}
LR = LogisticRegression(random_state=42)
grid_search = GridSearchCV(LR, param_grid, cv=5, scoring='accuracy')
grid_search.fit(x_train, y_train)

# Print the best parameters found by GridSearchCV
print("Best Parameters:", grid_search.best_params_)

# Model Prediction
y_pred = grid_search.predict(x_test)

# Model Evaluation
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f"\nAccuracy: {accuracy}")
print("\nConfusion Matrix:")
print(conf_matrix)
print("\nClassification Report:")
print(classification_rep)

Logistic_Regression=pd.DataFrame({'y_test':y_test,'prediction':y_pred})
Logistic_Regression.to_csv("Logistic Regression.csv")