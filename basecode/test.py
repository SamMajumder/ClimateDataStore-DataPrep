import cdsapi 

area = [45.01, -73.44, 42.72, -71.51]
url = "https://cds.climate.copernicus.eu/api"
key = "cf61da56-4246-4ccd-be3e-2ed16fa75647"
year = ["2024","2023"] 
month = ["01","02"]
variable = ["2m_temperature","total_precipitation"]


for y in year:
    for m in month:
        for v in variable:
        

            dataset = "reanalysis-era5-single-levels-monthly-means"
            request = {
                "product_type": ["monthly_averaged_reanalysis"],
                "variable": [v],
                "year": [y],
                "month": [m],
                "time": ["00:00"],
                "data_format": "netcdf",
                "download_format": "unarchived",
                "area": area
            }

            client = cdsapi.Client(url=url,key=key)
            client.retrieve(dataset, request).download() 

                



import xarray as xr 

xr.open_dataset("vermont_monthly/reanalysis-era5-single-levels-monthly-means_2023_01.nc")  




import pandas as pd 
df= pd.read_parquet("vermont_monthly_bronze/bronze_table.parquet")

df.columns
