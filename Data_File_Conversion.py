import os
import re
import pandas as pd
from pathlib import Path

# Presets: Show max. cols and rows => Only relevant,if you want to work in console purely
pd.set_option('display.max_columns', None) 
pd.set_option('display.width', None)


# Get raw data files and from given path
DIR_folder = Path("/home/aegis/Dokumente/Masterarbeit/Data/")
list_rawdata = sorted(os.listdir(str(DIR_folder) + "/" + "csv"))

# Define regex pattern for substring extraction
pattern_vStation = re.compile(r'[A-Z0-9]{5}')
pattern_vPeriod = re.compile(r'\d{4}-\d{4}')
pattern_vMainCrop = re.compile(r'[A-Z]+[a-zA-Z]{,3}')


# Return a list of substrings from extraction of the filenames
list_station = [x for f in range(len(list_rawdata)) for x in re.findall(pattern_vStation, str(list_rawdata[f]))]
list_period = [x for f in range(len(list_rawdata)) for x in re.findall(pattern_vPeriod, str(list_rawdata[f]))]
list_crop =  [x for f in range(len(list_rawdata)) for x in re.findall(pattern_vMainCrop, str(list_rawdata[f]))]

# Remove lines containing the string 'OO' and then apply upper()
list_crop = list(filter(lambda a:a!='OO', list_crop))
list_crop = list(map(lambda x: x.upper(), list_crop))


# Process/ Convert all listed data files to an appropriate and more easily handle data format
for i, element in enumerate(list_rawdata):
    raw = pd.read_csv(str(DIR_folder) + "/" + "csv" + "/" + list_rawdata[0], 
                      delimiter=';', header=3, usecols=[0, 1, 6])

    df_files = raw[(raw["Jahr"] != "Jahr") & 
             (raw["Jahr"] != "Station:") & 
             (raw["Jahr"] != "Flexibilisierung:") & 
             (raw["Jahr"] != "Hauptfrucht:")]
    df_files.dropna(inplace=True)
    df_files.reset_index(drop=True, inplace=True)

    # Rename column caption via index
    df_files = df_files.rename(columns={df_files.columns[2]: 'BOF (%nFK)'})

    # Check the number of days of a year, if the year contains more than 365 day then remove the day 366
    indexNames = df_files[df_files["Tag"] == "366"].index
    df_files = df_files.drop(indexNames)

    # Quick dtype conversion, because per default all read data are of type object (or string)
    # Use int32/float32 instead of int64/float64 by default to save memory
    df_files['Jahr'] = df_files['Jahr'].astype('int32')
    df_files['Tag'] = df_files['Tag'].astype('int32')
    
    # Special treatment for BOF (%nFK) object which are hast comma separation instead dot 
    # -> relevant to conversion
    df_files['BOF (%nFK)'] = df_files['BOF (%nFK)'].apply(lambda x: x.replace(',', '.')).astype('float32')
    
    
    ## Combine cols "Jahr" and "Tag" and then convert it to datetime format, ... 
    ## ... whereby Day 1, 2019 can be translated to jan 1st 2019
    # a.) Create a new col 'Date'
    df_files['Date'] = df_files['Jahr'] * 1000 + df_files['Tag']
    
    # b.) Convert current date format YYYY-DD to actual date format YYYY-MM-DD
    df_files['Date']  = pd.to_datetime(df_files['Date'], format='%Y%j')              
    df_files.insert(0, 'Date', df_files.pop('Date'))           # insert column using insert(position,column_name, first_column) function
    
    # Omit superfluous columns
    df_files = df_files.drop(columns=["Jahr", "Tag"])
    
    # Resample data from daily to weekly level on mean basis
    df_weekly = df_files.resample('W', on='Date').mean()
    
    # Quick reset datetime index to column + re-arrange column order -> easier way to use pd.reindex()
    df_weekly['Date'] = df_weekly.index
    df_weekly = df_weekly.reset_index(drop=True)
    df_weekly.insert(0, 'Date', df_weekly.pop('Date'))
    
    
    
    # Export converted data files
    # export_csv = df_new.to_csv(DIR + '/' + 'csv/' + 'export_' + dir_list[i],
                              # sep=';', index=False, header=True, encoding='utf-8')
