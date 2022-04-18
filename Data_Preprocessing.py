import os 
#import re
import pandas as pd
#import pathlib as Path

"""
# Define regex pattern for substring extraction
pattern_vStation = re.compile(r'[A-Z0-9]{5}')
pattern_vPeriod = re.compile(r'\d{4}-\d{4}')
pattern_vMainCrop = re.compile(r'[A-Z]+[a-zA-Z]{,3}')
"""

DIR_PATH = r"C:/Users/Tuan/Masterarbeit/Data/raw-data/"
CONV_PATH = r"C:/Users/Tuan/Masterarbeit/Data/conv_data/"

list_files = sorted(os.listdir(DIR_PATH))

for i, elem in enumerate(list_files):
    raw_files = pd.read_csv(DIR_PATH + list_files[i], sep="\s+", header=3, usecols=[0,1,6], encoding='unicode_escape')

    df_file = raw_files[(raw_files["Jahr"] != "Jahr") & 
                        (raw_files["Jahr"] != "Station:") &
                        (raw_files["Jahr"] != "Flexibilisierung:") & 
                        (raw_files["Jahr"] != "Hauptfrucht:") & 
                        (raw_files["Jahr"] != "mm")]
    
    
    df_file.dropna(inplace=True)
    df_file.reset_index(drop=True, inplace=True)
    
    # Rename columns caption via index
    df_file = df_file.rename(columns={df_file.columns[2]: "BOF (%nFK)"})
    
    # Check the number of days of a year, if the year contains more than 365 day then remove the day 366
    
    indexNames = df_file[df_file["Tag"] == "366"].index
    df_file = df_file.drop(indexNames)
    
    # Quick dtype conversion, because per default all read data are of type object (or string)
    # Use int32/float32 instead of int64/float64 by default to save memory
    df_file['Jahr'] = df_file['Jahr'].astype('int32')
    df_file['Tag'] = df_file['Tag'].astype('int32')
    
    # Special treatment for the col "BOF (%nFK)" which objects are comma separation instead dot 
    # => relevant for conversion
    df_file['BOF (%nFK)'] = df_file['BOF (%nFK)'].apply(lambda x: x.replace(',', '.')).astype('float32')
    
    ## Combine cols "Jahr" and "Tag" and then convert it to datetime format, ... 
    ## ... whereby Day 1, 2019 can be translated to jan 1st 2019
    # a.) Create a new col 'Date'
    df_file['Date'] = df_file['Jahr'] * 1000 + df_file['Tag']
    
    # b.) Convert current date format YYYY-DD to actual date format YYYY-MM-DD
    df_file['Date']  = pd.to_datetime(df_file['Date'], format='%Y%j')
    # insert column using insert(position, column_name, first_column) function              
    df_file.insert(0, 'Date', df_file.pop('Date'))
    
    # Omit superfluous columns
    df_file = df_file.drop(columns=["Jahr", "Tag"])
    
    # export each converted data files, but without meta data
    export_csv = df_file.to_csv(CONV_PATH + list_files[i] + ".csv", sep=";", index=False, header=True, encoding="utf-8")
    