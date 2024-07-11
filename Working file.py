# %%
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


# %%
def process_folder(folder_path):
    # Get all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in {folder_path}")
        return None

    # Initialize an empty list to store DataFrames
    dataframes = []

    # Read the first CSV file to get the column headers
    initial_df = pd.read_csv(os.path.join(folder_path, csv_files[0]))
    correct_columns = initial_df.columns

    # Process the first file
    dataframes.append(initial_df)
    print(f"Read {csv_files[0]} successfully with {len(initial_df)} rows.")

    # Loop through the remaining files
    for file in csv_files[1:]:
        try:
            # Read the current CSV file into a DataFrame
            df = pd.read_csv(os.path.join(folder_path, file))
            
            # Check if the number of columns matches
            if len(df.columns) != len(correct_columns):
                print(f"Warning: {file} has {len(df.columns)} columns instead of {len(correct_columns)}.")
                print(f"Columns in {file}: {df.columns.tolist()}")
                print(f"Expected columns: {correct_columns.tolist()}")
                continue  # Skip this file and move to the next one
            
            # Rename columns to match the correct columns
            df.columns = correct_columns
            
            print(f"Read {file} successfully with {len(df)} rows.")
            
            # Drop rows where all cells are blank
            df.dropna(how='all', inplace=True)
            
            # Append the DataFrame to the list
            dataframes.append(df)
            
        except Exception as e:
            print(f"Failed to read {file}: {e}")

    # Check if there are any DataFrames to concatenate
    if dataframes:
        # Concatenate all DataFrames in the list into a single DataFrame
        folder_df = pd.concat(dataframes, ignore_index=True)
        
        print(f"Columns in the concatenated DataFrame: {folder_df.columns.tolist()}")
        
        # Check if 'learner_id' column exists
        if 'learner_id' not in folder_df.columns:
            print("Error: 'learner_id' column not found in the DataFrame.")
            print("Available columns:", folder_df.columns.tolist())
            return None
        
        # Process the learner_id column
        folder_df['team'] = pd.to_numeric(folder_df['learner_id'].str[:2], errors='coerce').astype('Int64')
        folder_df['section'] = folder_df['learner_id'].str[-1]
        
        # Check if 'last_name' and 'first_name' columns exist
        if 'last_name' in folder_df.columns and 'first_name' in folder_df.columns:
            # Create a base for the unique identifier
            folder_df['base_id'] = (folder_df['last_name'].str[0].fillna('') + 
                                    folder_df['first_name'].str[0].fillna('') + 
                                    folder_df['learner_id'].fillna(''))
        else:
            print("Warning: 'last_name' or 'first_name' columns not found. Using only 'learner_id' for base_id.")
            folder_df['base_id'] = folder_df['learner_id'].fillna('')
        
        # Function to create a truly unique identifier
        def create_unique_id(group):
            if len(group) == 1:
                return group['base_id']
            else:
                return group['base_id'] + '_' + (group.groupby('base_id').cumcount() + 1).astype(str)
        
        # Apply the function to create unique identifiers
        folder_df['unique_id'] = folder_df.groupby('base_id', group_keys=False).apply(create_unique_id)
        
        # Reorder columns to move unique_id to the leftmost position
        columns = folder_df.columns.tolist()
        columns.remove('unique_id')
        columns = ['unique_id'] + columns
        folder_df = folder_df[columns]
        
        return folder_df
    else:
        print(f"No dataframes to concatenate in {folder_path}.")
        return None

# %%
# Main script
data_root = 'data'  # Adjust this to your data root directory
output_dir = 'cleaned_data'  # Directory to save output files

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Expected folder names
expected_folders = [
    'C100', 'C200', 'C300', 'C400', 'C500', 
    'F100', 'S100', 'H100', 'H400', 'L100', 'L400', 
    'M000', 'M100', 'M200', 'M300', 'M400'
]

# Get all subdirectories in the data root
data_folders = [f.path for f in os.scandir(data_root) if f.is_dir()]

print(f"Total folders found: {len(data_folders)}")
print("Folders to be processed:")
for folder in data_folders:
    print(f"- {folder}")

# Process each folder
processed_folders = 0
processed_folder_names = []

for folder in data_folders:
    folder_name = os.path.basename(folder)
    if folder_name not in expected_folders:
        print(f"\nSkipping unexpected folder: {folder}")
        continue

    print(f"\nProcessing folder: {folder}")
    result_df = process_folder(folder)
    
    if result_df is not None:
        # Save the compiled DataFrame
        output_file = os.path.join(output_dir, f'{folder_name}_compiled_dataframe.csv')
        result_df.to_csv(output_file, index=False)
        print(f"Data compiled and saved successfully to {output_file}")
        print(f"Total rows in compiled dataframe: {len(result_df)}")
        
        # Print summary statistics
        print("\nSummary of rows per section:")
        print(result_df['section'].value_counts().sort_index())
        
        # Display the first few rows to verify the new column order
        print("\nSample data with reordered columns:")
        print(result_df.head(10))

        processed_folders += 1
        processed_folder_names.append(folder_name)
    else:
        print(f"No data processed for {folder}")

print(f"\nTotal folders processed: {processed_folders}")
print(f"Expected folders: {len(expected_folders)}")
print(f"Missing folders: {len(expected_folders) - processed_folders}")

print("\nProcessed folders:")
for folder in processed_folder_names:
    print(f"- {folder}")

print("\nMissing folders:")
for folder in expected_folders:
    if folder not in processed_folder_names:
        print(f"- {folder}")

print("\nAll available folders processed.")

# Check the contents of the cleaned_data folder
print("\nContents of the cleaned_data folder:")
for file in os.listdir(output_dir):
    print(f"- {file}")


