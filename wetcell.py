import h5py
import numpy as np

# Open the HEC-RAS HDF file
with h5py.File("Zeta_Amite_20200114.p06.hdf", "r") as f:
    # Extract the water surface elevation dataset
    water_surface_elevation = f[
        "Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/2D Flow Areas/AmiteMaurepas/Water Surface"][
        ()]

    # Find the percentage of never wet cells
    total_cells = water_surface_elevation.size
    never_wet_cells = np.sum(water_surface_elevation <= 0)
    never_wet_cell_percent = (never_wet_cells / total_cells) * 100

    print("Percentage of never wet cells: {:.2f}%".format(never_wet_cell_percent))
