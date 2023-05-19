import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
import matplotlib.dates as mdates

# Custom date parser function
def custom_date_parser(x):
    if x.endswith("2400"):
        return pd.to_datetime(x.replace("2400", "0000")) + timedelta(days=1)
    else:
        return pd.to_datetime(x)

# Load the Excel file
xls = pd.ExcelFile('SensitivityData.xlsx')

# Get the names of all sheets in the file
sheet_names = xls.sheet_names

# Loop over each sheet
for sheet in sheet_names:
    # Read the data from the sheet
    data = pd.read_excel(xls, sheet_name=sheet, parse_dates=['Time and Date'], date_parser=custom_date_parser)

    # Create a new figure
    fig, ax1 = plt.subplots()

    # Plot the 'Elevation (ft)' data on the primary y-axis
    ax1.plot(data['Time and Date'], data['Stage HW Elevation (ft)'], label='Stage HW Elevation (ft)')
    ax1.plot(data['Time and Date'], data['Stage TW Elevation (ft)'], label='Stage TW Elevation (ft)')
    ax1.set_ylabel('Elevation (ft)')
    ax1.set_xlabel('Time and Date')

    # Create a secondary y-axis
    ax2 = ax1.twinx()

    # Plot the 'Flow (CFS)' data on the secondary y-axis
    ax2.plot(data['Time and Date'], data['Total Flow (CFS)'], label='Total Flow (CFS)', color='red')
    ax2.set_ylabel('Flow (CFS)')

    # Set the title of the plot to the name of the sheet
    plt.title(sheet)

    # Show the legend outside the plot area
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

    # Format the x-axis labels
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d%b%Y %H%M'))

    # Rotate the x-axis labels
    for label in ax1.get_xticklabels():
        label.set_rotation(45)

    # Save the plot
    plt.savefig(f'{sheet}.png', bbox_inches='tight')

    # Commented out plt.show()
    # plt.show()
