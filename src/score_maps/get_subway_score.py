import json
import numpy as np
import pandas as pd
import math
import pickle as pkl
from sklearn.preprocessing import normalize
import os

def find_n_closest_blocks(block_id, n):
    destination_blocks = timeData.loc[timeData['SourceBlockID'] == int(block_id)]
    # sort by travel time
    sorted_dst = destination_blocks.sort_values(by='TravelTime')
    # retrieve squares with subway stops
    blocks_w_stops = []

    # check if the block has a bus stop within itself
    # subtract one from count
    # will add in stop manually at end
    if subwaymap[str(block_id)]:
        n -= 1

    for i in sorted_dst['DestinationBlockID']:
        # use dict to check presence of subway stop in array
        if(subwaymap[str(i)] and n > 0):
            blocks_w_stops.append(i)
            n -= 1
        # stop once enough blocks with stops identified
        if(n == 0):
            break
    # print(blocks_w_stops)
    # return df containing closest blocks
    dists = sorted_dst.loc[sorted_dst['DestinationBlockID'].isin(blocks_w_stops)]

    if subwaymap[str(block_id)]:
        df_self = pd.DataFrame({"SourceBlockID":[block_id], "DestinationBlockID":[block_id], "TravelTime":60})
        dists = dists.append(df_self, ignore_index = True)

    return dists

def get_square_subway_score(block_id):
    n = 4
    n_closest = find_n_closest_blocks(block_id, n)
    score = 0
    # iterate through n closest and
    for dist in n_closest['TravelTime']:
        # add one to the denominator to prevent divide by zero error
        # this occurs
        score += 1 / (dist ** 2 + 3600)
    return score

def normalize_scores(raw_scores):
    mean_score = np.average((np.array(raw_scores, dtype=float)[:,1]))
    std_dev = np.std((np.array(raw_scores, dtype=float)[:,1]))

    norm_scores = []

    # normalize by maximum score
    for score in raw_scores:
        norm_scores.append([score[0], np.clip((score[1] - mean_score) / std_dev * 50 + 50, a_max=100, a_min=0)])

    # print(norm_scores)
    return norm_scores

if(not os.path.exists('../../data/raw_subway_scores.pkl')):
    with open('../../data/subway_map.json') as json_file:
        subwaymap = json.load(json_file)

        timeData = pd.read_csv("../../data/clean_WalkingTravelTimes.csv", )
        blockNum = len(subwaymap)

        # initialize scores arrays to hold
        raw_score = []

        # iterate through each block
        for i in subwaymap.keys():
            raw_score.append((i, get_square_subway_score(i)))

        # save raw score
        pkl.dump(raw_score, open('../../data/raw_subway_scores.pkl', 'wb'))

raw_score = pkl.load(open('../../data/raw_subway_scores.pkl', 'rb'))
print('Raw Score')
print(raw_score)

norm_scores = normalize_scores(raw_score)

print('Normalized Score')
print(norm_scores)
pkl.dump(norm_scores, open('../../data/normalized_subway_scores.pkl', 'wb'))
