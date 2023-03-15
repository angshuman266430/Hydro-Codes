import h5py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


def extract_water_surface_time_series(hdf_file_path, geom_file_path, target_coordinates):
    with h5py.File(hdf_file_path, "r") as f:
        water_surface = f[
            "Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/2D Flow Areas/AmiteMaurepas/Water Surface"][
            ()]
        water_surface = np.nan_to_num(water_surface)

    with h5py.File(geom_file_path, "r") as f:
        center_coordinates = f["Geometry/2D Flow Areas/AmiteMaurepas/Cells Center Coordinate"][()]

    distance = np.sqrt(np.sum((center_coordinates - target_coordinates) ** 2, axis=1))
    nearest_cell_index = np.argmin(distance)
    water_surface_time_series = water_surface[:, nearest_cell_index]

    return water_surface_time_series


def plot_water_surface_time_series(water_surface_time_series, target_coordinates, output_folder):
    plt.plot(water_surface_time_series)
    plt.title("Water Surface Time Series")
    plt.xlabel("Time Step")
    plt.ylabel("Water Surface (NAVD88, ft)")

    file_name = f"water_surface_{target_coordinates[0]}_{target_coordinates[1]}.png"
    output_file_path = os.path.join(output_folder, file_name)
    plt.savefig(output_file_path)
    plt.clf()


def read_target_coordinates_from_csv(csv_file_path):
    coordinates_df = pd.read_csv(csv_file_path)
    target_coordinates = coordinates_df[['x', 'y']].to_numpy()
    return target_coordinates


def save_combined_water_surface_time_series_to_csv(data, output_folder):
    output_file_path = os.path.join(output_folder, "Timeseries.csv")
    data.to_csv(output_file_path, index_label="Time Step")


hdf_file_path = "Amite_20200114.p06.hdf"
geom_file_path = "Amite_20200114.g03.hdf"
csv_file_path = "coordinates.csv"
output_folder = "output_plots"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

target_coordinates_list = read_target_coordinates_from_csv(csv_file_path)
water_surface_data = []

for target_coordinates in target_coordinates_list:
    water_surface_time_series = extract_water_surface_time_series(hdf_file_path, geom_file_path, target_coordinates)
    plot_water_surface_time_series(water_surface_time_series, target_coordinates, output_folder)

    header = f"{target_coordinates[0]}, {target_coordinates[1]}"
    water_surface_data.append(pd.Series(water_surface_time_series, name=header))

combined_data = pd.concat(water_surface_data, axis=1)
save_combined_water_surface_time_series_to_csv(combined_data, output_folder)
