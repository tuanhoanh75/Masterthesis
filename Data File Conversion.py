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

    # Export converted data files
    export_csv = df.to_csv(DIR + "/" + "csv/" + "export" + dir_list[i], sep=';', index=False, header=True)


    