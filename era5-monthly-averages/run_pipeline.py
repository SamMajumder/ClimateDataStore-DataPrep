
import os
import glob
from download import *
from bronze import *
from silver import *

## This kicks off the process
def run_pipeline(shapefile,
                 url,key,
                 dataset,
                 product_type,
                 variable,
                 year,
                 month,
                 data_format,
                 download_folder,
                 bronze_output_folder,
                 silver_output_folder): 

    ## STEP 0 ## check to see if download folder, bronze output and silver output folder all exists
    ## if they don't then create it ###
    
    
    ## create the folder to store downloaded files if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)   

    ## create the folder to store the bronze table if it doesn't exist 
    if not os.path.exists(bronze_output_folder):
        os.makedirs(bronze_output_folder) 

    ### create the folder to store the silver table if it doesn't exist
    if not os.path.exists(silver_output_folder):
        os.makedirs(silver_output_folder)
    
    
    
    ### STEP 1 CHECK IF THERE IS AN INVENTORY TABLE
     ## check to see if there is an inventory table
    ## if there is then compare current request to the filenames in the inventory table
    ## if no table is present create an empty one ## it will be a parquet table containing filenames
    ## skip the files which are already in the dataframe
    

    ## filename of the inventory table
    inventory_table_name = "inventory_table.parquet"
    ## path to save inventory table and downloaded files 
    inventory_table_path = os.path.join(download_folder,inventory_table_name)
    

    #### only create the table if doesn't exist 
    if not os.path.exists(inventory_table_path):
        ### create an empty dataframe 
        inventory_table = pd.DataFrame({"filename":[],"download_date":[]}) 
        ### save it in the output folder 
        inventory_table.to_parquet(inventory_table_path,index=False)
        print(f"[INFO] Inventory table created at: {inventory_table_path}") 
    else:
        print(f"[INFO] Inventory table already exists in the download folder")
        


    
    ## STEP 2 DOWNLOAD THE DATA and update inventory table###
    ## only download files which are not in the inventory table or
    ## have not been downloaded in the last 3 months of the present date
    ## skip ones which are
    download_and_update_inventory(shapefile=shapefile,
                                  url=url,
                                  key=key,
                                  dataset=dataset,
                                  product_type=product_type,
                                  variable=variable,
                                  year=year,
                                  month=month,
                                  data_format=data_format,
                                  download_folder=download_folder,
                                  inventory_table_name=inventory_table_name)  
    
   
    
   
    
    
    ### STEP 3 CREATE BRONZE TABLES AND SAVE ### 
    ## Ingest data from the netccdf files 
    ## 
         
    bronze_table_name = "bronze_table.parquet"
    bronze_table_path = os.path.join(bronze_output_folder,bronze_table_name)
    
    if os.path.exists(bronze_table_path):
       
       ## read the bronze table
       bronze_table = pd.read_parquet(bronze_table_path)
       

    
    else:
        bronze_table = pd.DataFrame(columns=["source_file"])
        bronze_table.to_parquet(bronze_table_path,index=False)
        print(f"[INFO] Bronze table created")

    
    ## STEP 4 Grabbing the file paths to ingest into the bronze table
    ## read the inventory table
    inventory_table = pd.read_parquet(inventory_table_path)
    files_to_upload_paths = files_to_ingest(inventory_table_source_file_column=inventory_table["filename"],
                                               bronze_table_source_file_column=bronze_table["source_file"],
                                               download_folder=download_folder) 

    netcdf_bronze(files_to_upload_paths=files_to_upload_paths,
                  bronze_output_folder=bronze_output_folder)
    
    
    ### STEP 5 CREATE SILVER TABLES AND SAVE ###
    ##  create silver table if it doesn't exist 
    ##  if it does then tessellate the latitude and longitude 

    silver_table_name = "silver_table.parquet"
    silver_table_path = os.path.join(silver_output_folder,silver_table_name)

    if os.path.exists(silver_table_path):

        ## read existing silver table
        silver_table = pd.read_parquet(silver_table_path)

    else:
        silver_table = pd.DataFrame(columns=["source_file"])
        silver_table.to_parquet(silver_table_path,index=False)
        print(f"[INFO] Silver table created")
    
    
    
    
    ### STEP 6 #########
    ## Isolating files to tessellate
    files_to_tessellate_list = files_to_tessellate(bronze_table_source_file_column=bronze_table["source_file"],
                                                   silver_table_source_file_column=silver_table["source_file"])
    
    
    
    ### STEP 7 #####
    #### H3 indexing ### 
    tessellate_table(bronze_table=bronze_table, 
                     latitude="latitude", 
                     longitude="longitude", 
                     silver_output_folder=silver_output_folder,
                     resolution= 6, 
                     files_to_tessellate=files_to_tessellate_list)

    






