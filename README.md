# CSE 6242 Project: LivingSpace

## Overview

Directory Structure  
|- LivingSpace/  
|-- data/  
|
|-- src/  
|--- get_data/  
|--- create_maps/  
|--- score_maps/  
|--- debug/  
|- LivingSpaceFrontend/

Backend Scripts Contents
src/create_maps:
	DropIDs.py
	clean_travel_data.py
	gen_atl_map_ids.py
	gen_busmap.py
	gen_subwaymap.py

src/debug:
	generateSample.py
	loadData.py
	plot_points.py
	verify_bus_stop.py
	verify_crime.py
	verify_restaurant.py
	verify_subway_stop.py
	visualizeClusterData.py

src/get_data:
	getTravelTimes.py
	get_yelp_data.py

src/score_maps:
	GenerateScores.py
	get_bus_score.py
	get_parks_score.py
	get_score_crime.py
	get_score_restaurants.py
	get_subway_score.py
	score_map_by_cluster.py

Frontend Contents
	combined_scores.json
	index.html
	scripts.js
	styles.css

The process to generate the visualization occurs in the following stages:
1. Data Collection
2. Map Generation
3. Scoring the Data
4. UI Representation

Each stage is manually run, and generates their own data files for the next stage to use. Future iterations of this process will have this pipeline run automatically and possible real-time updates as the data changes along with Atlanta.

## Script Execution Order

1. Gather Data
    get_yelp_data.py
    getTravelTimes.py x2
        Once for walking time
        Once for driving time
2. Generate Map
    gen_atl_map_ids.py
3. Clean Travel Data
     clean_travel_data.py
     Driving, Walking Time
4. Generate Boolean maps for subways, bus stops, and parks
    gen_busmap.py
    gen_subwaymap.py x2
        Once for subways
        Once for parks
5. Run scoring for sparse datasets
    get_bus_score.py
    get_subway_score.py x2
        Subway and park scores
6. Run clustering and scoring for dense datasets
    score_map_by_cluster.py x2
        Once for restaurants
        Once for crime
7. Combine scores
    GenerateScores.py

## Dependencies
Install Python dependencies using Anaconda:
conda install --file package_list.txt


## Data Collection

### 1. Bus, Subway, Restaurants etc

#### get_yelp_data.py

This script extracts the information(name, longtitude, latitude) of all restaurants in Atlanta. These information are gotten from Yelp Fusion API call. Input parameters are sets as terms:"parks", longitude and latitude are based on location of Atlanta with grid size of 700 feet, and radius of 150 meters.

This was then adapted to collect data on parks by modifying the parameters of the API call.

How to use: Get an API key first, and use the key as the system input and run the script.

Input:
Yelp API Key

Output:
data/restaurants-data.csv
data/parks.csv

### 2. Travel Times

#### getTravelTimes.py

This script downloads the driving times in seconds from all squares listed in the "locations" array in TravelTimesDataTemplate.json in the data directory to all other squares in that array. The output format is: src,dst,time

We have 65 * 65 = 4,255 blocks, hence this script produces a large CSV file with 4,255 * 4,255 = 18,105,025‬ rows. The output file is several hundreds of MBs and too large to store on Github.

How to use: Add all 4,255 blocks into TravelTimesDataTemplate.json, then run this script. The script will then make the appropriate API calls automatically. The code sleeps in between API calls to remain in the free tier. We also had to make 3 API calls for each source square, instead of just 1, in order to stay within the free tier limits. With all this taken into account, the estimated total running time of this script is about 20 hours.
            Get an API key [here](https://docs.traveltimeplatform.com/overview/getting-keys), and paste your userId and key into the spots noted in the code. Specify mode of travel in the script and output filename to generate differing data files for each

Input:
TravelTime Username, API Key
API Call Parameters: 
`json_body["departure_searches"][0]["transportation"] = {"type" : "<TransportType>"}`

Output:
data/TravelTime.csv
data/WalkingTravelTime.csv

#### clean_travel_data.py
In case it becomes necessary to trim the collected data from the previous scipt, we can run this one to drop IDs from the original CSV. For the original problem, the IDs were generated as JSONs and thus, we opted to clean the travel time data in this way to non-intrusively clean the existing data files. Downstream scripts were then re-pointed at these cleaned datafiles.

How to use: Change the input and output files within the script to match the data file locations and run script

Input:
data/dropIDs.csv
data/TravelTime.csv
data/WalkingTravelTime.csv

Output:
data/clean_TravelTime.csv
data/clean_WalkingTravelTime.csv
## Generating Maps

### grid.py

Given four corners in (Latitude, Longitude) format and size of grids, this script generates an indexed list of grids that will be used by the downstream scripts

How to use: Set input parameters below. Then run script to generate the requisite locations data file

Input:
Four corners of map
Size of square desired

Output:
data/locations_v2.json

### gen_busmap.py

Reads in raw data of bus stops using latitudes and longitudes and outputs a subway_map.json file that displays which squares in the grid of Atlanta have a bus stop.
How to use: Place the requisite data files in the data directory and run the script to generate the Boolean bus map

Input:
data/locations_v2.json
data/busstop.csv

Output:
data/busstop_map.json

### gen_subwaymap.py

Reads in raw data of subway (MARTA) locations using latitudes and longitudes and outputs a subway_map.json file that displays which squares in the grid of Atlanta have a subway stop.
How to use: Place the requisite data files in the data directory and run the script to generate the Boolean bus map

Input:
data/locations_v2.json
data/subway.csv


Output:
data/subway_map.json

## Scoring the Data

### 1. Calculating Scores for Each Input

#### get_bus_score.py / get_subway_score.py / get_parks_score.py

This takes in the previously generated bus map and iterates through each square in the overall map and assigns it a score based on the sum of its inverse squared distance to the closest 3 bus stops by walking time. Squares with stops inside it may cause divide by zero, so a bias of 3600 (representing 1 minute travel time) was added.

How to use: Place the requisite data files in the data directory and run the script to generate map scores indexed by ID

Input:
data/busstop_map.json or
data/subway_map.json or
data/park.csv

Output:
normalized_busmap_scores.pkl or
normalized_subway_scores.pkl or
parks_count.csv

### get_score.py
The input of this script is the travelling time between each square, and the count of each cluster. The script will calculate the score of each grid. The score function is the sum of the count of each cluster divided by the square of travelling time between this grid and the cluster center. 

How to use: Specify which travel metric dataset will be used and which dataset (restaurant/crime) will be used for scoring. Run the script, allowing approximately 21 hours for each.

Input:
data/TravelTimes.csv or
data/WalkingTravelTimes.csv
data/<data>_count.csv

Output:
data/<data>_score.csv

### score_crime.py / score_restaurants.py

These scripts cluster and score the crime and restaurant datasets. The DBScan hyperparameters were chosen in a way that effectivlely separates out clusters without pre-defining them. This should be manually validated by plotting centroids out before proceeeding. These produce the raw scores for each square, 

Input:
DBScan Hyperparameters
    Epsilon
    Minimum samples

data/crime-data.csv or
data/restaurant-data.csv

Output:
data/crime_count.csv or
data/restaurant_count.csv

### 2. Combining the scores to a single JSON data array to pass to the frontend

#### GenerateScores.py

This script takes all the scores calculated by the previous steps and packages it into a JSON file readable by the frontend.

Input:
data/restaurant_score.csv
data/crime_score.csv
data/busmap_scores.csv
data/normalized_subway_scores.pkl
data/parks_score.csv

Output:
data/combined_scores.jso


## Frontend

The frontend code can be found in this repository: https://github.com/benjamindupreez/LivingSpaceFrontend/. This frontend visualizes the final output by using D3.js alongside the Leaflet mapping library.

## Running Instructions
To run locally:
1. Clone the frontend repository
2. Install Python
3. Host a local server using the command 'python -m http.server <port_number>'
4. Open your browser at http://localhost:<port_number>/

## Live Online Demo
http://benjamindupreez.com/living-space/
