import pandas as pd
import os

# Get Files from directory
PATH = r"/Users/Tuan/Desktop/Output/Converted_files/csv"
file_list = os.listdir(PATH)

# Read csv Data Files; e.g. Kartoffel
df_kart = pd.read_csv(PATH + "/" + file_list[1], delimiter=';', header=0)
print(df_kart.shape)
