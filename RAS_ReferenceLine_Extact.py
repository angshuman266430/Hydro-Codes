import h5py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def extract_names(hdf_file_path, data_type):
    names_path = "Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/Reference Lines/Name"
    with h5py.File(hdf_file_path, "r") as f:
        names_data = f[names_path][()]
        names = [name.split('|')[0] for name in names_data.astype(str)]
        return names

def extract_time_series(hdf_file_path, data_type):
    with h5py.File(hdf_file_path, "r") as f:
        data_paths = {
            "Water Surface": "Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/Reference Lines/Water Surface",
            "Flow": "Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/Reference Lines/Flow"
        }

        data_path = data_paths.get(data_type)
        if data_path in f:
            data = f[data_path][()]
            data = np.nan_to_num(data)
            return data
        else:
            raise KeyError(f"Data path '{data_path}' not found in the HDF file.")

def process_data(data, data_type):
    data = data.T
    if data_type == "Flow":
        for time_step in range(data.shape[0]):
            if np.mean(data[time_step, :] <= 0) >= 0.9:
                data[time_step, :] *= -1
    return data

def plot_profile_time_series(data, names, data_type, output_folder):
    num_time_steps = data.shape[0]

    for time_step in range(num_time_steps):
        plt.figure(figsize=(10, 6), dpi=300)
        ax = plt.gca()  # Get current axis

        # Plot data
        plt.plot(data[time_step, :])

        # Enhancing the plot for research paper quality with names
        plot_title = f"{data_type.capitalize()} - {names[time_step]} Time Series"
        plt.title(plot_title, fontsize=20)
        plt.xlabel("Time Step", fontsize=16)
        plt.ylabel(f"{data_type.capitalize()} ({'ft³/s' if data_type == 'Flow' else 'ft'})", fontsize=16)

        # Set tick label sizes
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)

        # Set spine colors and properties
        ax.spines['top'].set_visible(False)
        ax.spines['right']. set_visible(False)
        ax.spines['left'].set_color('black')
        ax.spines['left'].set_linewidth(2)
        ax.spines['bottom'].set_color('black')
        ax.spines['bottom'].set_linewidth(2)

        # Set background color
        ax.set_facecolor('white')
        ax.figure.set_facecolor('white')
        ax.figure.set_edgecolor('white')

        plt.tight_layout()

        file_name = f"{data_type}_{names[time_step]}_time_series_profile.png"
        output_file_path = os.path.join(output_folder, file_name)
        plt.savefig(output_file_path, bbox_inches='tight', facecolor=ax.figure.get_facecolor())
        plt.close()

def main(hdf_file_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    names = extract_names(hdf_file_path, "Water Surface")
    water_surface_data = extract_time_series(hdf_file_path, "Water Surface")
    water_surface_data = process_data(water_surface_data, "Water Surface")
    plot_profile_time_series(water_surface_data, names, "Water Surface", output_folder)

    flow_names = extract_names(hdf_file_path, "Flow")
    flow_data = extract_time_series(hdf_file_path, "Flow")
    flow_data = process_data(flow_data, "Flow")
    plot_profile_time_series(flow_data, flow_names, "Flow", output_folder)

# Parameters
hdf_file_path = "Z:\\Greenbelt\\Code_Test\\Greenbelt_RAS.p01.hdf"  # Replace with your HDF file path
output_folder = "output_plots"

if __name__ == "__main__":
    main(hdf_file_path, output_folder)