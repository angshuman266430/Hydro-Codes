import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.spatial import distance

# Provided target coordinates directly as a list
target_coordinates_list = [
    (3619067.978156, 824449.247207), (3531663.507450, 856142.915773),
    (3618477.407408, 825039.812459), (3619067.978156, 824252.392122),
    (2962943.877114, 1006737.055235), (3134603.107869, 851812.103919),
    (3134209.394037, 852402.669172), (2963140.734030, 1006933.910320),
    (3618871.121240, 824449.247207), (2962747.020198, 1006737.055235)
]



# HDF file paths
hdf_file_paths = [
    "S:/For_Angshuman/LWI_Coastwide/Raster_Output/LWI_Coastwide_TZ_RASV61.p01.hdf",
    "S:/For_Angshuman/LWI_Coastwide/Raster_Output/LWI_Coastwide_TZ_RASV61.p02.hdf"
]


def find_nearest_cell_coordinate(hdf_file_path, target_coordinate):
    with h5py.File(hdf_file_path, 'r') as f:
        cell_centers_path = '/Geometry/2D Flow Areas/Perimeter 1/Cells Center Coordinate'
        cell_centers = f[cell_centers_path][:]
        if cell_centers.shape[0] == 2:
            cell_centers = cell_centers.T

        target_coordinate_2d = np.array([target_coordinate])
        distances = distance.cdist(target_coordinate_2d, cell_centers, 'euclidean')[0]
        nearest_cell_index = np.argmin(distances)

        water_surface_path = "Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/2D Flow Areas/Perimeter 1/Water Surface"
        water_surface_data = f[water_surface_path][:, nearest_cell_index]

        return water_surface_data


import matplotlib.pyplot as plt
import os


# Assuming other parts of the script remain unchanged, here's the updated plotting function
def plot_water_surface_time_series_for_coordinate(target_coordinate, output_folder):
    plt.figure(figsize=(10, 6))
    labels = ["10 min", "5 min"]  # Labels for the HDF files

    for i, hdf_file_path in enumerate(hdf_file_paths):
        water_surface_data = find_nearest_cell_coordinate(hdf_file_path, target_coordinate)
        plt.plot(water_surface_data, label=f'{labels[i]}')  # Use the labels list for naming

    plt.title(f"Water Surface Time Series at {target_coordinate}")
    plt.xlabel("Time Step")
    plt.ylabel("Water Surface Elevation")
    plt.legend()
    plt.savefig(os.path.join(output_folder, f"water_surface_{target_coordinate[0]}_{target_coordinate[1]}.png"))
    plt.close()


output_folder = "output_plots_Lowest10Coordinates"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)



# Loop over each target coordinate and plot data from both HDF files on the same plot
for target_coordinate in target_coordinates_list:
    plot_water_surface_time_series_for_coordinate(target_coordinate, output_folder)
