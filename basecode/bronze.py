import xarray as xr
from netCDF4 import Dataset
import numpy


path = "C:/Users/samba/OneDrive/Documents/ClimateDataStore-DataPrep/basecode/vermont_monthly/era5_2024_02.nc"
ds = xr.open_dataset(path,decode_times=True,engine="netcdf4") 

df = ds.to_dataframe().reset_index() 

### 
for key,value in ds.attrs.items():
    df[key] = value 









