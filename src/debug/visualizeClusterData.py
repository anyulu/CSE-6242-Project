import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt

data = np.genfromtxt("../../data/crime_score.csv", delimiter=',')
data = 5 + 2 *(data-np.mean(data))/np.std(data)
for i in range(4225):
    if data[i] > 10: data[i] = 10
    elif data[i] < 0: data[i] = 0
## normalzie
data2 = data.reshape((65,65))
sns.heatmap(data2)
plt.show()

clusterData = pd.read_csv("../../data/crime_count.csv")
x = []
y = []
r = []
for i in range(len(clusterData)):
    y.append(int(clusterData['id'][i]/66))
    x.append(clusterData['id'][i]%66)
    r.append(np.log(clusterData['count'][i]))

plt.scatter(x,y,r)
plt.show()