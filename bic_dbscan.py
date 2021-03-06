import numpy as np
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from reading_data import data_open_trans

sns.set()

df_open_transactions = data_open_trans()
print(df_open_transactions.columns.values)

start_time = pd.to_datetime(df_open_transactions['UTCTransactionStart'])


def creating_hour_values(transaction_start_time):
    return float(transaction_start_time.strftime("%H")) + float(transaction_start_time.strftime("%M")) / 60


df_open_transactions['Start Integer Hour_P'] = start_time.apply(lambda row: creating_hour_values(row))

print(df_open_transactions.columns.values)
df_open_transactions['ConnectedTime'] = pd.to_numeric(df_open_transactions['ConnectedTime'])
df_open_transactions = df_open_transactions[df_open_transactions['ConnectedTime'] <= 80]
data = df_open_transactions[['Start Integer Hour_P', 'ConnectedTime']]

neigh = NearestNeighbors(n_neighbors=2)
nbrs = neigh.fit(data)
distances, indices = nbrs.kneighbors(data)

distances = np.sort(distances, axis=0)
distances = distances[:, 1]
fig = plt.figure(figsize=(16, 8))
ax = plt.axes()

fig.patch.set_facecolor('xkcd:salmon')
plt.plot(distances, c='black')
# plt.xlabel('Start Connection Hour ')
plt.ylabel('Epsilon Value')
plt.title('THe BIC method showing the optimal value of Epsilon')
ax.minorticks_on()
#ax.grid(True, which='both', linestyle='-')
#plt.grid()
plt.savefig('bic_plot', dpi=600)
plt.show()
