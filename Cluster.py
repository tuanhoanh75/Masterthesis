#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 15:47:09 2022

@author: aegis
"""

import os
import re
import pandas as pd
from pathlib import Path


# Presets
DIR = Path("/home/aegis/Dokumente/Masterarbeit/Data")
file_container = sorted(os.listdir(str(DIR) + "/" + "hdf5")) 


# Get all files from file container
data_daily_file = pd.HDFStore(str(DIR) + "/" + "hdf5" + "/" + "data_daily.hdf5")
read_files = data_daily_file.keys()                 # keys() list alls records in the file container

# Read data sets from file container - get daily first
with pd.HDFStore(str(DIR) + "/" + "hdf5" + "/" + "data_daily.hdf5") as data_daily:
    
