import os
import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
# Preproccesing
from sklearn.preprocessing import MinMaxScaler
# Algorithms 
from tslearn.barycenters import dtw_barycenter_averaging
from tslearn.clustering import TimeSeriesKMeans
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


dire = '/home/aegis/Dokumente/Masterarbeit/archive/'

MySeries = []
namesofMySeries = []

# Plot data

for filename in os.listdir(dire):
    if filename.endswith(".csv"):
        df = pd.read_csv(dire + filename)
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

plot_n = math.ceil(math.sqrt(cluster_n))

fig, axs = plt.subplots(plot_n, plot_n, figsize=(25,25))
fig.suptitle("Clusters with euclidean and np.average")

row_i = 0
column_j = 0

# For each label there is plots every series with label
# With euclidean distance metric 
for label in set(labels_eu):
    cluster_eu = []
    for i, elem in enumerate(labels_eu):
        if (labels_eu[i] == label):
            axs[row_i, column_j].plot(MySeries[i], c="gray", alpha=0.4)
            cluster_eu.append(MySeries[i])
        
    if len(cluster_eu) > 0:
        axs[row_i, column_j].plot(np.average(np.vstack(cluster_eu), axis=0), c="red")
        axs[row_i, column_j].set_title("Cluster " + str(row_i*cluster_n+column_j))
        column_j += 1
        
    if column_j%plot_n == 0:
        row_i += 1
        column_j = 0

        

####################################################################################################

plot_n = math.ceil(math.sqrt(cluster_n))

fig, axs = plt.subplots(plot_n, plot_n, figsize=(25,25))
fig.suptitle("Clusters with dtw and np.averaging")

row_i = 0
column_j = 0


# With dtw distance metric 
for label in set(labels_dtw):
    cluster_dtw = []
    for i, elem in enumerate(labels_dtw):
        if (labels_dtw[i] == label):
            axs[row_i, column_j].plot(MySeries[i], c="gray", alpha=0.4)
            cluster_dtw.append(MySeries[i])
        
    if len(cluster_dtw) > 0:
        axs[row_i, column_j].plot(np.average(np.vstack(cluster_dtw), axis=0), c="red")
        axs[row_i, column_j].set_title("Cluster " + str(row_i*cluster_n+column_j))
        column_j += 1
        
    if column_j%plot_n == 0:
        row_i += 1
        column_j = 0



plot_n = math.ceil(math.sqrt(cluster_n))

fig, axs = plt.subplots(plot_n, plot_n, figsize=(25,25))
fig.suptitle("Clusters with dtw and dtw_barycenter_averaging")

row_i = 0
column_j = 0


# With dtw distance metric 
for label in set(labels_dtw):
    cluster_dtw = []
    for i, elem in enumerate(labels_dtw):
        if (labels_dtw[i] == label):
            axs[row_i, column_j].plot(MySeries[i], c="gray", alpha=0.4)
            cluster_dtw.append(MySeries[i])
        
    if len(cluster_dtw) > 0:
        axs[row_i, column_j].plot(dtw_barycenter_averaging(np.vstack(cluster_dtw)), c="red")
        axs[row_i, column_j].set_title("Cluster " + str(row_i*cluster_n+column_j))
        column_j += 1
        
    if column_j%plot_n == 0:
        row_i += 1
        column_j = 0
        
        
# Cluster Distribution for eu and dtw
cluster_c_eu = [len(labels_eu[labels_eu==i]) for i in range(cluster_n)]
cluster_num_eu = ["Cluster " + str(i) for i in range(cluster_n)]

plt.figure(figsize=(15,5))
plt.title("Cluster Distribution for KMeans with eu")
plt.bar(cluster_num_eu, cluster_c_eu)

cluster_c_dtw = [len(labels_dtw[labels_dtw==i]) for i in range(cluster_n)]
cluster_num_dtw = ["Cluster " + str(i) for i in range(cluster_n)]

plt.figure(figsize=(15,5))
plt.title("Cluster Distribution for KMeans with dtw")
plt.bar(cluster_num_dtw, cluster_c_dtw)


# Cluster Mapping
names_for_labels_eu = [f"Cluster {label}" for label in labels_eu]
pd.DataFrame(zip(namesofMySeries, names_for_labels_eu), 
             columns=["Series", "Cluster"]).sort_values(by="Cluster").set_index("Series")

names_for_labels_dtw = [f"Cluster {label}" for label in labels_dtw]
pd.DataFrame(zip(namesofMySeries, names_for_labels_dtw), 
             columns=["Series", "Cluster"]).sort_values(by="Cluster").set_index("Series")
 

###################################################################################   
  
  
# Curse of Dimensionality
pca = PCA(n_components=2)
MySeries_transformed = pca.fit_transform(MySeries)

plt.figure(figsize=(25,10))
plt.scatter(MySeries_transformed[:,0], MySeries_transformed[:, 1], s=300)

kmeans = KMeans(n_clusters=6, max_iter=5000)
labels_pca_transformed = kmeans.fit_predict(MySeries_transformed)

plt.figure(figsize=(25,10))
plt.scatter(MySeries_transformed[:,0], MySeries_transformed[:, 1], 
            c=labels_pca_transformed, s=300)


plot_n = math.ceil(math.sqrt(cluster_n))

fig, axs = plt.subplots(plot_n, plot_n, figsize=(25,25))
fig.suptitle("Clusters with PCA transformed series")

row_i = 0
column_j = 0

# set() groups clusters, e.g.: [0 0 0 1 2 2 3 4 4 4 5 5] => {0 1 2 3 4 5}
for label in set(labels_pca_transformed):
    cluster_pca = []
    for i, elem in enumerate(labels_pca_transformed):
        if (labels_pca_transformed[i] == label):
            axs[row_i, column_j].plot(MySeries[i], c="gray", alpha=0.4)
            cluster_pca.append(MySeries[i])
        
    if len(cluster_pca) > 0:
        axs[row_i, column_j].plot(np.average(np.vstack(cluster_pca), axis=0), c="red")
        axs[row_i, column_j].set_title("Cluster " + str(row_i*8+column_j))
        column_j += 1
        
    if column_j%plot_n == 0:
        row_i += 1
        column_j = 0
    
    
    
    
    
    
    
    

        
