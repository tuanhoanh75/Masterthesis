#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 15:47:09 2022

@author: aegis
"""

import os
import re
import numpy as np
import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt
# Preproccesing
from sklearn.preprocessing import MinMaxScaler
# Algorithms 
from tslearn.barycenters import dtw_barycenter_averaging
from tslearn.clustering import TimeSeriesKMeans
from sklearn.cluster import KMeans


# Presets
DIR = Path("/home/aegis/Dokumente/Masterarbeit/Data")
file_container = sorted(os.listdir(str(DIR) + "/" + "hdf5")) 
plt.rcParams['figure.figsize'] = (26,14)
plt.style.use('fivethirtyeight')


# Get all files from file container
data_file = pd.HDFStore(str(DIR) + "/" + "hdf5" + "/" + "data_daily.hdf5")
read_files = data_file.keys()                 # keys() list all records in the file container


# Read data sets from file container - get daily first
# Sample: Crop="Kartoffeln", Station=10361, Period=1961-2020
with pd.HDFStore(str(DIR) + "/" + "hdf5" + "/" + "data_daily.hdf5") as store_daily:
    data_KART = store_daily[read_files[0]]
    meta_KART = store_daily.get_storer(read_files[0]).attrs.meta_data
    
    
# Quick plot data; set col "Date" as index
data_KART = data_KART.set_index("Date")

daily_1961 = data_KART["BOF (%nFK)"]["1961-01-01":"1961-12-31"]
daily_2017 = data_KART["BOF (%nFK)"]["2017-01-01":"2017-12-31"]
daily_2018 = data_KART["BOF (%nFK)"]["2018-01-01":"2018-12-31"]
daily_2019 = data_KART["BOF (%nFK)"]["2019-01-01":"2019-12-31"]

# Init the subplot function using number of rows and columns
figure, axis = plt.subplots(2,2)

axis[0,0].plot(daily_1961, linewidth=1)
axis[0,0].set_title("Year 1961")


axis[0,1].plot(daily_1962, linewidth=1)
axis[0,1].set_title("Year 2017")

axis[1,0].plot(daily_2018, linewidth=1)
axis[1,0].set_title("Year 2018")

axis[1,1].plot(daily_2019, linewidth=1)
axis[1,1].set_title("Year 2019")




"""
axis[0,0].data_KART["BOF (%nFK)"]["1961-01-01":"1961-12-31"].plot(linewidth=1, fontsize=8)
axis[0,0].set_title("Year 1961")

axis[0,1].data_KART["BOF (%nFK)"]["1962-01-01":"1962-12-31"].plot(linewidth=1, fontsize=8)
axis[0,1].set_title("Year 1962")

axis[1,0].data_KART["BOF (%nFK)"]["2018-01-01":"2018-12-31"].plot(linewidth=1, fontsize=8)
axis[1,0].set_title("Year 2018")

axis[1,1].data_KART["BOF (%nFK)"]["2019-01-01":"2019-12-31"].plot(linewidth=1, fontsize=8)
axis[1,1].set_title("Year 2019")

#y_ticks = np.arange(0, 110, 10)
#plt.yticks(y_ticks)
daily_1961 = data_KART["BOF (%nFK)"]["1961-01-01":"1961-12-31"].plot(linewidth=1, 
                                                                   fontsize=14)
daily_1962 = data_KART["BOF (%nFK)"]["1962-01-01":"1962-12-31"].plot(linewidth=1, 
                                                                   fontsize=14)
daily_2018 = data_KART["BOF (%nFK)"]["2018-01-01":"2018-12-31"].plot(linewidth=1, 
                                                                   fontsize=14)
daily_2019 = data_KART["BOF (%nFK)"]["2019-01-01":"2019-12-31"].plot(linewidth=1, 
                                                                   fontsize=14)

ax_daily.set_ylabel("BOF (%nFK)")
"""


