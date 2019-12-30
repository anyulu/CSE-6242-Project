import pandas as pd 
import math

data = pd.DataFrame(columns = ['SourceBlockID', 'DestinationBlockID', 'TravelTime'])
for i in range(25):
    ix = math.ceil((i+1)/5)
    iy = (i+1)%5 if (i+1)%5 !=0 else 5
    print(i,ix,iy)
    for j in range(25):
        jx = math.ceil((j+1)/5)
        jy = (j+1)%5 if (j+1)%5 !=0 else 5
        data = data.append({'SourceBlockID': i+1,
                'DestinationBlockID': j+1,
                'TravelTime': (ix-jx)**2 + (iy-jy)**2}, ignore_index = True)

data.to_csv('../../data/sampleTime.csv', sep=',', index = False)