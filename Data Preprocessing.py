import pandas as pd
import os

# Get the list of all files and directories
PATH = "C://Users/Tuan/Desktop/Output/Converted_files/"
dir_list = os.listdir(PATH)

# Read raw data; Reminder: Header starts at row 3 (internally in python, cuz index start with 0)
for f in range(len(dir_list)):
    file = PATH + dir_list[f]
    df_file = pd.read_csv(file, delimiter=';', header=3)

    df = df_file[df_file.Jahr != 'Jahr']
    df.dropna(inplace=True)
    df = df.reset_index(drop=True)

    export_file = df.to_csv(PATH + 'export_' + dir_list[f], sep=';', index=False, header=True)
