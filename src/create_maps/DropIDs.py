import json
import numpy as np

# Compare locations.json to locations_v2.json and find differences in IDs

with open('../../data/locations.json') as input_file1:
    location_data1 = json.load(input_file1)

with open('../../data/locations_v2.json') as input_file2:
    location_data2 = json.load(input_file2)

ids_list1 = [i['id'] for i in location_data1['locations']]
ids_list2 = [i['id'] for i in location_data2['locations']]

diff = np.setdiff1d(ids_list1, ids_list2)

np.savetxt('../../data/dropIDs.csv', diff, fmt='%s')
