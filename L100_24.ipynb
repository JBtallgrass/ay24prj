# Import dependencies
import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns
from scipy import stats
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.linear_model import ElasticNet, Lasso, Ridge
from sklearn.model_selection import KFold, cross_val_score 
import statsmodels.api as sm

# read in mulitple csv files
csv_files = [
]
     

# Initialize an empty list to store DataFrames
dataframes = []

# Read the first CSV file to get the column headers
initial_df = pd.read_csv(csv_files[0])
initial_columns = initial_df.columns

# Loop through the list of files
for file in csv_files:
    # Read the current CSV file into a DataFrame, ensuring it matches the initial columns
    df = pd.read_csv(file, usecols=lambda column: column in initial_columns).reindex(columns=initial_columns)
       
    # Drop rows where all cells are blank
    df.dropna(how='all', inplace=True)
    
    # Append the DataFrame to the list
    dataframes.append(df)

# Concatenate all DataFrames in the list into a single DataFrame
m200_df = pd.concat(dataframes, ignore_index=True)

# Optionally, handle blanks in the compiled DataFrame as well

# Save the compiled DataFrame
m200_df.to_csv('data/m200_compiled_dataframe.csv', index=False)