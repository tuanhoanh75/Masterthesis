import pandas as pd
import os

# Get the list of all files and directories
path = "C://Users/Tuan/Desktop/Output/Converted files"
dir_list = os.listdir(path)

print("Files and directories in '", path, "' :")
print(len(dir_list))

"""
# Read raw data; Reminder: Header starts at row 3 (internally in python, cuz index start with 0)
df_kart = pd.read_csv('/Users/Tuan/Desktop/Output/Converted files/output_10361_1961-2020_Kart.csv',
                      delimiter=';', header=3)

df = df_kart[df_kart.Jahr != 'Jahr']
df.dropna(inplace=True)
df = df.reset_index(drop=True)

# Export new formatted data file
export_test = df.to_csv(r'/Users/Tuan/Desktop/Output/Converted files/export_10361_1961-2020_Kart.csv',
                        sep=';', index=False, header=True)
"""
