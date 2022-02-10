#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 18:30:53 2022

@author: aegis
"""

import os
import re
import pandas as pd
#from matplotlib.pyplot import pyplot as plt

PATH = r'/home/aegis/Dokumente/Masterarbeit/Data/Converted_files/'
files_daily = sorted(os.listdir(PATH + 'Daily/'))
files_weekly = sorted(os.listdir(PATH + 'Weekly/'))

# Define regex pattern for substring extraction
#pattern_vNames = re.compile(r'[a-z0-9]+_\d{4}-\d{4}_\w{,4}', re.IGNORECASE)
pattern_vStation = re.compile(r'[A-Z0-9]{5}')
pattern_vPeriod = re.compile(r'\d{4}-\d{4}')
pattern_vMainCrop = re.compile(r'[A-Z]+[a-zA-Z]{,3}')

# Return a list of substrings from extraction of the filenames
list_station = [x for f in range(len(files_daily)) for x in re.findall(pattern_vStation, str(files_daily[f]))]
list_period = [x for f in range(len(files_daily)) for x in re.findall(pattern_vPeriod, str(files_daily[f]))]
list_crop =  [x for f in range(len(files_daily)) for x in re.findall(pattern_vMainCrop, str(files_daily[f]))]

list_crop = list(filter(lambda a:a!='OO', list_crop))
list_crop = list(map(lambda x: x.upper(), list_crop))


# Loop through all data sets and create for each of them meta data set
for i, element in enumerate(files_daily):                        
    file_read = pd.read_csv(PATH + 'Daily/' + files_daily[i],
                            delimiter=';', decimal=',', header=0)
    
    # Create hdf5 container and store data within it 
    storedata_daily = pd.HDFStore(PATH + '/hdf5_files/' + 'data_daily.hdf5')
    
    # Data
    storedata_daily.put('data_' + list_crop[i] + '_' + list_station[i], file_read)
    
    # Including meta data
    meta_daily = {'Station': list_station[i],
                  'Hauptfrucht': list_crop[i],
                  'Zwischenfrucht': 'keine',
                  'Flexbilisierung': 'keine',
                  'Betrachtungszeitraum': list_period[i]}
    
    # Getting attributes
    storedata_daily.get_storer('data_' + list_crop[i] + '_' + list_station[i]).attrs.meta_daily = meta_daily
    
    # Closing the storedata
    storedata_daily.close()



# getting data
with pd.HDFStore(PATH + '/hdf5_files/' + 'data_daily.hdf5') as storedata_daily:
    data_daily = storedata_daily['data_' + list_crop[23] + '_' + list_station[23]]
    metadata_daily = storedata_daily.get_storer('data_' + list_crop[23] + '_' + list_station[23]).attrs.meta_daily


# display data
print('\nDataFrame:\n', data_daily)

# display stored data or the name of the file where data are stored
#print('\nStored Data:\n', storedata_daily)
 
# display metadata
print('\nMetadata:\n', metadata_daily)

# Display short overview about data structures
print(data_daily.info())

# Convert the 'Date' column to datetime format and BOF (%nFK) to numeric
data_daily['Date'] = pd.to_datetime(data_daily['Date'])
data_daily["BOF (%nFK)"] = pd.to_numeric(data_daily["BOF (%nFK)"], downcast='float', errors='coerce')

# Quick Downsampling data tp weekly lvl
df_weekly = data_daily.resample("W", on="Date").mean()

"""
# Read daily and weekly lvl data
df_daily = pd.read_csv(PATH + 'Daily/' + files_daily[0], 
                            delimiter=';', decimal=',', header=0)
                                                  
df_weekly = pd.read_csv(PATH + 'Weekly/' + files_weekly[0],
                             delimiter=';', decimal=',', header=0)


# Store in hdf5 file format
storedata_daily = pd.HDFStore('college_data_daily.hdf5')
#storedata_weekly = pd.HDFStore('college_data_weekly.hdf5')

# data
storedata_daily.put('data_01', df_daily)
#storedata_weekly.put('data_02', df_weekly_kart)

# including meta data
metadata_daily = {'Station': 10361, 
                  'Hauptfrucht': 'Kartoffeln',
                  'Zwischenfrucht': 'keine', 
                  'Flexbilisierung': 'keine',
                  'Betrachtungszeitraum':"1961-2020"}
#metadata_weekly = {'scale': 0.1, 'offset': 15}

# getting attributes
storedata_daily.get_storer('data_01').attrs.metadata_daily = metadata_daily
#storedata_daily.get_storer('data_02').attrs.metadata = metadata_weekly

# closing the storedata
storedata_daily.close()
#storedata_weekly.close()


# getting data
with pd.HDFStore('college_data_daily.hdf5') as storedata_daily:
    data_daily = storedata_daily['data_01']
    metadata_daily = storedata_daily.get_storer('data_01').attrs.metadata_daily


# display data
print('\nDataFrame:\n', data_daily)

# display stored data or the name of the file where data are stored
print('\nStored Data:\n', storedata_daily)
 
# display metadata
print('\nMetadata:\n', metadata_daily)
"""





