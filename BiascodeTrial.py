import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Read the CSV file
data = pd.read_csv("data.csv")

# Extract the storm name and data values
storm_name = data["storm_name"].unique()

# Create a dictionary to store the data
data_dict = {storm: data[data['storm_name'] == storm] for storm in storm_name}

# Plotting the data
markers = ['o', 'o', 'o', 'o', 's', 's', 's', 's', '^', '^', '^', '^', 'p', 'p', 'p', 'p']
marker_index = 0
observed_all = np.concatenate([data_dict[storm]["observed"].values for storm in storm_name])
modeled_all = np.concatenate([data_dict[storm]["modeled"].values for storm in storm_name])
# Calculate overall bias
overall_bias = np.mean(np.subtract(modeled_all, observed_all))
print("Overall bias:", overall_bias)

# Calculate overall RMSE
overall_rmse = np.sqrt(np.mean(np.square(np.subtract(modeled_all, observed_all))))
print("Overall RMSE:", overall_rmse)

# Calculate overall standard deviation
overall_std_dev = np.std(modeled_all)
print("Overall modeled standard deviation:", overall_std_dev)

for storm in storm_name:
    observed = data_dict[storm]["observed"].values
    modeled = data_dict[storm]["modeled"].values

    # Calculate bias
    bias = np.mean(np.subtract(modeled, observed))
    print("Bias for " + storm + ":", bias)

    # Calculate RMSE
    rmse = np.sqrt(np.mean(np.square(np.subtract(modeled, observed))))
    print("RMSE for " + storm + ":", rmse)

    # Calculate standard deviation of modeled data
    std_dev = np.std(modeled)
    print("Standard deviation of modeled data for " + storm + ":", std_dev)

    marker = markers[marker_index % len(markers)]
    marker_index += 1
    plt.scatter(modeled, observed, label=storm, marker=marker, edgecolors='black', s=22, linewidths=0.5)

# Add a 1 to 1 line and modeled standard deviation line
x_limit = 45
y_limit = 45

plt.plot([0, x_limit], [0, y_limit], '-r', label='1:1 line')
plt.plot([0, x_limit], [0-overall_std_dev, y_limit-overall_std_dev], '--k')
plt.plot([0, x_limit], [0+overall_std_dev, y_limit+overall_std_dev], '--k')
plt.xlim(0, x_limit)
plt.ylim(0, y_limit)
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.subplots_adjust(right=0.7)


# Perform linear regression for all storms combined
modeled_all = data["modeled"].values
observed_all = data["observed"].values
reg = LinearRegression().fit(modeled_all.reshape(-1, 1), observed_all)

# Calculate R2 value for all storms combined
r2 = r2_score(observed_all, reg.predict(modeled_all.reshape(-1, 1)))

# Get coefficients for all storms combined
a, b = reg.coef_[0], reg.intercept_

# Add dotted linear regression line to the plot
plt.plot(modeled_all, reg.predict(modeled_all.reshape(-1, 1)), ':b')
dotted_line, = plt.plot(modeled_all, reg.predict(modeled_all.reshape(-1, 1)), ':b', label='Linear Regression')

# Add linear regression equation and R2 value to the plot
plt.text(1.05*max(modeled_all), 0.05*max(observed_all), f'y = {a:.2f}x + ({b:.2f})\nR$^2$ = {r2:.2f}\nBias = {overall_bias:.2f}\nRMSE = {overall_rmse:.2f}',
         verticalalignment='bottom', horizontalalignment='right', fontsize=9)

# Add axis labels, title and legend
plt.xlabel('Modeled water surface elevation (NAVD88, ft)')
plt.ylabel('Observed water surface elevation (NAVD88, ft)')
plt.title('TCs numerical model uncertainty for Gage data')

# Add the standard deviation legend to the plot
plt.plot([], [], '--k', label='+/- 1 std')
plt.legend(bbox_to_anchor=(1,1), loc="upper left", prop={'size': 8})
plt.subplots_adjust(right=0.7)


# Set the x-axis and y-axis limits to start at 0
plt.xlim(0, None)
plt.ylim(0, None)

# Show the plot
plt.show()
