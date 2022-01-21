import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# Generate time series of lenght of t = 10
t = range(1,11)


ts = pd.DataFrame([3,1,2,6,4,1,1,8,4,0], index=t)
print(ts)

ts = ts.rename(columns={ts.columns[0]: 'x'})

plt.plot(ts.x, linewidth=1)
