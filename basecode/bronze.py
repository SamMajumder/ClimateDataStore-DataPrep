import xarray as xr
from netCDF4 import Dataset
import numpy
import os
import pandas as pd


def files_to_ingest(inventory_table_source_file_column:pd.Series,
                    bronze_table_source_file_column:pd.Series,
                    download_folder):

    
    # STEP 1: Filter files in inventory that are NOT yet in bronze
    files_to_upload = inventory_table_source_file_column[
        ~inventory_table_source_file_column.isin(bronze_table_source_file_column)
    ].tolist()

    # STEP 2: Build full paths
    files_to_upload_paths = [os.path.join(download_folder, f) for f in files_to_upload]
    
    return files_to_upload_paths




def netcdf_bronze(files_to_upload_paths,
                  bronze_output_folder): 
    
     

    ### STEP 1 ### 
    # load bronze table from memory
    bronze_table_name = "bronze_table.parquet"
    bronze_table_path = os.path.join(bronze_output_folder,bronze_table_name)

    
    bronze_table = pd.read_parquet(bronze_table_path)
    print(f"[INFO] Existing bronze table is loaded to memory") 

    
    ### STEP 2 ###
    ## only open netcdf files which are new or have not been downloaded 
    ### in the past three months
    ## open the netcdf file from files_to_upload list

    ## defining an empty list to accumulate all new entries to the bronze table

    bronze_table_updates = []
    
    for file_path in files_to_upload_paths:
    
        filename = os.path.basename(file_path) 

        if filename in bronze_table["source_file"].values:
            print(f"[⏭️] Skipping {filename} — already processed.")
            continue

        print(f"[📥] Ingesting {filename}...")


        ds = xr.open_dataset(file_path,
                            decode_times=True,
                            engine="netcdf4") 
        

        ##### STEP 3
        ##### create a dataframe 
        df = ds.to_dataframe().reset_index() 

        ### STEP 4
        ### adding the attribute data to the dataframe 
        for key, value in ds.attrs.items():
            df[key] = value 

        ### STEP 5
        ### Adding the name of the source file
        df["source_file"] = os.path.basename(file_path)

        print(f"[✅] Added {filename} to bronze table.")

        ## appending new entries to the empty list
        bronze_table_updates.append(df)

    ### STEP 6
    ## save the entries to the bronze table
    
    if bronze_table_updates:
        new_updates = pd.concat(bronze_table_updates,ignore_index=True)
        bronze_table = pd.concat([bronze_table,new_updates],ignore_index=True)
        bronze_table.to_parquet(bronze_table_path, index=False)
        print(f"[✅] Bronze table updated with {len(new_updates)} new rows.")
    else:
        print("[✅] No new rows to append to bronze table.")
    











