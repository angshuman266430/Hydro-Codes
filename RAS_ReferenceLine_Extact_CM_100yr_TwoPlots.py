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
    return data

def plot_profile_time_series(data1, data2, names, data_type, output_folder, hdf_file_path1, hdf_file_path2):
    num_time_steps = data1.shape[0]
    invert_points = ["KCou_PS", "KCou_I10", "KCou_EPrienLkRd", "KCou_Hwy90", "KCou_LegionSt"]

    for time_step in range(num_time_steps):
        plt.figure(figsize=(10, 6), dpi=300)
        ax = plt.gca()  # Get current axis

        # Check if the current plot needs to be inverted
        if data_type == "Flow" and names[time_step] in invert_points:
            data_to_plot1 = data1[time_step, :] * -1
            data_to_plot2 = data2[time_step, :] * -1
        else:
            data_to_plot1 = data1[time_step, :]
            data_to_plot2 = data2[time_step, :]



        # Plot data for both HDF files
        plt.plot(data_to_plot1, label='100yr with project high tide')
        plt.plot(data_to_plot2, label='100yr without project high tide')

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

        # Add legend
        plt.legend()

        plt.tight_layout()

        file_name = f"{data_type}_{names[time_step]}_time_series_profile.png"
        output_file_path = os.path.join(output_folder, file_name)
        plt.savefig(output_file_path, bbox_inches='tight', facecolor=ax.figure.get_facecolor())
        plt.close()

def main(hdf_file_paths, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for data_type in ["Water Surface", "Flow"]:
        names = extract_names(hdf_file_paths[0], data_type)
        data1 = process_data(extract_time_series(hdf_file_paths[0], data_type), data_type)
        data2 = process_data(extract_time_series(hdf_file_paths[1], data_type), data_type)
        plot_profile_time_series(data1, data2, names, data_type, output_folder, hdf_file_paths[0], hdf_file_paths[1])

# Parameters
hdf_file_paths = [
    "S:\\For_Angshuman\\Greenbelt\\ClientMeeting_HDFs\\100yr\\Greenbelt_RAS.p10.hdf",
    "S:\\For_Angshuman\\Greenbelt\\ClientMeeting_HDFs\\100yr\\Greenbelt_RAS.p13.hdf"
]
output_folder = "output_plots_100yr_with_without_project_High_tide"

if __name__ == "__main__":
    main(hdf_file_paths, output_folder)
