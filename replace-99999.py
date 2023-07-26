import pandas as pd
import os
import numpy as np


def interpolate_columns(df):
    # Convert -99999 and -100000 to NaN
    df.replace([-99999, -100000], np.nan, inplace=True)

    for col in df.columns:
        # Identify rows directly connected to top and bottom values
        top_invalid_rows = df[df[col].isna()].index.tolist()
        bottom_invalid_rows = df[df[col].isna()][::-1].index.tolist()

        # Handle edge case where entire column is invalid
        if len(top_invalid_rows) == len(df):
            if col > 0 and col < df.columns[-1]:  # Not the first or last column
                df[col] = np.nanmean([df.iloc[:, col - 1], df.iloc[:, col + 1]], axis=0)
            continue

        # Interpolate invalid first row value and any directly connected values from neighboring columns
        for row in top_invalid_rows:
            if row <= top_invalid_rows[0] + 1 or pd.notna(df.iloc[row - 1, col]):
                if col > 0 and col < df.columns[-1]:  # Not the first or last column
                    if pd.notna(df.iloc[row, col - 1]) or pd.notna(df.iloc[row, col + 1]):
                        df.iloc[row, col] = np.nanmean([df.iloc[row, col - 1], df.iloc[row, col + 1]])

        # Interpolate invalid last row value and any directly connected values from neighboring columns
        for row in bottom_invalid_rows:
            if row >= bottom_invalid_rows[0] - 1 or pd.notna(df.iloc[row + 1, col]):
                if col > 0 and col < df.columns[-1]:  # Not the first or last column
                    if pd.notna(df.iloc[row, col - 1]) or pd.notna(df.iloc[row, col + 1]):
                        df.iloc[row, col] = np.nanmean([df.iloc[row, col - 1], df.iloc[row, col + 1]])

    # Interpolate remaining values
    df.interpolate(method='linear', inplace=True)

    return df


# Define the path of the directory containing the CSV files
csv_dir_path = "Z:/extract_wl_bc/trial/"

# Define the path to save processed files
processed_path = "Z:/extract_wl_bc/trial/Output"

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

            # Interpolate between valid values and replace invalid values
            df = interpolate_columns(df)

            # Save the processed file
            df.to_csv(processed_file_path, index=False, header=False)
        except Exception as e:
            print(f"Processing of {csv_file} failed due to error: {e}")
