import pandas as pd
import numpy as np
from pathlib import Path
import os

data_folder = Path("/home/aegis/Dokumente/Masterarbeit/Data/Converted_files/csv")

file_list = sorted(os.listdir(data_folder))

print(file_list)

