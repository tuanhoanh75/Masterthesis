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
from minisom import MiniSom
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from tslearn.barycenters import dtw_barycenter_averaging
from tslearn.clustering import TimeSeriesKMeans, silhouette_score


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

tmp_data = mySeries_daily_norm[0:21]
tmp_data = np.reshape(tmp_data, (21, 365, 1))


# Quick Cluster Validation
print('Silhoutte Score(n_cluster=8):', silhouette_score(tmp_data, labels=labels_euc, metric="euclidean"))
print('\nSilhoutte Score(n_cluster=8):', silhouette_score(tmp_data, labels=labels_dtw, metric="dtw"))


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
print('\nSilhoutte Score(n=8):', silhouette_score(MySeries_pca[0:21], labels_pca))


# 3.) SOM Clustering
som_x = som_y = math.ceil(math.sqrt(math.sqrt(len(mySeries_daily_norm))))

# Try out adjustment to the learning paramater - the first two passed args deterine the map size
# initialization of 8x8 SOM will yield the SOM map size 
som = MiniSom(som_x, som_y, len(mySeries_daily_norm[0]), sigma=1.0, learning_rate=0.2, 
              neighborhood_function='gaussian', activation_distance='cosine')

weight = som.random_weights_init(mySeries_daily_norm)
som.train(mySeries_daily_norm[0:21], num_iteration=50000)     # train SOM with given data and pass number training iterations

# Plot result
def plot_som_series_averaged_center(som_x, som_y, win_map):
    fig, axs = plt.subplots(som_x, som_y, figsize=(26,14))
    fig.suptitle("Clusters via SOM")
    
    for x in range(som_x):
        for y in range(som_y):
            cluster = (x,y)
            if cluster in win_map.keys():
                for series in win_map[cluster]:
                    axs[cluster].plot(series, c="gray", alpha=0.5)
                axs[cluster].plot(np.average(np.vstack(win_map[cluster]), axis=0), c="red")
            
            cluster_num = x*som_y+y+1
            axs[cluster].set_title(f'Cluster {cluster_num}')
            

win_map = som.win_map(mySeries_daily_norm[0:21])

# Obtain the position of the winning neuron on the map; each neuron represents a cluster
winner = []

for w, elem in enumerate(mySeries_daily_norm[0:21]):
    tmp = som.winner(mySeries_daily_norm[w])
    winner.append(tmp)

plot_som_series_averaged_center(som_x, som_y, win_map)


# Quick plot
mySeries_daily[5].plot(linewidth=1, fontsize=10)
plt.yticks(y_ticks)
mySeries_daily[6].plot(linewidth=1, fontsize=10)
plt.yticks(y_ticks)
mySeries_daily[9].plot(linewidth=1, fontsize=10)
plt.yticks(y_ticks)
#mySeries_daily[17].plot(linewidth=1, fontsize=10)
#plt.yticks(y_ticks)


##########################################################################################################

# Quick Introduction to tsfresh package
from tsfresh.examples.robot_execution_failures import download_robot_execution_failures, load_robot_execution_failures
from tsfresh import select_features, extract_features, extract_relevant_features
from tsfresh.utilities.dataframe_functions import impute


download_robot_execution_failures()
timeseries, y = load_robot_execution_failures()

print(timeseries.head())

## Plot data with id == 3 (no failure) and id == 20 (failure)
timeseries[timeseries['id'] == 3].plot(subplots=True, sharex=True, figsize=(10,10)) 
timeseries[timeseries['id'] == 20].plot(subplots=True, sharex=True, figsize=(10,10))

# Returns a dataframe with more than 1200 different extracted features
extracted_features = extract_features(timeseries, column_id="id", column_sort="time")

# Next remove Nan Values and select relevant features
impute(extracted_features)
# Only around 682 features were classified as relevant enough
features_filtered = select_features(extracted_features, y)

# Furthermore, perform extraction, imputing and filtering at the same time with (yield same result)
features_filtered_direct = extract_relevant_features(timeseries, y, column_id="id", column_sort="time")

features_filtered = features_filtered.sort_values(by=['F_x__value_count__value_-1'])


# Export features extraction
export_features = features_filtered.to_csv("expor_features.csv", sep=';', index=False, header=True, encoding='utf-8')












