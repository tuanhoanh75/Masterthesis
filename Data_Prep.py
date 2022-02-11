import os
import numpy as np
import pandas as pd


# Presets
#plt.rcParams['figure.figsize'] = (12,6)
#plt.style.use('fivethirtyeight')

# Get Files from directory --> Please use your directory
PATH = r"/home/aegis/Dokumente/Masterarbeit/Data/Converted_files/csv"
PATH_2 = r"/home/aegis/Dokumente/Masterarbeit/Data/Converted_files/"
file_list = sorted(os.listdir(PATH))


# Presets: Show maximum columns and in one row
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Read csv Data Files; e.g. Kartoffel and interpret decimal with dot instead comma; Taking int32 instead default
# int64 or float64 respectively for saving memory
for f in range(len(file_list)):
    df_daily = pd.read_csv(PATH + "/" + file_list[0], delimiter=';',
                       header=0, decimal=',', usecols=["Jahr", "Tag", "BOF (%nFK)", "BOF (Vol%)"],
                       dtype={"Jahr": np.int32, "Tag": np.int32, "BOF (%nFK)": np.float32, "BOF (Vol%)": np.float32})


    ## Convert cols "Jahr" and "Tag" to datetime format, whereby Day 1, 2019 can be translated to jan 1st 2019
    # a.) Create a new col
    df_daily["Combined"] = df_daily["Jahr"] * 1000 + df_daily["Tag"]

    # b.) Convert current date format Year-Day to actual date
    df_daily["Date"] = pd.to_datetime(df_daily["Combined"], format="%Y%j")
    daily = df_daily.pop("Date")              # shift column 'Name' to first position
    df_daily.insert(0, "Date", daily)         # insert column using insert(position,column_name, first_column) function

    # c) Quick resample data from daily to weekly level
    df_weekly = df_daily.drop(columns=["Jahr", "Tag", "Combined", "BOF (Vol%)"])
    df_weekly = df_weekly.resample("W", on="Date").mean()

    # Quick reset datetime index to column + re-arrange column order
    df_weekly["Date"] = df_weekly.index
    df_weekly = df_weekly.reset_index(drop=True)
    weekly = df_weekly.pop("Date")                    # shift column 'Name' to first position
    df_weekly.insert(0, "Date", weekly)

    # Omit superfluous columns like above
    df_daily = df_daily.drop(columns=["Jahr", "Tag", "Combined", "BOF (Vol%)"])


    # Tip: Instead using PATH + '/' + ... -> use os.path.join to make it OS independet
    export_daily = df_daily.to_csv(PATH_2 + 'Daily' + '/' + 'daily_' + file_list[f],
                                   sep=';', index=False, header=True, encoding='utf-8')

    export_weekly = df_weekly.to_csv(PATH_2 + 'Weekly' + '/' + 'weekly_' + file_list[f],
                                   sep=';', index=False, header=True, encoding='utf-8')


#########

"""
df_daily_kart = pd.read_csv(PATH + "/" + file_list[1], delimiter=';', header=0,
                      decimal=',', usecols=["Jahr", "Tag", "BOF (%nFK)", "BOF (Vol%)"],
                      dtype={"Jahr": np.int32, "Tag": np.int32, "BOF (%nFK)": np.float32, "BOF (Vol%)": np.float32})


## Convert columns "Jahr" and "Tag" to datetime format, whereby Day 1, 2019 can be translated to January 1st 2019
# a) Create a new column
df_daily_kart["Combined"] = df_daily_kart["Jahr"] * 1000 + df_daily_kart["Tag"]

# b) Convert current date format Year-Day to actual date
df_daily_kart["Date"] = pd.to_datetime(df_daily_kart["Combined"], format="%Y%j")
first_col = df_daily_kart.pop("Date")             # shift column 'Name' to first position
df_daily_kart.insert(0, "Date", first_col)        # insert column using insert(position,column_name, first_column) function

# c) Quick resample data from daily to weekly level
df_daily_weekly = df_daily_kart.drop(columns=["Jahr", "Tag", "Combined", "BOF (Vol%)"])         # Omit superfluous columns
df_daily_weekly = df_daily_weekly.resample('W', on='Date').mean()                               # With on='Date' it sets automatically column "Date"  as index


# Quick reset datetime index to column + re-arrange column order
df_daily_weekly['Date'] = df_daily_weekly.index
df_daily_weekly = df_daily_weekly.reset_index(drop=True)
var_shift = df_daily_weekly.pop("Date")
df_daily_weekly.insert(0, "Date", var_shift)


# Omit superfluous columns like above
df_daily_kart = df_daily_kart.drop(columns=["Jahr", "Tag", "Combined", "BOF (Vol%)"])


export_daily = df_daily_kart.to_csv(PATH + '/' + 'daily_' + file_list[1],
                             sep=';', index=False, header=True, encoding='utf-8')

export_weekly = df_daily_weekly.to_csv(PATH + '/' + 'weekly_' + file_list[1],
                               sep=';', index=False, header=True, encoding='utf-8')

## At first plot multiple raw time series data
# Set the date column as the index of your DataFrame
#df_daily_kart = df_daily_kart.set_index("Date")

y_ticks = np.arange(0, 110, 10)
plt.yticks(y_ticks)
ax_daily = df_daily_kart["BOF (%nFK)"]["1961-01-01":"1961-12-31"].plot(linewidth=1, fontsize=10)
ax_weekly = df_daily_weekly["BOF (%nFK)"]["1961-01-01":"1961-12-31"].plot(linewidth=1, fontsize=10)

## Try out some naiv clustering (e.g. hierarchical) approach
"""
