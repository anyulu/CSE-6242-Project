import numpy as np
import pandas as pd
import math
import json
from sklearn.cluster import DBSCAN

earth_radius_km = 6378.137 #kilometers

bottom_left_lat = 33.718139
bottom_left_long = -84.440371
top_left_lat = 33.789353
top_left_long = -84.440371
bottom_right_lat = 33.718139
bottom_right_long = -84.332289
top_right_lat = 33.789353
top_right_long = -84.332289

#500 feet = 0.1524 km
km_to_feet = 3280.84 # 1 km = 3280.84 feet
earth_radius_ft = earth_radius_km * km_to_feet

new_latitude = bottom_left_lat
new_longitude = bottom_left_long

lat_list = []
long_list = []

while new_latitude < top_right_lat or new_longitude < top_right_long:
    new_latitude = new_latitude + (500 / earth_radius_ft) * (180 / math.pi)
    new_longitude = new_longitude + (500 / earth_radius_ft) * (180 / math.pi) / math.cos(new_latitude * math.pi / 180)
    lat_list.append(new_latitude)
    long_list.append(new_longitude)

# get latitude, longitude of bottom left corner of each square on the grid
coord_list = []
for lat in lat_list:
    for long in long_list:
        coord_list.append([lat, long])

lat_count = 0
long_count = 0
squares = []
while lat_count < len(lat_list) - 1:
    bottom_left = lat_list[lat_count], long_list[long_count]
    top_left = lat_list[lat_count + 1], long_list[long_count]
    top_right = lat_list[lat_count + 1], long_list[long_count + 1]
    bottom_right = lat_list[lat_count], long_list[long_count + 1]
    squares.append((bottom_left, top_left, top_right, bottom_right))
    long_count += 1
    if long_count == len(long_list) - 1:
        lat_count += 1
        long_count = 0

with open('../../data/locations.json') as input_file:
    location_data = json.load(input_file)

locations = {}
locations['locations'] = []
square_ids = []
for square in squares:
    for i in range(len(location_data['locations'])):
        lat = location_data['locations'][i]['coords']['lat']
        long = location_data['locations'][i]['coords']['lng']
        id = location_data['locations'][i]['id']

        if square[0][0] == lat and square[0][1] == long:
            new_id = id

    square_ids.append((new_id, square))
    locations['locations'].append({
        "id": str(new_id),
        "coords": {"lat": square[0][0], "lng": square[0][1]}})

# save location file
with open('../../data/locations_v2.json', 'w') as output_file:
    json.dump(locations, output_file)

def get_square_ids():
    return square_ids
