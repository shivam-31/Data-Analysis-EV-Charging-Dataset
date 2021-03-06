from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
from reading_data import data_open_trans
plt.rcParams.update(plt.rcParamsDefault)

df_open_transactions = data_open_trans()

print(df_open_transactions.columns.values)

start_time = pd.to_datetime(df_open_transactions['UTCTransactionStart'])


def creating_hour_values(transaction_start_time):
    return float(transaction_start_time.strftime("%H")) + float(transaction_start_time.strftime("%M")) / 60


df_open_transactions['Start Integer Hour_P'] = start_time.apply(lambda row: creating_hour_values(row))

# print(df_open_transactions.columns.values)

# print(df_open_transactions['Start Integer Hour_P'])
df_open_transactions['ConnectedTime'] = pd.to_numeric(df_open_transactions['ConnectedTime'])
df_open_transactions = df_open_transactions[df_open_transactions['ConnectedTime'] <= 24]
df = data = df_open_transactions[['Start Integer Hour_P', 'ConnectedTime']]
distortions = []
K = range(1, 10)
for k in K:
    kmeanModel = KMeans(n_clusters=k)
    kmeanModel.fit(df)
    distortions.append(kmeanModel.inertia_)

fig = plt.figure(figsize=(16, 8))
plt.grid()
fig.patch.set_facecolor('xkcd:salmon')
plt.plot(K, distortions, 'ko-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k (K-Means)')
plt.savefig('elbow_means_24_kmeans_pp', dpi=600)
plt.show()

