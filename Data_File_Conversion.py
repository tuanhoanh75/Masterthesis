import os
import numpy as np
import pandas as pd
from pathlib import Path

# Get raw data files and from given path
DIR_folder = Path("/home/aegis/Dokumente/Masterarbeit/Data/")
list_rawdata = os.listdir(str(DIR_folder) + "/" + "csv")


# Step 1: Process/ Convert all listed data files to an appropriate and more easily handle data format
for i, element in enumerate(list_rawdata):
    raw = pd.read_csv(str(DIR_folder) + "/" + "csv" + "/" + list_rawdata[0], 
                      delimiter=';', header=3, decimal=',', usecols=[0, 1, 6])

    df = raw[(raw["Jahr"] != "Jahr") & 
             (raw["Jahr"] != "Station:") & 
             (raw["Jahr"] != "Flexibilisierung:") & 
             (raw["Jahr"] != "Hauptfrucht:")]
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Rename column caption via index
    df = df.rename(columns={df.columns[2]: 'BOF (%nFK)'})

    # Check the number of days of a year, if the year contains more than 365 day then remove the day 366
    indexNames = df[df["Tag"] == "366"].index
    df = df.drop(indexNames)
    

    #ToDo: Merge all a data prep files (Enrichment, Dat_prep) into one
    
    # Export converted data files
    # export_csv = df_new.to_csv(DIR + '/' + 'csv/' + 'export_' + dir_list[i],
                              # sep=';', index=False, header=True, encoding='utf-8')
