import os
import csv
import pandas as pd

def save_as_csv(file_name, object, headers):
    file_exists = os.path.isfile(file_name)
    with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow(object.to_csv_row())

def read_from_csv(csv_file):

 try:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Check if the DataFrame is empty
    if df.empty:
        print(f"The CSV file '{csv_file}' is empty.")
    else:
        # Extract the first row
        first_row = df.iloc[0]
        data=[]
        # Add values to list
        data.append(first_row['Commits'])
        data.append(first_row['Additions'])
        data.append(first_row['Deletions'])
        data.append(first_row['Changed_Files'])
        return data

 except FileNotFoundError:
    print(f"The CSV file '{csv_file}' does not exist.")

 except pd.errors.EmptyDataError:
    print(f"The CSV file '{csv_file}' is empty.")

 except Exception as e:
    print(f"An error occurred: {e}")
 
