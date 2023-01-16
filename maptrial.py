import h5py
import numpy as np
import matplotlib.pyplot as plt

# Open the HEC-RAS HDF file for water depth
with h5py.File("Zeta_Amite_20200114.p06.hdf", "r") as f:
    # Extract the water surface elevation dataset
    water_depth = f[
        "Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/2D Flow Areas/AmiteMaurepas/Water Surface"][
        ()]
    water_depth = np.nan_to_num(water_depth)
    water_depth = water_depth.flatten() #flatten the water_depth array to 1-dimensional

# Open the HEC-RAS HDF file for cell coordinates
with h5py.File("Amite_20200114.g01.hdf", "r") as f:
    # Extract the cell center coordinates
    center_coordinates = f[
        "Geometry/2D Flow Areas/AmiteMaurepas/Cells Center Coordinate"][()]
    x_coordinates = center_coordinates[:,0]
    y_coordinates = center_coordinates[:,1]

# Check the length of the arrays
print(len(x_coordinates))
print(len(y_coordinates))

# Trim the arrays to the same length
min_len = min(len(x_coordinates), len(y_coordinates), len(water_depth))
x_coordinates = x_coordinates[:min_len]
y_coordinates = y_coordinates[:min_len]
water_depth = water_depth[:min_len]

# Create a scatter plot of all data
plt.scatter(x_coordinates, y_coordinates, c='gray', alpha=0.5)
plt.title("Plain Map of the Entire Area")
plt.xlabel("X Coordinates")
plt.ylabel("Y Coordinates")

# Filter the data to show only water depths less than or equal to 0
water_depth_nonpositive = water_depth <= 0
x_coordinates = x_coordinates[water_depth_nonpositive]
y_coordinates = y_coordinates[water_depth_nonpositive]
water_depth = water_depth[water_depth_nonpositive]

# Create a scatter plot of the filtered data with water depth as the color
plt.scatter(x_coordinates, y_coordinates, c=water_depth)
plt.colorbar(label='Water Surface (ft)')
plt.title("All never wet cells")
plt.xlabel("X Coordinates")
plt.ylabel("Y Coordinates")

# Show the plot
plt.show()
