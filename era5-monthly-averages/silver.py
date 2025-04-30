import h3  
import pandas as pd
import os 


def files_to_tessellate(bronze_table_source_file_column:pd.Series,
                        silver_table_source_file_column:pd.Series):
    

    ### Identify files to tessellate 
    files_to_tessellate = bronze_table_source_file_column[
        ~bronze_table_source_file_column.isin(silver_table_source_file_column)
    ].tolist() 

    return files_to_tessellate 




def tessellate_table(bronze_table,
                     latitude,
                     longitude,
                     silver_output_folder,
                     resolution,
                     files_to_tessellate):
    
    ######
    ## STEP 1 ##########
    ### loading existing silver table from memory
    silver_table_name = "silver_table.parquet"
    silver_table_path = os.path.join(silver_output_folder,silver_table_name)

    silver_table = pd.read_parquet(silver_table_path)
    print(f"[INFO] Existing silver table is loaded to memory") 

    #####
    ### STEP 2 #####
    ### only tessellate observations from files that have not been tessellated 
    #### 

    ## defining an empty list to accumulate all new entries to the silver table

    silver_table_updates = []

    for file in files_to_tessellate:

        ### subset the bronze table based on source file name and pass that to the h3 indexing function
        observations_to_tessellate = bronze_table.loc[bronze_table["source_file"] == file].copy()

        ## if there are no files to tessellate then stop 
        if observations_to_tessellate.empty:
            print(f"[⚠️] No observations found for {file}. Skipping.")
            continue

        
        ##### 
        observations_to_tessellate['h3_cell_index'] = observations_to_tessellate.apply(lambda row:h3.latlng_to_cell(row[latitude],
                                                                                        row[longitude],
                                                                                        resolution),
                                                                                        axis=1)
    
        ### save to the table 
        silver_table_updates.append(observations_to_tessellate) 
        print(f"[✅] Tessellated {len(observations_to_tessellate)} rows from {file}.")


    ###### STEP 3: Save updates ##########
    ### now adding the updates to the silver table 
    if silver_table_updates:
        new_updates = pd.concat(silver_table_updates,ignore_index=True)
        silver_table = pd.concat([silver_table,new_updates],ignore_index=True)
        silver_table.to_parquet(silver_table_path,index=False)
        print(f"[✅] Silver table updated with {len(new_updates)} new rows.")
    else:
        print("[✅] No new rows to append to silver table.")

    
    



