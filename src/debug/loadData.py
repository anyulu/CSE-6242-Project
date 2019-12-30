import pandas as pd

busstop = pd.read_csv("../../data/busstop.csv")
busstop = busstop.drop(['stop_id', 'stop_code','stop_name'], axis=1)
busstop.columns = ['lat', 'long']
(row, columns) = busstop.shape
typ = [1]*row
busstop['type'] = typ

park = pd.read_csv("../../data/park.csv")
park = park.drop(['name'], axis=1)
park.columns = ['lat', 'long']
(row, columns) = park.shape
typ = [2]*row
park['type'] = typ

restaurant = pd.read_csv("../../data/restaurants-data.csv")
restaurant = restaurant.drop(['name'], axis=1)
restaurant.columns = ['lat', 'long']
(row, columns) = restaurant.shape
typ = [3]*row
restaurant['type'] = typ

crime = pd.read_csv("../../data/crime-data.csv", encoding = 'ISO-8859-1')
crime = crime.drop(['UC2_Literal','Report Number','Report Date','Location'], axis=1)
crime.columns = ['lat', 'long']
(row, columns) = crime.shape
typ = [4]*row
crime['type'] = typ

data = busstop.append([park,restaurant,crime])
for i in range(data.shape[0]):
        data = data[(data['lat']>=33.718139) & (data['lat']<=33.789353) & (data['long']>=-84.440371) & (data['long']<=-84.332289)]
print(data)

