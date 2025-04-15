
import geopandas as gpd
import cdsapi
import os



def era5_monthly_cds_data_download(url:str,
                                   key:str,
                                   dataset:str,
                                   product_type:list,
                                   variable:list,
                                   year:list,
                                   month:list,
                                   data_format:str,
                                   area:list,
                                   output_folder:str): 

    
    ## create the folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder) 

    ## construct the file path
    filename = f"era5_{year[0]}_{month[0]}.nc"
    output_path = os.path.join(output_folder,filename)

    
    dataset = dataset
    request = {
        "product_type": product_type,
        "variable": variable,
    "year": year,
    "month": month,
    "time": ["00:00"],
    "data_format": data_format,
    "download_format": "unarchived",
    "area": area
    } 

    print(f"[INFO] Submitting request for dataset: {dataset}")
    print(f"[INFO] Request: {request}")
    #print(f"[INFO] Saving to: {output_path}")

    client = cdsapi.Client(url=url,key=key)
    client.retrieve(dataset, request).download(target=output_path)



    #print(f"[INFO] Download complete: {output_path}")




def download_data(shapefile:str,
                  url:str,key:str,
                  dataset:str,product_type:list,
                  variable:list,year:list,
                  month:list,data_format:str,
                  output_folder:str): 

    #### in the future we will have an if else statement based on data products
    ## and which download functions to activate 

    ### Step 1 ### read the the shapefile
    gdf = gpd.read_file(shapefile) 

    ### Step 2 ### convert the CRS to EPSG 
    ### if the crs is not 4326 please convert it to 4326
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326") 

    ### STEP 3 ######
    ### extract the ROI ### 
    ###### 

    west, south, east, north = gdf.total_bounds

    ############
    ### Orient the ROI to how CDS expects it
    ######### 

    area = [north, west, south, east]


    #### Step 4 ### download data ####  
    era5_monthly_cds_data_download(url,key,dataset,
                                   product_type,variable,
                                   year,month,data_format,
                                   area,output_folder)
    





    