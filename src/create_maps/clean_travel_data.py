import pandas as pd

# clean walking data
timeData = pd.read_csv("../../data/WalkingTravelTimes.csv")
ids_to_drop = pd.read_csv("../../data/dropIDs.csv", header=None).values.flatten()

removeSrc = timeData[~timeData['SourceBlockID'].isin(ids_to_drop)]
clean_df = removeSrc[~removeSrc['DestinationBlockID'].isin(ids_to_drop)]

clean_df.to_csv("../../data/clean_WalkingTravelTimes.csv", index=False)

# clean driving time
timeData = pd.read_csv("../../data/TravelTimes.csv")
ids_to_drop = pd.read_csv("../../data/dropIDs.csv", header=None).values.flatten()

removeSrc = timeData[~timeData['SourceBlockID'].isin(ids_to_drop)]
clean_df = removeSrc[~removeSrc['DestinationBlockID'].isin(ids_to_drop)]

clean_df.to_csv("../../data/clean_TravelTimes.csv", index=False)