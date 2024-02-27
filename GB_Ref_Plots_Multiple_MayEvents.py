import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta


def generate_dates(start_date, end_date, num_steps):
    start = datetime.strptime(start_date, "%d %b %Y %H:%M")
    end = datetime.strptime(end_date, "%d %b %Y %H:%M")
    delta = (end - start) / (num_steps - 1)
    return [start + i * delta for i in range(num_steps)]


def extract_names(hdf_file_path, data_type):
    names_path = "Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/Reference Lines/Name"
    with h5py.File(hdf_file_path, "r") as f:
        names_data = f[names_path][()]
        names = [name.split('|')[0] for name in names_data.astype(str)]
        return names


def extract_time_series(hdf_file_path, data_type):
    data_paths = {
        "Water Surface": "Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/Reference Lines/Water Surface",
        "Flow": "Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/Reference Lines/Flow"
    }
    with h5py.File(hdf_file_path, "r") as f:
        data_path = data_paths.get(data_type)
        if data_path in f:
            data = f[data_path][()]
            data = np.nan_to_num(data)
            return data
        else:
            raise KeyError(f"Data path '{data_path}' not found in the HDF file.")


def process_data(data, data_type):
    return data.T



def plot_profile_time_series(data, names, data_type, output_folder, dates):
    name_mapping = {
        "Kaouche_Coulee": "Kayouche Coulee",
        "CryingBrewery": "Crying Brewery",
        "GT": "Greinwich Terrace",
        "Near_LegionSt": "Near Legion St",
        "W_Sale_Rd": "West Sale Rd"
    }

    for idx, name in enumerate(names):
        if name in name_mapping:
            plt.figure(figsize=(10, 6), dpi=300)
            ax = plt.gca()

            data_to_plot = data[idx, :]

            plt.plot(dates, data_to_plot, label=f'{name_mapping[name]}', color='navy', linewidth=2)

            plot_title = f"{name_mapping[name]}"
            plt.title(plot_title, fontsize=20)
            plt.xlabel("Date", fontsize=16)
            plt.ylabel(f"{data_type.capitalize()} ({'ft³/s' if data_type == 'Flow' else 'ft'})", fontsize=16)

            plt.xticks(rotation=45)
            plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d %b %Y %H:%M'))

            # Increase font size of tick labels for both axes
            ax.tick_params(axis='x', labelsize=14)
            ax.tick_params(axis='y', labelsize=14)

            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('black')
            ax.spines['left'].set_linewidth(2)
            ax.spines['bottom'].set_color('black')
            ax.spines['bottom'].set_linewidth(2)

            ax.set_facecolor('white')
            ax.figure.set_facecolor('white')

            plt.tight_layout()

            file_name = f"{data_type}_{name.replace('_', '')}_time_series_profile.png"
            output_file_path = os.path.join(output_folder, file_name)
            plt.savefig(output_file_path, bbox_inches='tight', facecolor=ax.figure.get_facecolor())
            plt.close()



def main(hdf_file_base_path, output_base_folder, hdf_suffixes):
    start_date = "16 May 2021 00:00"
    end_date = "24 May 2021 12:00"


    for suffix in hdf_suffixes:
        hdf_file_path = f"{hdf_file_base_path}{suffix}.hdf"
        output_folder = f"{output_base_folder}_{suffix}"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for data_type in ["Water Surface", "Flow"]:
            names = extract_names(hdf_file_path, data_type)
            data = extract_time_series(hdf_file_path, data_type)
            data_processed = process_data(data, data_type)
            dates = generate_dates(start_date, end_date, data_processed.shape[1])
            plot_profile_time_series(data_processed, names, data_type, output_folder, dates)


if __name__ == "__main__":
    hdf_file_base_path = "S:\\For_Angshuman\\Greenbelt\\Task_ProfilePlots_2_27_2024\\Greenbelt_RAS.p"
    output_base_folder = "output_plots"
    hdf_suffixes = ["02", "15", "17"]

    main(hdf_file_base_path, output_base_folder, hdf_suffixes)
