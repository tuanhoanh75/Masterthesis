import os
import pandas as pd

# Get Files and directories from given path
DIR = "/Users/Tuan/Desktop/Output/Converted_files"
dir_list = os.listdir(DIR)

# Process/ Convert all listed data files to an appropriate and more easily handle data format
for i in range(1, len(dir_list)):
    file = pd.read_csv(DIR + "/" + dir_list[i], delimiter=';', header=3)
    
    df = file[file["Jahr"] != "Jahr"]
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    # Rename column caption via index
    mapping = {df.columns[2]: 'PET (mm)',
               df.columns[3]: 'AET (mm)',
               df.columns[4]: 'SNKk (mm)',
               df.columns[5]: 'PERC (mm)',
               df.columns[6]: 'BOF (%nFK)',
               df.columns[7]: 'BOF (Vol%)',
               df.columns[8]: 'SWI (mm)',
               df.columns[9]: 'ZG (cm)'}
    
    df_new = df.rename(columns=mapping)
    
    # Export converted data files
    export_csv = df_new.to_csv(DIR + "/" + "csv/" + "export_" + dir_list[i], sep=';', index=False, header=True)
