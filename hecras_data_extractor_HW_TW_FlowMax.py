import h5py
import numpy as np
import os
import pandas as pd


def extract_data_from_hecras_hdf5(filename):
    results = []

    with h5py.File(filename, 'r') as f:
        base_path = "Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series"
        base_path_2D = f"{base_path}/2D Flow Areas/Model_Domain/2D Hyd Conn"
        base_path_bridges = f"{base_path}/2D Bridges"

        # Extract data function
        def extract_data(base_path, structure):
            structure_var_path = f"{base_path}/{structure}/Structure Variables"

            if structure_var_path in f:
                data = np.array(f[structure_var_path][:])

                # Modify structure name if it starts with "Model_Domain"
                if structure.startswith("Model_Domain "):
                    structure = structure.replace("Model_Domain ", "")

                # Check if the structure is NC or C type
                if "_NC" in structure:
                    max_values = data.max(axis=0)[[2, 3, 0]]  # Adjusted order here
                    keys = ["Max Headwater", "Max Tailwater", "Max Flow"]
                elif "_C" in structure:
                    max_values = data.max(axis=0)[[1, 2, 0]]  # Adjusted order here
                    keys = ["Max Headwater", "Max Tailwater", "Max Flow"]
                else:
                    return

                # Prepare result dictionary
                result = {"Structure": structure}
                for key, max_val in zip(keys, max_values):
                    result[key] = max_val

                results.append(result)

        # Extract data for 2D structures
        structures_2D = list(f[base_path_2D].keys())
        for structure in structures_2D:
            extract_data(base_path_2D, structure)

        # Extract data for all Bridge structures
        structures_bridges = list(f[base_path_bridges].keys())
        for structure in structures_bridges:
            extract_data(base_path_bridges, structure)

    # Sort results based on the structure name in the desired binary numbers way
    results.sort(key=lambda x: (int(''.join(filter(str.isdigit, x["Structure"]))), x["Structure"]))

    return results


def process_directory(dir_path):
    # List all files in the directory
    all_files = os.listdir(dir_path)

    # Filter out files that don't end with .hdf extension
    hdf_files = [f for f in all_files if f.endswith('.hdf')]

    # Process each HDF file and extract results
    all_results = {}
    for hdf_file in hdf_files:
        file_path = os.path.join(dir_path, hdf_file)
        results = extract_data_from_hecras_hdf5(file_path)
        all_results[hdf_file] = results

    return all_results


def write_to_excel(all_results, output_filename="hecras_results.xlsx"):
    # Define the mapping from PlanID to GLO RAS Events
    plan_id_mapping = {
        'p01': 'BaseModel',
        'p30': '050yr_Atlas_14',
        'p31': '050y_ Left_PD_Bivariate',
        'p32': '050yr_MostLikely_Bivariate',
        'p33': '050yr_Right_SD_Bivariate',
        'p10': '010yr_Atlas_14',
        'p11': '010yr_Left_PD_Bivariate',
        'p12': '010yr_MostLikely_Bivariate',
        'p13': '010yr_Right_SD_Bivariate',
        'p50': '100yr_Atlas_14',
        'p51': '100yr_Left_PD_Bivariate',
        'p52': '100yr_MostLikely_Bivariate',
        'p53': '100yr_Right_SD_Bivariate',
        'p70': '500yr_Atlas_14',
        'p71': '500yr_Left_PD_Bivariate',
        'p72': '500yr_MostLikely_Bivariate',
        'p73': '500yr_Right_SD_Bivariate',
        'p90': 'Harvey_AORC(no_wind)',
        'p91': 'Ike_AORC(no_wind)',
        'p92': 'Rita_AORC(no_wind)',
        'p93': 'Harvey_AORC(no_wind))_Epoch',
        'p94': 'Ike_AORC(no_wind)_Epoch',
        'p95': 'Rita_AORC(no_wind)_Epoch'
    }

    with pd.ExcelWriter(output_filename) as writer:
        for hdf_file, results in all_results.items():
            # Extract the PlanID from the filename
            plan_id = hdf_file.split('.')[-2]

            # Use the mapping to get the GLO RAS Event name for the sheet
            sheet_name = plan_id_mapping.get(plan_id, plan_id)  # Use PlanID as default if not found in mapping

            # Convert results to DataFrame
            df = pd.DataFrame(results).set_index("Structure").T
            df.to_excel(writer, sheet_name=sheet_name)

if __name__ == "__main__":
    dir_path = "Z:\\GLO\\Latest_Model"  # Provide the path to the directory containing your HDF files
    all_results = process_directory(dir_path)
    write_to_excel(all_results)
    print(f"Results written to hecras_results.xlsx")