#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 15:47:09 2022

@author: aegis
"""

import os
import math
import numpy as np
import pandas as pd
from pathlib import Path
import datetime as dt
from matplotlib import pyplot as plt
#Preprocessig
from sklearn.preprocessing import MinMaxScaler
# Algorithms 
from tslearn.barycenters import dtw_barycenter_averaging
from tslearn.clustering import TimeSeriesKMeans
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA


# Presets
DIR = Path("/home/aegis/Dokumente/Masterarbeit/Masterthesis/Data")
file_container = sorted(os.listdir(str(DIR) + "/" + "hdf5")) 
plt.rcParams['figure.figsize'] = (26,14)
plt.style.use('fivethirtyeight')
y_ticks = np.arange(0,101,10)


# Get all files from file container for daily data set
daily_file = pd.HDFStore(str(DIR) + "/" + "hdf5" + "/" + "data_daily.hdf5")
daily_files = daily_file.keys()                 # keys() list all records in the file container

# Get all files from file container for weekly data set
#weekly_file = pd.HDFStore(str(DIR) + "/" + "hdf5" + "/" + "data_weekly.hdf5")
#weekly_files = weekly_file.keys()  


# Read data sets from file container - get daily first
# Sample: Crop="Kartoffeln", Station=10361, Period=1961-2020
with pd.HDFStore(str(DIR) + "/" + "hdf5" + "/" + "data_daily.hdf5") as store_daily:
    
    tmpSeries = []
    mySeries_daily = []
    
    data_KART = store_daily[daily_files[0]]
    meta_KART_daily = store_daily.get_storer(daily_files[0]).attrs.meta_data
    data_KART['Date'] = data_KART['Date'].dt.strftime('%Y-%m-%d')

    data_KART.set_index('Date', inplace=True)
    data_KART.sort_index(inplace=True)
    
    # Partition dataframe data_KART by years
    #agg = data_KART.groupby(pd.DatetimeIndex(Samuel Kimdata_KART.index).year)
    for y in data_KART.groupby(pd.DatetimeIndex(data_KART.index).year):
        tmpSeries.append(y)
    
    # Get rid of the tuple     
    for i, elem in enumerate(tmpSeries):
        mySeries_daily.append(elem[1])
    
    # Delete unnecessary (tmp) variables, which are not needed in further analysis
    del tmpSeries, elem, i, y, data_KART

"""
# Read data sets from file container - get weekly first
# Sample: Crop="Kartoffeln", Station=10361, Period=1961-2020
with pd.HDFStore(str(DIR) + "/" + "hdf5" + "/" + "data_weekly.hdf5") as store_weekly:
    
    tmpSeries = []
    mySeries_weekly = []
    
    data_KART = store_weekly[weekly_files[0]]
    meta_KART_weekly = store_weekly.get_storer(weekly_files[0]).attrs.meta_data
    data_KART['Date'] = data_KART['Date'].dt.strftime('%Y-%m-%d')

    data_KART.set_index('Date', inplace=True)
    data_KART.sort_index(inplace=True)
    
    
    # Partition dataframe data_KART by years
    #agg = data_KART.groupby(pd.DatetimeIndex(data_KART.index).year)
    for y in data_KART.groupby(pd.DatetimeIndex(data_KART.index).year):
        tmpSeries.append(y)
    
    # Get rid of the tuple     
    for i, elem in enumerate(tmpSeries):
        mySeries_weekly.append(elem[1])
    
    # Delete unnecessary (tmp) variables, which are not needed in further analysis
    del tmpSeries, elem, i, y, data_KART
"""

# Create label 'year'
tmp = []
year = []

for i, elem in enumerate(mySeries_daily):
    y = pd.DatetimeIndex(elem.index).year
    dupl = list(dict.fromkeys(y))
    tmp.append(dupl)

for j, elem in enumerate(tmp):
    year.extend(elem)

year = pd.DataFrame(year, columns=['Jahr'])
# Delete unnecessary (tmp) variables, which are not needed in further analysis
del tmp, dupl, elem, i, j, y
    

## Normalize the data, which is actually not necessary, since all data series have the same scale
# First instantiate MinMaxScaler
scaler = MinMaxScaler()
mySeries_daily_norm = []
for i, elem in enumerate(mySeries_daily):
    tmp = scaler.fit_transform(mySeries_daily[i])
    mySeries_daily_norm.append(tmp)
    
for j, elem in enumerate(mySeries_daily_norm):
    mySeries_daily_norm[j] = mySeries_daily_norm[j].reshape(len(mySeries_daily_norm[j]))

# Delete unnecessary (tmp) variables, which are not needed in further analysis
del tmp, elem, i, j


# 1.) K-Means
# A good rule of thumb is choosing k as the square root of the number of points in the training data set
cluster_n = math.ceil(math.sqrt(len(mySeries_daily_norm)))
cluster_count = math.ceil(math.sqrt(math.sqrt(len(mySeries_daily_norm))))

# Euclidean distance metric
km_euc = TimeSeriesKMeans(n_clusters=cluster_n, metric="euclidean", max_iter=1000)
# DTW distance metric
km_dtw = TimeSeriesKMeans(n_clusters=cluster_n, metric="dtw", max_iter_barycenter=1000)

labels_euc = km_euc.fit_predict(mySeries_daily_norm[0:21])
labels_dtw = km_dtw.fit_predict(mySeries_daily_norm[0:21])


# Quick Cluster Validation
print(f'Silhoutte Score(n=8): {silhouette_score(mySeries_daily_norm[0:21], labels_euc)}')


# 2.) Plot Results - for each label plot every series with that label
plot_n = math.ceil(cluster_n / 2)

fig, axs = plt.subplots(nrows=plot_n, ncols=plot_n, figsize=(26,14))
fig.suptitle("Clusters of BOF (%nFK) - calucated with euclidean metric and dtw.barycenter_averaging")

row_i = 0
col_j = 0

# For euclidean distance
for label in set(labels_euc):
    cluster_eu = []
    for i, elem in enumerate(labels_euc):
        if (labels_euc[i] == label):
            axs[row_i, col_j].plot(mySeries_daily_norm[i], c="gray", alpha=0.4)
            cluster_eu.append(mySeries_daily_norm[i])
            
    if len(cluster_eu) > 0:
        axs[row_i, col_j].plot(dtw_barycenter_averaging(np.vstack(cluster_eu)), c="red")
    
    axs[row_i, col_j].set_title("Cluster " + str(row_i*cluster_count+col_j))
    col_j +=1
    
    if col_j%plot_n == 0:
        row_i +=1
        col_j = 0


fig, axs = plt.subplots(nrows=plot_n, ncols=plot_n, figsize=(26,14))
fig.suptitle("Clusters of BOF (%nFK) - calucated with euclidean metric and np.average")

row_i = 0
col_j = 0

# For euclidean distance
for label in set(labels_euc):
    cluster_eu = []
    for i, elem in enumerate(labels_euc):
        if (labels_euc[i] == label):
            axs[row_i, col_j].plot(mySeries_daily_norm[i], c="gray", alpha=0.4)
            cluster_eu.append(mySeries_daily_norm[i])
            
    if len(cluster_eu) > 0:
        axs[row_i, col_j].plot(np.average(np.vstack(cluster_eu), axis=0), c="red")
    
    axs[row_i, col_j].set_title("Cluster " + str(row_i*cluster_count+col_j))
    col_j +=1
    
    if col_j%plot_n == 0:
        row_i +=1
        col_j = 0


fig, axs = plt.subplots(nrows=plot_n, ncols=plot_n, figsize=(26,14))
fig.suptitle("Clusters of BOF (%nFK) - calucated with dtw metric")

row_i = 0
col_j = 0

# For dtw distance metric
for label in set(labels_dtw):
    cluster_dtw = []
    for i, elem in enumerate(labels_dtw):
        if (labels_dtw[i] == label):
            axs[row_i, col_j].plot(mySeries_daily_norm[i], c="gray", alpha=0.4)
            cluster_dtw.append(mySeries_daily_norm[i])
            
    if len(cluster_dtw) > 0:
        axs[row_i, col_j].plot(dtw_barycenter_averaging(np.vstack(cluster_dtw)), c="red")
    
    axs[row_i, col_j].set_title("Cluster " + str(row_i*cluster_count+col_j))
    col_j +=1
    
    if col_j%plot_n == 0:
        row_i +=1
        col_j = 0



# 2.) Apply dimensionality reduction via PCA
pca = PCA(n_components=2)
MySeries_pca = pca.fit_transform(mySeries_daily_norm)

kmeans_pca = KMeans(n_clusters=cluster_n, n_init=100, max_iter=1000)
labels_pca = kmeans_pca.fit_predict(MySeries_pca[0:21]) 

# Plot result
fig, axs = plt.subplots(nrows=plot_n, ncols=plot_n, figsize=(26,14))
fig.suptitle("Clusters of BOF (%nFK) - PCA transformed")

row_i = 0
col_j = 0

# For dtw distance metric
for label in set(labels_pca):
    cluster_pca = []
    for i, elem in enumerate(labels_pca):
        if (labels_pca[i] == label):
            axs[row_i, col_j].plot(mySeries_daily_norm[i], c="gray", alpha=0.4)
            cluster_pca.append(mySeries_daily_norm[i])
            
    if len(cluster_pca) > 0:
        axs[row_i, col_j].plot(dtw_barycenter_averaging(np.vstack(cluster_pca)), c="red")
    
    axs[row_i, col_j].set_title("Cluster " + str(row_i*cluster_count+col_j))
    col_j +=1
    
    if col_j%plot_n == 0:
        row_i +=1
        col_j = 0


# Quick Cluster Validation with silhoutte score
print(f'Silhoutte Score(n=8): {silhouette_score(MySeries_pca[0:21], labels_pca)}')


# Quick plot
mySeries_daily[6].plot(linewidth=1, fontsize=10)
plt.yticks(y_ticks)
mySeries_daily[11].plot(linewidth=1, fontsize=10)
plt.yticks(y_ticks)
mySeries_daily[20].plot(linewidth=1, fontsize=10)
plt.yticks(y_ticks)

##########################################################################################################





