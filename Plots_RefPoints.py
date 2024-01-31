import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
import re


def extract_data(hdf_file_path, variable_name):
    data_path = f"Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/Reference Points/{variable_name}"
    with h5py.File(hdf_file_path, "r") as f:
        if data_path in f:
            data = f[data_path][()]
            return data.T  # Transpose the data
        else:
            raise KeyError(f"Data path '{data_path}' not found in the HDF file.")


def extract_names(hdf_file_path):
    names_path = "Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/Reference Points/Name"
    with h5py.File(hdf_file_path, "r") as f:
        if names_path in f:
            names = f[names_path][()]
            return names
        else:
            raise KeyError(f"Names path '{names_path}' not found in the HDF file.")


def clean_filename(filename):
    cleaned_filename = re.sub(r'[\/:*?"<>|]', '_', filename.decode('utf-8'))
    cleaned_filename = re.sub(r'_time_series_\d+|_Perimeter 1', '', cleaned_filename)
    return cleaned_filename


def get_time_label(hdf_file_path):
    if 'p01.hdf' in hdf_file_path:
        return "10 min"
    elif 'p02.hdf' in hdf_file_path:
        return "5 min"
    else:
        return "Unknown time"


def plot_and_save_data(hdf_file_paths, variable_name, output_folder):
    all_data = []
    for file_path in hdf_file_paths:
        data = extract_data(file_path, variable_name)
        all_data.append(data)

    names = extract_names(hdf_file_paths[0])  # Assuming the names are the same in both files

    for i, name in enumerate(names):
        plt.figure(figsize=(10, 6), dpi=300)

        for j, data in enumerate(all_data):
            time_label = get_time_label(hdf_file_paths[j])
            plt.plot(data[i], label=f"{clean_filename(name)} - {time_label}", linestyle='-', marker='o', markersize=3)

        cleaned_name = clean_filename(name)
        plt.title(f"{variable_name} - {cleaned_name}", fontsize=20)
        plt.xlabel("Time Step", fontsize=16)
        plt.ylabel(f"{variable_name} (ft/s)" if variable_name == "Velocity" else f"{variable_name} (ft)", fontsize=16)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.legend(fontsize=14)
        plt.tight_layout()

        output_file_name = f"{variable_name}_{cleaned_name}.png"
        output_file_path = os.path.join(output_folder, output_file_name)
        plt.savefig(output_file_path, dpi=300, bbox_inches='tight')


if __name__ == "__main__":
    hdf_file_paths = [
        "S:\\For_Angshuman\\LWI_Coastwide\\HDFs_01.30.2024\\10min_VS_5minComparisons - Copy\\LWI_Coastwide_TZ_RASV61.p01.hdf",
        "S:\\For_Angshuman\\LWI_Coastwide\\HDFs_01.30.2024\\10min_VS_5minComparisons - Copy\\LWI_Coastwide_TZ_RASV61.p02.hdf"
    ]
    variable_names = ["Water Surface", "Velocity"]
    output_folder = "Ref_Point_Plots"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for variable_name in variable_names:
        plot_and_save_data(hdf_file_paths, variable_name, output_folder)
