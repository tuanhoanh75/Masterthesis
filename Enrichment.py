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
pattern_vStation = re.recompile(r'[a-z0-9]{5}', re.IGNORECASE)
pattern_vPeriod = re.recompile(r'd{4}-\d{4}', re.IGNORECASE)

pattern_vMainCrop = re.recompile(r'[a-z0-9]{5}', re.IGNORECASE)

# Return a list of substrings from extraction of the filenames
# list_substr = sorted([x for f in range(len(files_daily)) for x in re.findall(pattern_vNames, str(files_daily[f]))])

# Extract substrings from the filenames
station = []
period = []
crop =  []

# ToDo: Complete loop and writing hdf5 files

for i in range(len(files_daily)):
    tmp_station = re.findall(pattern_vStation, str(files_daily[i]))
    tmp_period = re.findall(pattern_vPeriod, str(files_daily[i]))
    tmp_vMainCrop = re.findall(pattern_vMainCrop, str(files_daily[i]))



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






