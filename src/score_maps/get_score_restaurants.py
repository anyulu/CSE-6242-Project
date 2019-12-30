import numpy as np
import pandas as pd
import math
import json
from sklearn.cluster import DBSCAN
import os
import pandas as pd
from collections import OrderedDict

GEN_MAP = False

# if(not os.path.exists('restaurants_center.pkl')):
restaurants = pd.read_csv("../../data/restaurants-data.csv")
restaurants = restaurants.drop(['name'], axis=1)
restaurants.columns = ['lat', 'long']

# filter data point
restaurants = restaurants[(restaurants['lat'] >= 33.71950803244919) & (restaurants['lat'] <= 33.80849514164657)
                          & (restaurants['long'] >= -84.43872506372654) & (restaurants['long'] <= -84.33168366309474)]

# DBSCAN
restaurants_tp = np.array(restaurants.long)
restaurants_fp = np.array(restaurants.lat)
restaurants_X = np.vstack((restaurants_tp, restaurants_fp)).T
# print(np.max(restaurants_tp), np.min(restaurants_tp))
# print(np.max(restaurants_fp), np.min(restaurants_fp))
# for i in restaurants_X:
#     print(i)
restaurants_db = DBSCAN(eps=0.001, min_samples=4).fit(restaurants_X)
restaurants_labels = restaurants_db.labels_
restaurants_unique_labels = set(restaurants_labels)

restaurants_n_clusters = len(restaurants_unique_labels) - (1 if -1 in restaurants_labels else 0)

restaurants_center = []
for i in range(len(restaurants)):
    if restaurants_labels[i] == -1:
        continue
    restaurants_center.append(
        [restaurants_labels[i], restaurants_X[i][1], restaurants_X[i][0]])

# print(restaurants_center)


restaurants_center = pd.DataFrame(restaurants_center, columns=['Group', 'Lat', 'Lng'])

#     pkl.dump(restaurants_center, open('restaurants_center.pkl', 'wb'))
# else:
#     restaurants_center = pkl.load(open('restaurants_center.pkl', 'rb'))
# print(restaurants_center)

restaurant_groups = restaurants_center.groupby('Group')

cluster_centers = []
for name, group in restaurant_groups:
    # print(group)
    cluster_centers.append([np.mean(group['Lat']), np.mean(group['Lng']), len(group)])
    # print('Size of Group: ',len(group))

restaurants_df = pd.DataFrame(cluster_centers, columns=['lat', 'lng', 'count'])
restaurants_by_id = []
## The following
with open('../../data/locations_v2.json') as json_file:

    json_body = json.load(json_file)

    # read from locations_v2.json
    all_locations = json_body["locations"].copy()  # all the locations
    block_ids = list(map(lambda block: int(block["id"]), all_locations))  # all the ids of those locations
    num_blocks = len(block_ids)  # for us this will be 4,356

    # check if bus stops exist within the square
    lat_diff = 0.0013690324491903993
    lng_diff = np.mean([0.001645962522360378, 0.0016459887730206901, 0.00164601502547157, 0.0016460412796845958,
                        0.0016460675356881893, 0.0016460937934681397, 0.0016461200530244469, 0.001646146314357111,
                        0.0016461725774661318, 0.0016461988423515095, 0.0016462251090274549, 0.0016462513774655463,
                        0.0016462776476942054, 0.0016463039196850104, 0.0016463301934663832, 0.0016463564690241128,
                        0.0016463827463724101, 0.0016464090254828534, 0.0016464353063838644, 0.0016464615890470213,
                        0.001646487873500746, 0.0016465141597308275, 0.0016465404477514767, 0.0016465667375342719,
                        0.0016465930291076347, 0.0016466193224573544, 0.0016466456175976418, 0.0016466719145000752,
                        0.0016466982131930763, 0.0016467245136624342, 0.001646750815908149, 0.0016467771199444314,
                        0.0016468034257570707, 0.0016468297333460669, 0.0016468560427256307, 0.0016468823538815514,
                        0.0016469086668138289, 0.001646934981536674, 0.001646961298035876, 0.001646987616311435,
                        0.0016470139363633507, 0.001647040258205834, 0.0016470665818388852, 0.0016470929072482932,
                        0.001647119234434058, 0.0016471455633961796, 0.0016471718941488689, 0.001647198226692126,
                        0.001647224560997529, 0.0016472508971077104, 0.001647277234980038, 0.001647303574657144,
                        0.0016473299160963961, 0.0016473562593262159, 0.0016473826043466033, 0.0016474089511433476,
                        0.0016474352997164488, 0.0016474616500801176, 0.001647488002234354, 0.0016475143561649475,
                        0.0016475407118718977, 0.0016475670693694155, 0.0016475934286575011, 0.0016476197897219436,
                        0.0016476461525769537])
    # Create boolean map of squares that contain bus stops
    restaurant_map = OrderedDict(dict.fromkeys(block_ids, False))

    for location in all_locations:
        # print(location)
        id = location['id']
        bottom_lat = location['coords']['lat']
        left_lng = location['coords']['lng']
        # check if any bus stops exist within the square
        # drop if so
        top_lat = bottom_lat + lat_diff
        right_lng = left_lng + lng_diff
        # print(top_lat, bottom_lat)
        # print(left_lng, right_lng)
        within_lat = restaurants_df[restaurants_df['lat'].between(bottom_lat, top_lat)].index
        within_lng = restaurants_df[restaurants_df['lng'].between(left_lng, right_lng)].index
        within_sq = within_lat.intersection(within_lng)
        # print(within_lat)
        # print(within_lng)
        # print(within_sq)

        if(len(within_sq) > 0):
            restaurant_map[id] = True
            # print(within_sq.values)
            # print(restaurants_df.iloc[within_sq])
            # print(restaurants_df.iloc[within_sq]['count'].values[0])
            # append the id and the count
            restaurants_by_id.append([id,restaurants_df.iloc[within_sq]['count'].values[0]])
    # print('lat', np.mean())
    # print('lng', np.mean(np.delete(lng_diff,0)))

restaurants_final = pd.DataFrame(restaurants_by_id, columns=['id', 'count'])
restaurants_final.to_csv('../../data/restaurants_count.csv', index=False)
# print(df_to_save)
# Save
with open('../../data/restaurant_map.json', 'w') as fp:
    json.dump(restaurant_map, fp)

