# by Angshuman Saharia (asaharia@thewaterinstitute.org)
# 7/26/2023

import pandas as pd
import os
import numpy as np

def interpolate_rows(df):
    # Convert specified values to NaN
    df.replace([-99999, -100000, -328080.72, -328081], np.nan, inplace=True)

    for idx, row in df.iterrows():
        # Find the first non-NaN value in the row
        first_valid = row.first_valid_index()
        # Find the last non-NaN value in the row
        last_valid = row.last_valid_index()

        # If the first value in the row is NaN, replace it with the first non-NaN value
        if first_valid is not None:
            row.loc[:first_valid] = row[first_valid]

        # If the last value in the row is NaN, replace it with the last non-NaN value
        if last_valid is not None:
            row.loc[last_valid:] = row[last_valid]

        # Perform linear interpolation for the row
        df.loc[idx] = row.interpolate(method='linear')

    return df

# Define the path of the directory containing the CSV files
csv_dir_path = "S:\\For_Angshuman\\LWI_2024\\WL_BC\\WL_NC_to_CSV\\Processed\\replace-99999multiples"

# Define the path to save processed files
processed_path = "S:\\For_Angshuman\\LWI_2024\\WL_BC\\WL_NC_to_CSV\\Processed\\replace-99999multiples"

# Get the list of files in the directory
csv_files = os.listdir(csv_dir_path)

# Process each file in the directory
for csv_file in csv_files:
    # Only process CSV files
    if csv_file.endswith(".csv"):
        # Construct the paths
        csv_path = os.path.join(csv_dir_path, csv_file)
        processed_file_path = os.path.join(processed_path, csv_file)

        try:
            # Load the CSV file with no header
            df = pd.read_csv(csv_path, header=None)

            # Skip the first row and the first column
            df = df.iloc[1:, 1:]

            # Interpolate between valid values and replace invalid values
            df = interpolate_rows(df)

            # Delete the last column
            df = df.iloc[:, :-1]

            # Save the processed file
            df.to_csv(processed_file_path, index=False, header=False)
        except Exception as e:
            print(f"Processing of {csv_file} failed due to error: {e}")
