import pandas as pd
import json
import numpy as np
from collections import OrderedDict

# read in subway stop data
subway = pd.read_csv("../../data/subway.csv")
subway = subway.drop(['stop_name'], axis=1)
subway.columns = ['lat', 'long']

# print(subway)

# filter data points
subway = subway[(subway['lat']>=33.71950803244919) &
                  (subway['lat']<=33.80849514164657) &
                  (subway['long']>=-84.43872506372654) &
                  (subway['long']<=-84.33168366309474)]

with open('../data/locations_v2.json') as json_file:

    json_body = json.load(json_file)

    # read from locations_v2.json
    all_locations = json_body["locations"].copy()  # all the locations
    block_ids = list(map(lambda block: int(block["id"]), all_locations))  # all the ids of those locations
    num_blocks = len(block_ids)  # for us this will be 4,356

    # check if subway stops exist within the square
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
    # Create boolean map of squares that contain subway stops
    subwaymap = OrderedDict(dict.fromkeys(block_ids , False))

    for location in all_locations:
        # print(location)
        id = location['id']
        bottom_lat = location['coords']['lat']
        left_lng = location['coords']['lng']
        # check if any subway stops exist within the square
        # drop if so
        top_lat = bottom_lat + lat_diff
        right_lng = left_lng + lng_diff
        # print(top_lat, bottom_lat)
        # print(left_lng, right_lng)
        within_lat = subway[subway['lat'].between(bottom_lat, top_lat)].index
        within_lng = subway[subway['long'].between(left_lng, right_lng)].index
        within_sq = within_lat.intersection(within_lng)
        # print(within_lat)
        # print(within_lng)
        # print(within_sq)

        if(len(within_sq) > 0):
            subwaymap[id] = True
    # print('lat', np.mean())
    # print('lng', np.mean(np.delete(lng_diff,0)))

# print(df_to_save)
# Save
with open('../../data/subway_map.json', 'w') as fp:
    json.dump(subwaymap, fp)
