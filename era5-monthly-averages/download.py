
import geopandas as gpd
import cdsapi
import os
import pandas as pd
from datetime import datetime, timedelta



def era5_monthly_cds_data_download(url:str,
                                   key:str,
                                   dataset:str,
                                   product_type:list,
                                   variable:list,
                                   year:list,
                                   month:list,
                                   data_format:str,
                                   area:list,
                                   download_folder:str,
                                   inventory_table_name:str): 

    
    v_str = variable[0]
    y_str = year[0]
    m_str = str(month[0]).zfill(2)
    
    ## construct the file path
    filename = f"{dataset}_{v_str}_{y_str}_{m_str}.nc"
    output_path = os.path.join(download_folder,filename)

    
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



    print(f"[INFO] Download complete: {output_path}") 

    ### Step 5 ### load the existing inventory table 
    inventory_table_path = os.path.join(download_folder,inventory_table_name)
    inventory_table = pd.read_parquet(inventory_table_path) 

    ## Step 5 ## update the table row by row 
    new_row = {
        "filename": filename,
        "download_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    } 
    ## converting it to a dataframe row 
    new_row = pd.DataFrame([new_row])

    ## Step 6 ## add this to the existing dataframe 
    inventory_table = pd.concat([inventory_table,new_row],
                                ignore_index=True) 
    
    ### Step 7 ## save the updated file ###
    inventory_table.to_parquet(inventory_table_path,index=False)
    print(f"[INFO] inventory table updated")






def download_and_update_inventory(shapefile:str,
                                  url:str,key:str,
                                  dataset:str,product_type:list,
                                  variable:list,year:list,
                                  month:list,data_format:str,
                                  download_folder:str,
                                  inventory_table_name:str): 

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
    ## only download files which are not in the inventory table or
    ## have not been downloaded in the last 3 months of the present date
    ## skip ones which are
    
    # Load inventory table into DataFrame
    
    inventory_table_path = os.path.join(download_folder, inventory_table_name)

    inventory_df = pd.read_parquet(inventory_table_path)
    
    inventory_df["download_date"] = pd.to_datetime(inventory_df["download_date"])
    
    cutoff_date = datetime.now() - timedelta(days=90)


    for y in year:
        for m in month:
            for v in variable:
                filename = f"{dataset}_{v}_{y}_{str(m).zfill(2)}.nc"

                ## Look up the row in the inventory table where the filename matches, 
                # and grab the download timestamp from that row
                if filename in inventory_df["filename"].values:
                    last_downloaded = inventory_df.loc[
                    inventory_df["filename"] == filename, "download_date"
                    ].values[0] 

                    if pd.to_datetime(last_downloaded) > cutoff_date:
                        print(f"[⏭️] Skipping {filename} — downloaded within last 3 months.")
                        continue
                    else:
                        print(f"[♻️] Re-downloading {filename} — older than 3 months.")



                era5_monthly_cds_data_download(url,key,dataset,
                                           product_type,
                                           variable=[v],
                                           year=[y],
                                           month=[m],
                                           data_format=data_format,
                                           area=area,
                                           download_folder=download_folder,
                                           inventory_table_name=inventory_table_name)


    

    
    





    