import pandas as pd
import os
import datetime as dt

# Get Files from directory
PATH = r"/Users/Tuan/Desktop/Output/Converted_files/csv"
file_list = os.listdir(PATH)

# Presets: Show maximum columns and in one row
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Read csv Data Files; e.g. Kartoffel and interpret decimal with dot instead comma
df_kart = pd.read_csv(PATH + "/" + file_list[1], delimiter=';', header=0,  decimal=',')

# Replace commas with dots, which is required to convert object (string) to float
print(df_kart.head(25))
print(df_kart.info())
