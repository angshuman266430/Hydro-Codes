import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data from Excel sheet
df = pd.read_excel('water_data_Bonnie.xlsx')

# Plot observed water level
plt.plot(df['Time_Observed'], df['Water_Level_Observed'], 'b-', label='Observed')

# Plot simulated water level
plt.plot(df['Time_Simulated'], df['Water_Level_Simulated'], 'r-', label='Simulated')

# Add legend and labels
plt.legend()
plt.xlabel('Date')
plt.ylabel('Water Surface Elevation (NAVD88, in ft)')

# Set the major x-axis ticks with 3 intervals
start, end = plt.xlim()
plt.xticks(np.linspace(start, end, 4))

# Show plot
plt.show()