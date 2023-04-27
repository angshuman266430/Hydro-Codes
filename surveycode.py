import os
import pandas as pd
import matplotlib.pyplot as plt

# Read the Excel file
excel_file = "Survey_tracking.xlsx"
xl = pd.read_excel(excel_file, sheet_name=None, engine='openpyxl')

# Create the output folder if it doesn't exist
output_folder = "Survey_tracking_plots"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through each sheet in the Excel file
for sheet_name, df in xl.items():
    # Skip if the sheet has less than 2 columns
    if df.shape[1] < 2:
        continue

    # Get the B and C column names
    col_b, col_c = df.columns[1], df.columns[2]

    # Convert the data in columns B and C to numeric format
    df[col_b] = pd.to_numeric(df[col_b], errors='coerce')
    df[col_c] = pd.to_numeric(df[col_c], errors='coerce')

    # Create a new figure for each sheet
    plt.figure()
    plt.plot(df[col_b], label=col_b)
    plt.plot(df[col_c], label=col_c)
    plt.xlabel("Serial number")
    plt.ylabel("Elevation (ft)")
    plt.title(f"Comparison of {col_b} and {col_c} in {sheet_name}")
    plt.legend()

    # Save the plot to the output folder
    plt.savefig(os.path.join(output_folder, f"{sheet_name}.png"))

# Show all the plots
#plt.show()
