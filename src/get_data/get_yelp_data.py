import requests
import pandas as pd
import numpy as np
import pprint
import sys

### Refer to this website to get the info of params: 
### https://www.yelp.com/developers/documentation/v3/business_search

offset = 0
data = pd.DataFrame(columns=['name', 'latitude', 'longitude'])
api_key = sys.argv[1]
url = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'Bearer %s' %api_key}
#[33.753746, -84.38633]
# list are in range of 700 feet (213 meters)
latitude_list = [33.720055645428864, 33.72197229085773, 33.72388893628659, 33.725805581715456, 33.72772222714432, 33.72963887257318, 33.73155551800205, 33.73347216343091, 33.735388808859774, 33.73730545428864, 33.7392220997175, 33.741138745146365, 33.74305539057523, 33.74497203600409, 33.74688868143296, 33.74880532686182, 33.750721972290684, 33.75263861771955, 33.75455526314841, 33.756471908577275, 33.75838855400614, 33.760305199435, 33.762221844863866, 33.76413849029273, 33.766055135721594, 33.76797178115046, 33.76988842657932, 33.771805072008185, 33.77372171743705, 33.77563836286591, 33.777555008294776, 33.77947165372364, 33.7813882991525, 33.78330494458137, 33.78522159001023, 33.787138235439095, 33.78905488086796, 33.79097152629682, 33.792888171725686, 33.79480481715455, 33.79672146258341, 33.79863810801228, 33.80055475344114, 33.802471398870004, 33.80438804429887, 33.80630468972773, 33.808221335156595]
longitude_list = [-84.43806667451807, -84.43576229758622, -84.43345786919959, -84.43115338935327, -84.42884885804241, -84.42654427526213, -84.42423964100755, -84.42193495527378, -84.41963021805596, -84.41732542934919, -84.41502058914861, -84.41271569744933, -84.41041075424646, -84.40810575953513, -84.40580071331046, -84.40349561556756, -84.40119046630156, -84.39888526550756, -84.3965800131807, -84.39427470931606, -84.39196935390879, -84.38966394695399, -84.38735848844678, -84.38505297838228, -84.38274741675558, -84.38044180356181, -84.3781361387961, -84.37583042245353, -84.37352465452923, -84.37121883501831, -84.36891296391589, -84.36660704121707, -84.36430106691695, -84.36199504101066, -84.3596889634933, -84.35738283435998, -84.3550766536058, -84.35277042122588, -84.35046413721533, -84.34815780156924, -84.34585141428275, -84.34354497535094, -84.34123848476891, -84.33893194253179, -84.33662534863466, -84.33431870307264, -84.33201200584084]
for thisLatitude in latitude_list:
    for thisLongitude in longitude_list:
        for i in range(20):
            offset = 50*i
            params = {'term': 'food',
                      'limit': 50,
                      'offset': offset,
                      'latitude': thisLatitude,
                      'longitude': thisLongitude,
                      'radius': 150 # 150*sqrt(2) = 212 
                      }
            resp = requests.get(url=url, params=params, headers=headers)
            #pprint.pprint(resp.json())
            temp = resp.json()['businesses']
            #print(resp.json()['total'])
            for j in range(len(temp)):
                data = data.append({'name': temp[j]['name'], 'latitude': temp[j]['coordinates']['latitude'],
                          'longitude': temp[j]['coordinates']['longitude']}, ignore_index = True)
            if resp.json()['total']  < 50: break
            elif resp.json()['businesses'] == []: break
data.drop_duplicates(subset =['name', 'latitude', 'longitude'], keep = 'first')
data.to_csv('../../data/restaurants-data.csv', sep=',', index = False)