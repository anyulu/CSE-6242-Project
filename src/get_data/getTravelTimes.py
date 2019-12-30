import http.client
import json
import csv
import time

# tutorial: https://blog.traveltimeplatform.com/distance-matrix-tutorial-calculate-times-to-multiple-locations

# This script downloads the travel times from all blocks listed in the "locations" array in TravelTimesDataTemplate.json in the data directory
# to all other blocks in that array. We have 65 * 65 = 4,255 blocks, hence this script produces a large CSV file with 4,255 * 4,255 = 18,105,025‬ rows

# How to use: Add all 4,255 blocks into TravelTimesDataTemplate.json, then run this script. The script will then make the appropriate API calls automatically.
# The travel time API allows 10,000 calls per month in the free tier and the script makes one API call to get the distances from each block to ALL OTHER blocks.
# So for 4,255 blocks we make 4,255 calls and you get about two chances to run this script with the full blocks data.

# Date: 11/06/2019
# Author: Benjamin Du Preez

walking = False

# build authorization header
app_id = "YOUR APP ID HERE"
key = "YOUR API KEY HERE"
headers = { 'X-Api-Key' : key, 'X-Application-Id': app_id, 'Content-type': 'application/json', 'Accept': 'application/json'}
# create connection
connection = http.client.HTTPSConnection("api.traveltimeapp.com")

# write all the processed tracks to a json file
with open('../../data/TravelTimes.csv', 'a', newline='') as outfile:
	csv_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	csv_writer.writerow(["SourceBlockID", "DestinationBlockID", "TravelTime"])
	
	# get template request body
	with open('../data/TravelTimesDataTemplate.json') as json_file:

		print("Please be patient, this might take a while :)")

		json_body = json.load(json_file)

		# read from TravelTimesDataTemplate.json
		all_locations = json_body["locations"].copy() # all the locations
		block_ids = list(map(lambda block: block["id"], all_locations)) # all the ids of those locations
		num_blocks = len(block_ids) # for us this will be 4,356

		group1End = int(len(block_ids)/3)
		group2End = int(2*len(block_ids)/3)
		group3End = len(block_ids)

		# split locations id's into 3 groups
		group1 = block_ids[0:group1End]
		group2 = block_ids[group1End:group2End]
		group3 = block_ids[group2End:group3End]
		groups = [group1, group2, group3]

		# split locations into 3 groups
		location_group1 = all_locations[0:group1End]
		location_group2 = all_locations[group1End:group2End]
		location_group3 = all_locations[group2End:group3End]

		location_groups = [location_group1, location_group2, location_group3]

		# for each source
		for i in range(0, 2500): # TODO: change the start and end index of this loop to limit

			source = block_ids[i] # the current source block in our upcoming one-to-many travel time query

			# add the source into the json body as the source of our query
			json_body["departure_searches"][0]["departure_location_id"] = source

			# holds the result of the one-to-many search of the source block
			results = []

			# for this source make a separate query for each destination group
			for j in range(0, len(groups)):

				destination_ids = groups[j].copy()

				# only add the locations from the current destination group to the locations list for the query
				locations_list = location_groups[j].copy()

				# if the source is in the current destinations group -> remove it
				if source in destination_ids:
					destination_ids.remove(source)
				else: # if the source is not in the current destination id's it is also not in the locations group -> add it to the locations list
					locations_list.append(all_locations[i])

				# add the locations list, which holds all the destinations and the source to the query
				json_body["locations"] = locations_list

				json_body["departure_searches"][0]["arrival_location_ids"] = destination_ids

				if(walking):
					json_body["departure_searches"][0]["transportation"] = {"type": "walking"}

				start_time = time.time() # use this to throttle requests so we don't exceed the free tier

				connection.request("POST", "/v4/time-filter", json.dumps(json_body), headers)
				temp = json.loads(connection.getresponse().read())
				#print(temp)
				results += temp["results"][0]["locations"]			

				# get the time elapsed in seconds since we made the previous api call
				time_elapsed = time.time() - start_time

				# make sure we don't do more than 30 calls a minute to stay in the free tier
				if time_elapsed < 6:
					time.sleep(6 - time_elapsed)

			print(str(round(i / num_blocks * 100, 2)) + "%")
			num_results = len(results)

			# append the driving time to the csv file, each row represents the travel time (in seconds) from the block
			# corresponding to the id in the first column to the block with id in the second
			for j in range(0, num_results):
				# put the travel time to other blocks in the right format to write to file source,dest,travel_time
				row = []
				row.append(source)
				row.append(results[j]["id"])
				row.append(results[j]["properties"][0]["travel_time"])
				csv_writer.writerow(row)
				

			#print(results)

	print("Done. Results written to ../data/TravelTimes.csv")
