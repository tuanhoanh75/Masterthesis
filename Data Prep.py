import os
import numpy as np
import pandas as pd
import seaborn as sns
import datetime as dt
from matplotlib import pyplot as plt

# Presets
plt.rcParams['figure.figsize'] = (10,5)
plt.style.use('fivethirtyeight')

# Get Files from directory
PATH = r"/Users/Tuan/Masterarbeit/Data/Converted_files/csv"
file_list = os.listdir(PATH)

# Presets: Show maximum columns and in one row
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Read csv Data Files; e.g. Kartoffel and interpret decimal with dot instead comma; Taking int32 instead default
# int64 or float64 respectively for saving memory
df_kart = pd.read_csv(PATH + "/" + file_list[1], delimiter=';', header=0,
                      decimal=',', usecols=["Jahr", "Tag", "BOF (%nFK)", "BOF (Vol%)"],
                      dtype={"Jahr": np.int32, "Tag": np.int32, "BOF (%nFK)": np.float16, "BOF (Vol%)": np.float16})


## Convert columns "Jahr" and "Tag" to datetime format, whereby Day 1, 2019 can be translated to January 1st 2019
# a) Create a new column
df_kart["Combined"] = df_kart["Jahr"] * 1000 + df_kart["Tag"]

print(df_kart.head())
print(df_kart.info())

# b) Convert current date format Year-Day to actual date
df_kart["Date"] = pd.to_datetime(df_kart["Combined"], format="%Y%j")
first_col = df_kart.pop("Date")             # shift column 'Name' to first position
df_kart.insert(0, "Date", first_col)        # insert column using insert(position,column_name, first_column) function

# c) Quick resample data from daily to weekly level
df_weekly = df_kart.drop(columns=["Jahr", "Tag", "Combined", "BOF (Vol%)"])         # Omit superfluous columns
df_weekly = df_weekly.resample('W', on='Date').mean()                               # With on='Date' it sets automatically column "Date"  as index

## At first plot multiple raw time series data
# Set the date column as the index of your DataFrame
df_kart = df_kart.set_index("Date")

print("\n")

# Print the summary statistics of the DataFrame
df_kart = df_kart.drop(columns=["Jahr", "Tag", "Combined"])
y_ticks = np.arange(0, 110, 10)

plt.yticks(y_ticks)
ax_daily = df_kart["BOF (%nFK)"]["1961-01-01":"1961-12-31"].plot(linewidth=1, fontsize=10)
ax_weekly = df_weekly["BOF (%nFK)"]["1961-01-01":"1961-12-31"].plot(linewidth=1, fontsize=10)
