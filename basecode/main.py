

from download import *





## This kicks off the process
def main(shapefile="C:/Users/samba/OneDrive/Documents/ClimateDataStore-DataPrep/basecode/vermont/FS_VCGI_OPENDATA_Boundary_BNDHASH_poly_vtbnd_SP_v1.shp",
         url = "https://cds.climate.copernicus.eu/api",
         key = "cf61da56-4246-4ccd-be3e-2ed16fa75647",
         dataset = "reanalysis-era5-land-monthly-means",
         product_type = ["monthly_averaged_reanalysis"],
         variable = ["2m_temperature", 
                    "total_precipitation"],
         year=["2024"],
         month=["02"],
         data_format="netcdf",
         output_folder="vermont_monthly"): 

    
    ## STEP 1 DOWNLOAD THE DATA ###
    download_data(shapefile=shapefile,
                url=url,
                key=key,
                dataset=dataset,
                product_type=product_type,
                variable=variable,
                year=year,
                month=month,
                data_format=data_format,
                output_folder=output_folder) 
    


if __name__ == "__main__":
    main()


