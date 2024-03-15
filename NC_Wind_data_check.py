import xarray as xr
import numpy as np

# Load the NetCDF file
ds = xr.open_dataset("S:\\For_Angshuman\\LWI_2024\\Wind_Check\\Laura_Wind_ft_per_sec\\ras_wind_laura_converted_ft_per_sec.nc")
#xr.open_dataset("S:\\For_Angshuman\\LWI_2024\Wind_Check\\ras_wind_laura_refTime_20200731_0000.nc")
#xr.open_dataset("S:\\For_Angshuman\\LWI_2024\\Wind_Check\\Laura_Wind_ft_per_sec\\ras_wind_laura_converted_ft_per_sec.nc")

# Assuming 'wind_u' and 'wind_v' are the variables of interest for the first time step
first_time_step_wind_u = ds['wind_u'].isel(time=0)
first_time_step_wind_v = ds['wind_v'].isel(time=0)

# Calculate and print the statistics for wind_u
print("Statistics for 'wind_u' at the first time step:")
print(f"Max Value (ft/s): {np.max(first_time_step_wind_u).values.item()}")
print(f"Min Value (ft/s): {np.min(first_time_step_wind_u).values.item()}")
print(f"Mean Value (ft/s): {np.mean(first_time_step_wind_u).values.item()}")

# Calculate and print the statistics for wind_v
print("\nStatistics for 'wind_v' at the first time step:")
print(f"Max Value (ft/s): {np.max(first_time_step_wind_v).values.item()}")
print(f"Min Value (ft/s): {np.min(first_time_step_wind_v).values.item()}")
print(f"Mean Value (ft/s): {np.mean(first_time_step_wind_v).values.item()}")

# Close the dataset
ds.close()
