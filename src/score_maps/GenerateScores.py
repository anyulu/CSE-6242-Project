import json
import numpy as np
import pandas as pd
import math
import pickle as pkl
from gen_atl_map_ids import get_square_ids

square_ids = get_square_ids()
square_id_dict = {}
for i in square_ids:
	id = i[0]
	bottom_left_lat = i[1][0][0]
	bottom_left_long = i[1][0][1]
	top_left_lat = i[1][1][0]
	top_left_long = i[1][1][1]
	top_right_lat = i[1][2][0]
	top_right_long = i[1][2][1]
	bottom_right_lat = i[1][3][0]
	bottom_right_long = i[1][3][1]
	lat_list = [bottom_left_lat, top_left_lat, top_right_lat, bottom_right_lat]
	long_list = [bottom_left_long, top_left_long, top_right_long, bottom_right_long]
	square_id_dict[id] = (lat_list, long_list)

# print(square_id_dict)

rest_score = np.loadtxt(open("../../data/restaurant_score.csv", "rb"), delimiter=",")
crime_score = np.loadtxt(open("../../data/crime_score.csv", "rb"), delimiter=",")
bus_score = np.loadtxt(open("../../data/busmap_scores.csv", "rb"), delimiter=",")
subway_score = pkl.load(open('../../data/normalized_subway_scores.pkl', 'rb'))
park_score = np.loadtxt(open("../../data/parks_score.csv", "rb"), delimiter=",")
scores = {}
scores["scores"] = []
#print(subway_score)
rest_mean = np.mean(rest_score)
rest_dev = np.std(rest_score)
crime_mean = np.mean(crime_score)
crime_dev = np.std(crime_score)
park_mean = np.mean(park_score)
park_dev = np.std(park_score)
for i in range(65):
	for j in range(65):
		ID = i * 66 +j+1
		index = i * 65 +j
		scores["scores"].append({
			# "id": str(ID),
			"lat": square_id_dict[str(ID)][0],
			"long": square_id_dict[str(ID)][1],
			"bus_score": bus_score[i,j],
			"park_score": np.clip((park_score[index] - park_mean) / park_dev * 50 + 50, a_max=100, a_min=0),
			"subway_score": subway_score[index][1],
			"restaurant_score": np.clip((rest_score[index] - rest_mean) / rest_dev * 50 + 50, a_max=100, a_min=0),
			"crime_score":np.clip((crime_score[index] - crime_mean) / crime_dev * 50 + 50, a_max=100, a_min=0)
			})

with open('../../data/combined_scores.json', 'w') as output_file:
    json.dump(scores, output_file)
