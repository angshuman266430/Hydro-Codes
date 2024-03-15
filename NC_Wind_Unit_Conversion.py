import xarray as xr
import numpy as np

# Path to the original NetCDF file
file_path = "S:\\For_Angshuman\\LWI_2024\Wind_Check\\ras_wind_laura_refTime_20200731_0000.nc"

# Load the NetCDF file
ds = xr.open_dataset(file_path)

# Conversion factor from m/s to ft/s (1 meter = 3.28084 feet)
conversion_factor = 3.28084

# Convert wind speed from m/s to ft/s
if 'wind_u' in ds.variables:
    ds['wind_u'] *= conversion_factor
    ds['wind_u'].attrs['units'] = 'ft/s'
if 'wind_v' in ds.variables:
    ds['wind_v'] *= conversion_factor
    ds['wind_v'].attrs['units'] = 'ft/s'

# Optionally, convert 'z' (elevation or depth) from meters to feet
if 'z' in ds.variables:
    ds['z'] *= conversion_factor
    ds['z'].attrs['units'] = 'ft'

# Specify the path for the output file
output_file_path = "S:\\For_Angshuman\\LWI_2024\Wind_Check\\ras_wind_laura_converted_ft_per_sec.nc"

# Save the modified dataset to a new NetCDF file
ds.to_netcdf(output_file_path)

# Close the dataset
ds.close()

print(f'Conversion completed. Output file saved at {output_file_path}')
