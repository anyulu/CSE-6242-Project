import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from gen_atl_map_ids import get_square_ids

# read in latitude and longitudes of input data
parks = pd.read_csv("../../data/park.csv")
parks = parks.drop(['name'], axis=1)
parks.columns = ['lat', 'long']


# filter data point
parks = parks[(parks['lat']>=33.71950803244919) & (parks['lat']<=33.80849514164657) & (parks['long']>=-84.43872506372654) & (parks['long']<=-84.33168366309474)]

# DBSCAN
parks_tp = np.array(parks.long)
parks_fp = np.array(parks.lat)
parks_X = np.vstack((parks_tp, parks_fp)).T
parks_db = DBSCAN(eps=0.0015, min_samples=1).fit(parks_X)
parks_labels = parks_db.labels_

parks_unique_labels = set(parks_labels)
parks_n_clusters = len(parks_unique_labels) - (1 if -1 in parks_labels else 0)


parks_center = np.zeros((parks_n_clusters,3))
for i in range(len(parks)):
	if parks_labels[i] == -1:
		continue
	parks_center[parks_labels[i]][0] += parks_tp[parks_labels[i]]
	parks_center[parks_labels[i]][1] += parks_fp[parks_labels[i]]
	parks_center[parks_labels[i]][2] += 1
parks_center[:,0] = parks_center[:,0]/parks_center[:,2]
parks_center[:,1] = parks_center[:,1]/parks_center[:,2]

parks_df = pd.DataFrame(parks_center, columns=['long', 'lat', 'count'])


# assign ID to cluster
square_ids = get_square_ids()
for id, square in square_ids:
    bottom_lat = square[0][0]
    top_lat = square[1][0]
    left_long = square[0][1]
    right_long = square[2][1]
    parks_df.loc[(parks_df.lat>=bottom_lat)
                     & (parks_df.lat<top_lat)
                     & (parks_df.long>=left_long)
                     & (parks_df.long<right_long), 'id'] = id

#Get ID and count only
parks_final = parks_df[['id', 'count']].copy()

#Output ID and count to CSV
parks_final.to_csv('../../data/parks_count.csv', index=False)