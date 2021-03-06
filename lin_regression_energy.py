import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import pandas as pd
from reading_data import data_open_trans
import matplotlib.patheffects as pe

# from sklearn.model_selection import cross_val_score

df_open_transactions = data_open_trans()
print(df_open_transactions.columns.values)

start_time = pd.to_datetime(df_open_transactions['UTCTransactionStart'])


def creating_hour_values(transaction_start_time):
    return float(transaction_start_time.strftime("%H")) + float(transaction_start_time.strftime("%M")) / 60


df_open_transactions['Start Integer Hour_P'] = start_time.apply(lambda row: creating_hour_values(row))

print(df_open_transactions.columns.values)

# print(df_open_transactions['Start Integer Hour_P'])
df_open_transactions['ConnectedTime'] = pd.to_numeric(df_open_transactions['ConnectedTime'])
df_open_transactions = df_open_transactions[df_open_transactions['ConnectedTime'] <= 25]
data = df_open_transactions[['Start Integer Hour_P', 'ConnectedTime', 'TotalEnergy', 'Start Integer Hour']]

plt.scatter(data['Start Integer Hour_P'], data['TotalEnergy'], edgecolors='k',
            s=45, alpha=.8, c='royalblue')
plt.title('Start Time and Total Connected Time')
plt.xlabel('Start Connection Hour ')
plt.ylabel('Total Energy Units')
plt.savefig('scatter_energy', dpi=600)
plt.show()

# pp predict -- total hours connected
# input is start hour

# to predict -- total energy
# input -- start hour

n_components = 5
gmm = GaussianMixture(n_components=n_components, covariance_type='full',
                      random_state=300140951).fit(data[['Start Integer Hour_P', 'ConnectedTime']])

labels = gmm.predict(data[['Start Integer Hour_P', 'ConnectedTime']])
print(labels)
frame = pd.DataFrame(data)
frame['cluster'] = labels
frame.columns = ['Start Integer Hour_P', 'ConnectedTime', 'TotalEnergy', 'Start Integer Hour', 'cluster']
#
print(frame['cluster'].nunique())
# plotting results
color = ['lightgreen', 'yellow', 'deeppink', 'orange', 'magenta', 'yellow', 'black', 'orange', 'pink']
row_color = [['palegreen'], ['khaki'], ['plum'], ['orange']]
marker_r = ["*", "+", "x", "3", ".", "o", "p", "D", "2"]
for k in range(0, 4):
    data = frame[frame["cluster"] == k]
    # print("shape: " + str(data.shape))
    x = data['Start Integer Hour_P'].to_numpy().reshape(-1, 1)
    y = data['TotalEnergy'].to_numpy()
    reg = LinearRegression().fit(x, y)  # only using start connection hour as input ||
    y_pred = reg.predict(x)
    energy_predicted = [round(float(reg.predict(np.array([[hour]]))), 2) for hour in range(min(data['Start Integer Hour']), max(data['Start Integer Hour']) + 1)]
    total_energy_used_per_hour = pd.DataFrame(data.groupby(['Start Integer Hour'], as_index=False)['TotalEnergy']
                                              .mean().round(2))
    total_energy_used_per_hour.columns = ['Connection Start Hour', 'Total Energy Demand']
    print(total_energy_used_per_hour)
    # start_hours = range(0, 24)
    start_hours = range(min(data['Start Integer Hour']), max(data['Start Integer Hour']) + 1)
    # range_demand = range(min(data['Start Integer Hour']), max(data['Start Integer Hour']) + 1)

    energy_per_start_hour = pd.DataFrame(list(zip(start_hours, energy_predicted)),
                                         columns=['Connection Start Hour',
                                                  'Total Energy predicted'])
    # energy_per_start_hour_demand = pd.DataFrame(list(zip(range_demand, total_energy_used_per_hour)),
    #                                             columns=['Connection Start Hour',
    #                                                      'Total Energy demand'])
    #
    plt.axis('off')
    plt.axis('tight')
    plt.table(cellText=total_energy_used_per_hour.values, colLabels=total_energy_used_per_hour.columns,
              cellLoc='center', colColours=row_color[k] * 2,
              loc='center')
    plt.title("Energy demand for cluster of color " + str(color[k]), y=1.01)
    plt.axis('tight')
    plt.savefig("table-for-energy-demand " + str(color[k]), dpi=600)
    plt.show()
    plt.close()

    ## demand energy

    plt.axis('off')
    plt.axis('tight')
    plt.table(cellText=energy_per_start_hour.values, colLabels=energy_per_start_hour.columns,
              cellLoc='center', colColours=row_color[k] * 2,
              loc='center')
    plt.title("Energy prediction for cluster of color " + str(color[k]), y=1.08)
    plt.savefig("table-for-" + str(color[k]), dpi=600)
    plt.show()
    plt.close()

    x1 = energy_per_start_hour['Connection Start Hour'].tolist()
    y1 = energy_per_start_hour['Total Energy predicted'].tolist()

    x2 = total_energy_used_per_hour['Connection Start Hour'].tolist()
    y2 = total_energy_used_per_hour['Total Energy Demand'].tolist()

    plt.plot(x1, y1, label="Predicted Energy", color=color[k], mec='k', marker='o')
    plt.plot(x2, y2, label="Energy Demand", color='k', marker='o')
    plt.xlabel('Start Connection Hour')
    plt.ylabel('Average Energy Demand vs Energy Predicted (kWh)')

    plt.title('Average Energy Demand vs Energy Predicted for cluster of color  ' + str(color[k]))

    plt.legend()
    plt.savefig('Energy-demand-vs-predicted color ' + str(color[k]), dpi=600)
    plt.show()

    # print(hours_per_start_hour.shape)

    # print("Prediction of total energy used with " + str(color[k]) +
    #       " cluster at 7 PM " + str(reg.predict(np.array([[19]]))))
    # print("Score :" + str(reg.score(x, y) * 100))
    # plt.xlim(-1, 26)
    # plt.ylim(-1, 26)
    # plt.scatter(data['Start Integer Hour_P'], data['ConnectedTime'], c=color[k], edgecolors='k',
    #             s=50, alpha=.8)
    # max_x = round(float(max(x)), 2)
    # max_y = round(float(max(y)), 2)
    # min_x = round(float(min(x)), 2)
    # min_y = round(float(min(y)), 2)
    # plt.xlabel(str(min_x) + '<= Start Connection Hour <=' + str(max_x))
    # plt.ylabel(str(min_y) + '<= Total Hours Connected <=' + str(max_y))
    # plt.savefig("cluster " + str(color[k]), dpi=600)
    # plt.show()
    # plt.close()

# color = ['lightgreen', 'yellow', 'deeppink', 'orange', 'magenta', 'yellow', 'black', 'orange', 'pink']
# marker_r = ["*", "+", "x", "3", ".", "o", "p", "D", "2"]
# for k in range(0, 4):
#     data = frame[frame["cluster"] == k]
#     print("shape: " + str(data.shape))
#
#     plt.scatter(data['Start Integer Hour_P'], data['ConnectedTime'], c=color[k], edgecolors='k',
#                 s=50, alpha=.8)
#
# plt.title('GMM Visualization with ' + str(n_components) + ' clusters of charging sessions')
# plt.xlabel('Start Connection Hour ')
# plt.ylabel('Total Hours Connected')
# plt.savefig('gmm_fig', dpi=600)
# plt.show()
