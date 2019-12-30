import pandas as pd
import numpy as np
import math
import json

score_dataset = 'crime'
# score_dataset = 'restaurant'

distance_measure = 'Drive'
# distance_measure = 'Walk'

clusterData = pd.read_csv('../../data/' + score_dataset +'_count.csv')
if distance_measure == 'Drive':
    timeData = pd.read_csv("../../data/clean_TravelTimes.csv")
else:
    timeData = pd.read_csv("../../data/clean_WalkingTravelTimes.csv")

clusterNum = len(clusterData)
with open('../../data/locations_v2.json') as input_file2:
    location_data2 = json.load(input_file2)
ids_list2 = [i['id'] for i in location_data2['locations']]
blockNum = len(ids_list2)
print(blockNum, clusterNum)
score = np.zeros(blockNum)
for i in range(blockNum): # i is the source block id
    thisID = int(ids_list2[i])
    print(thisID)
    temp = 0
    for j in range(clusterNum):
        thisCluster = clusterData['id'][j] #Destination block id
        #print(thisCluster)
        if thisCluster == thisID: # in this case there is no travel time
            temp += clusterData['count'][j]
            continue 
        if math.isnan(thisCluster): continue # some clusters are outside of Atlanta
        thisTime = timeData.loc[(timeData['SourceBlockID'] == thisID)&(timeData['DestinationBlockID'] == thisCluster),['TravelTime']].values[0][0]
        thisValue = clusterData['count'][j]
        # print(thisCluster, thisTime, thisValue)
        temp += thisValue/(1+thisTime**2/3600) # use the unit as minute
    score[i] = temp

# print(score)
np.savetxt('../../data/' + score_dataset +'_score.csv', score, delimiter=",")