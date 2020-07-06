import numpy as np
import matplotlib.pyplot as plt

file1 = '/Users/clif.jackson/Repositories/bronto-moog-fest/raw/2016/11/25/20161125_000000_20161125_003000_sends_1MA.out'
file2 = '/Users/clif.jackson/Music/MoogFest/data/data_20161125_raw_sends_opens_clicks/data_20161125_sends.out'
file3 = '/Users/clif.jackson/Repositories/bronto-moog-fest/raw/2016/11/25/20161125_000000_20161125_003000_clicks_60MA.out'

x,y = np.loadtxt(file1, delimiter='\t').T

plt.scatter(x,y)
plt.show()
