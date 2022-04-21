import os 
#import re
import pandas as pd
from pathlib import Path

"""
# Define regex pattern for substring extraction
pattern_vStation = re.compile(r'[A-Z0-9]{5}')
pattern_vPeriod = re.compile(r'\d{4}-\d{4}')
pattern_vMainCrop = re.compile(r'[A-Z]+[a-zA-Z]{,3}')
"""

# Get current directoy
cwd = os.getcwd()

# Check exisiting working directory, if not create one
if not os.path.exists(cwd + "/" + "working_dir"):
    os.makedirs("working_dir")
    print("Working directory successfully created")
    
    if not os.path.exists(cwd + "/" + "working_dir" + "/" + "done"):
        os.makedirs(cwd + "/" + "working_dir" + "/" + "done")
        print("Done directory successfully created")
    else:
        print("Done directory already exists")
    
    if not os.path.exists(cwd + "/" + "working_dir" + "/" + "raw_data"):
        os.makedirs(cwd + "/" + "working_dir" + "/" + "raw_data")
    else:
        print("Raw data directory already exists")
else:
    print("Working directory already exists, but check exisiting done and raw directory!")
    
    if not os.path.exists(cwd + "/" + "working_dir" + "/" + "done"):
        os.makedirs(cwd + "/" + "working_dir" + "/" + "done")
        print("Done directory successfully created")
    else:
        print("Done directory already exists")
        
    if not os.path.exists(cwd + "/" + "working_dir" + "/" + "raw_data"):
        os.makedirs(cwd + "/" + "working_dir" + "/" + "raw_data")
        print("Raw data directory successfully created")
    else:
        print("Raw data directory already exists")


# Define path variable
# First path variable contains raw data
WORK_PATH = Path(cwd + "/" + "working_dir" + "/" + "raw_data")
DONE_PATH = Path(cwd + "/" + "working_dir" + "/" + "done")

# List all files within working directory
file_list = []
filename_only = sorted([])
for x in sorted(os.listdir(WORK_PATH)):
    if x.endswith(".txt"):
        file_list.append(x)

        
# Process raw data files and convert them to a manageable data format, like csv
# At first check if the list of files is empty, if not then continue else skip because no files exists to work with
if file_list:
    for i, elem in enumerate(file_list):
        raw_files = pd.read_csv(str(WORK_PATH) + "/" + file_list[i], sep="\s+", header=3, usecols=[0,1,6], encoding='unicode_escape')

        # Alternativ to slicing data (filtering)
        df_file = raw_files.loc[raw_files["Jahr"] != "Station:", "Jahr":"BOF"]
        df_file = raw_files.loc[raw_files["Jahr"] != "Flexibilisierung:", "Jahr":"BOF"]
        df_file = raw_files.loc[raw_files["Jahr"] != "Hauptfrucht:", "Jahr":"BOF"]

        # Special treatment for for Jahr, Tag and BOF
        df_file = raw_files.loc[raw_files["Jahr"].str.contains("Jahr|mm") == False, "Jahr":"BOF"]

        df_file.dropna(inplace=True)
        df_file.reset_index(drop=True, inplace=True)

        # Rename columns caption via index
        df_file = df_file.rename(columns={df_file.columns[2]: "BOF (%nFK)"})

        # Check the number of days of a year, if the year contains more than 365 day then remove the day 366
        indexNames = df_file.loc[df_file["Tag"] == "366", "Jahr":"BOF (%nFK)"].index
        df_file = df_file.drop(indexNames)

        # Quick dtype conversion, because per default all read data are of type object (or string)
        # Use int32/float32 instead of int64/float64 by default to save memory
        df_file['Jahr'] = df_file['Jahr'].astype('int32')
        df_file['Tag'] = df_file['Tag'].astype('int32')

        # Special treatment for the col "BOF (%nFK)" which objects are comma separation instead dot 
        # => relevant for conversion
        df_file['BOF (%nFK)'] = df_file['BOF (%nFK)'].apply(lambda x: x.replace(',', '.')).astype('float32')

        ## Combine cols "Jahr" and "Tag" and then convert it to datetime format, ... 
        ## ... whereby Day 1, 2019 can be translated to jan 1st 2019
        # a.) Create a new col 'Date'
        df_file['Date'] = df_file['Jahr'] * 1000 + df_file['Tag']

        # b.) Convert current date format YYYY-DD to actual date format YYYY-MM-DD
        df_file['Date']  = pd.to_datetime(df_file['Date'], format='%Y%j')
        # insert column using insert(position, column_name, first_column) function              
        df_file.insert(0, 'Date', df_file.pop('Date'))

        # Omit superfluous columns
        df_file = df_file.drop(columns=["Jahr", "Tag"])

        # Filenames without extension .txt
        base = os.path.basename(file_list[i])
        tmp = os.path.splitext(base)
        filename_only.append(tmp[0])

        # export each converted data files, but without meta data
        export_csv = df_file.to_csv(str(DONE_PATH) + "/" + filename_only[i] + ".csv", sep=";", index=False, header=True, encoding="utf-8")
else:
    print("List is empty, hence no files in directory to process")
