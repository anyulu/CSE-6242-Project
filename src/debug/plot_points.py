import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_restaurant(filepath):
    data = pd.read_csv(filepath)
    for i in range(data.shape[0]):
        data = data[(data['latitude']>=33.718139) & (data['latitude']<=33.789353) & (data['longitude']>=-84.440371) & (data['longitude']<=-84.332289)]
    print(data.shape)
    xmax = max(data['latitude'])
    xmin = min(data['latitude'])
    ymax = max(data['longitude'])
    ymin = min(data['longitude'])
    #fig = plt.figure()
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.scatter(data['latitude'],data['longitude'])
    plt.title('Restaurant scatter')
    plt.savefig(current_path+"/figures/restaurant_scatter")
    #plt.show()
    return None

current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
plot_restaurant(current_path+"../data/restaurants-data.csv")