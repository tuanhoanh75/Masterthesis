import os
import re
import math
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


directory = '/home/aegis/Dokumente/Masterarbeit/archive/'

MySeries = []
namesofMySeries = []

# Plot data

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        df = pd.read_csv(directory + filename)
        df = df.loc[:,["date", "value"]]
        
        df.set_index("date", inplace=True)
        df.sort_index(inplace=True)
        
        MySeries.append(df)
        namesofMySeries.append(filename[:-4])

fig, axs = plt.subplots(6,4, figsize=(25,25))
fig.suptitle('Series')

for i in range(6):
    for j in range(4):
        if i*4+j+1 > len(MySeries):
            continue
        axs[i, j].plot(MySeries[i*4+j].values)
        axs[i, j].set_title(namesofMySeries[i*4+j])
        

# Preprocessing        

series_len = {len(series) for series in MySeries}

ind = 0
for series in MySeries:
    print("[" + str(ind) + "]" + series.index[0] + " " + series.index[len(series) - 1])
    ind+=1


max_len = max(series_len)
longest_series = None
for series in MySeries:
    if len(series) == max_len:
        longest_series = series
        

problems_index = []

for i, elem in enumerate(MySeries):
    if len(MySeries[i]) != max_len:
        problems_index.append(i)
        MySeries[i] = MySeries[i].reindex(longest_series.index)


def nan_counter(list_of_series):
    nan_polluter_series_counter = 0
    for series in list_of_series:
        if series.isnull().sum().sum() > 0:
            nan_polluter_series_counter+=1
    print(nan_polluter_series_counter)
    
    
for i in problems_index:
    MySeries[i].interpolate(limit_direction="both", inplace=True)
    
    
for i, elem in enumerate(MySeries):
    scaler = MinMaxScaler()
    MySeries[i] = scaler.fit_transform(MySeries[i])
    MySeries[i] = MySeries[i].reshape(len(MySeries[i]))


# Clustering using Euclidean and DTW
cluster_n = math.ceil(math.sqrt(len(MySeries)))

km_euclidean = TimeSeriesKMeans(n_clusters=cluster_n, metric="euclidean")
km_dtw = TimeSeriesKMeans(n_clusters=cluster_n, metric="dtw")

labels_eu = km_euclidean.fit_predict(MySeries)
labels_dtw = km_dtw.fit_predict(MySeries)


# Plotting cluster result

plot_n = cluster_n

fig, axs = plt.subplots(plot_n, plot_n, figsize=(25,25))
fig.suptitle("Clusters")

row_i = 0
column_j = 0

# For each label there is plots every series with label
for label in set(label):
    None
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        
