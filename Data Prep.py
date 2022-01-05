import os
import pandas as pd
import seaborn as sns
import datetime as dt
from matplotlib import pyplot as plt

# Presets
plt.rcParams['figure.figsize'] = (10,5)
plt.style.use('fivethirtyeight')

# Get Files from directory
PATH = r"/Users/Tuan/Desktop/Output/Converted_files/csv"
file_list = os.listdir(PATH)

# Presets: Show maximum columns and in one row
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Read csv Data Files; e.g. Kartoffel and interpret decimal with dot instead comma
df_kart = pd.read_csv(PATH + "/" + file_list[1], delimiter=';', header=0, decimal=',')

## Convert columns "Jahr" and "Tag" to datetime format, whereby Day 1, 2019 can be translated to January 1st 2019
# a) Create a new column
df_kart["Combined"] = df_kart["Jahr"] * 1000 + df_kart["Tag"]

# b) Convert current date format Year-Day to actual date
df_kart["Date"] = pd.to_datetime(df_kart["Combined"], format="%Y%j")
first_col = df_kart.pop("Date")             # shift column 'Name' to first position
df_kart.insert(0, "Date", first_col)        # insert column using insert(position,column_name, first_column) function

## At first plot multiple raw time series data
# Set the date column as the index of your DataFrame
print(df_kart[350:370])
df_kart = df_kart.set_index("Date")

print("\n")

# Print the summary statistics of the DataFrame
df_kart = df_kart.drop(columns=["Jahr", "Tag", "Combined"])

ax = df_kart["BOF (Vol%)"]["2003-01-01":"2003-12-31"].plot(linewidth=1, fontsize=10)


# Additional customizations
ax.set_xlabel('Date')
ax.legend(fontsize=10)

plt.show()



