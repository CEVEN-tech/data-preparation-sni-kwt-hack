import pandas as pd
import numpy as np
import json

pathCounties = "monthly_state.json"
path_eDNA = "41467_2016_BFncomms12544_MOESM1319_ESM.xlsx"

# json
with open(pathCounties, 'r') as countries_file:
    zones_data = json.load(countries_file)

zones = zones_data['data']['countries'].keys()
numOfZones = len(zones)

# pandas
df = pd.read_excel(path_eDNA, header=1)
numMaxSpecies = len(df.index)
# countries times copy of df
dfForEachZone = [df.copy() for _ in range(numOfZones)]

# each copy replacement of values in one of the following columns
colsToBeManipulated = [
    'Number of Sequences',
    'Average of % of identical matches',
    'Average reference alignment length'
]

datetimes = [
    "2021-08-01T00:00:00Z",
    "2021-09-01T00:00:00Z",
    "2021-10-01T00:00:00Z",
    "2021-11-01T00:00:00Z",
    "2021-12-01T00:00:00Z",
    "2022-01-01T00:00:00Z",
    "2022-02-01T00:00:00Z",
    "2022-03-01T00:00:00Z",
    "2022-04-01T00:00:00Z",
    "2022-05-01T00:00:00Z",
    "2022-06-01T00:00:00Z",
    "2022-07-01T00:00:00Z",
    ]

numOfDatetimes = len(datetimes)

# make list of each column, this lists can be used to sample and generate randomised data
numOfSeqList = df[colsToBeManipulated[0]].tolist()
avgPercOfIdenticalMatches = df[colsToBeManipulated[1]].tolist()
avgRefAlignmentLength = df[colsToBeManipulated[2]].tolist()

# in each zone are only the species present that were not sampled twice or more from U[0,n-1] n=numOfSpeciesOriginalSample
# high sizeForSampling results in large pseudo samples, low sizeForSampling results in small pseudo samples
# sizeForSampling = round(np.random.uniform(low=0, high=numMaxSpecies))
# print(sizeForSampling)
# matrixWithDuplicates = np.random.uniform(low=0, high=numMaxSpecies-1, size=(numOfZones, numOfDatetimes, sizeForSampling)).round()
# need a tensor
# 3rd dimension (most inner) is selection of samples for one month in one zone 
# 2nd dim is for 12 months
# 1st dim is for 400+ zones

# print([len(matrixWithDuplicates[i][j]) for j in range(numOfDatetimes) for i in range(numOfZones)])
# matrixWithDuplicates.shape >> (407, 255)

numOfSequences = np.random.choice(numOfSeqList,size=(numOfZones, numOfDatetimes, numMaxSpecies))
avgPercOfIdenticalMatchesSampled = np.random.choice(avgPercOfIdenticalMatches,size=(numOfZones, numOfDatetimes, numMaxSpecies))
avgRefAlignmentLengthSampled = np.random.choice(avgRefAlignmentLength,size=(numOfZones, numOfDatetimes, numMaxSpecies))

# from here repeat this action for 407 zones
# for each create 
# 1) randomised data
# 2) write to json file
# 3) create folder for each zone
# 4) save json file to this folder

# replace "DE" with zones
# replace with for i, zone in enumerate(zones):
for i, zone in enumerate(zones):
    print(i, zone)
    toBeJson = {
        "data": {
            "hasData":True,
            "stateAggregation":"monthly",
        }
    }

    zoneStates = []

    for j, stateDatetime in enumerate(datetimes):
        # drop duplicates, non-duplicates emulate sampled species
        sizeForSampling = round(np.random.uniform(low=0, high=numMaxSpecies))
        matrixWithDuplicates = np.random.uniform(low=0, high=numMaxSpecies-1, size=(sizeForSampling)).round()
        # hope that df is not drained via multiple drop rounds but original persists
        # print(matrixWithDuplicates[i][0:3])
        dfPseudoSampledSpecies = dfForEachZone[i].drop(matrixWithDuplicates, inplace=False) #.drop_duplicates()

        # draw from existing values e.g numOfSeqList, dimensions numSpeciesForZoneA x 1
        
        # replace the original data columns with randomised data

        dfPseudoSampledSpecies[colsToBeManipulated[0]] = pd.Series(numOfSequences[i][j])
        dfPseudoSampledSpecies[colsToBeManipulated[1]] = pd.Series(avgPercOfIdenticalMatchesSampled[i][j])
        dfPseudoSampledSpecies[colsToBeManipulated[2]] = pd.Series(avgRefAlignmentLengthSampled[i][j])

        # make for each df (ie. each zone) a json
        #dfPseudoSampledSpecies['json'] = dfPseudoSampledSpecies.apply(lambda x: x.to_json(), axis=1)
        #dfPseudoSampledSpecies['json'].tolist()
        
        speciesListForJson = dfPseudoSampledSpecies.apply(lambda x: x.to_dict(), axis=1).values.tolist()

        zoneState = {
            "_isFinestGranularity": True,
            "countryCode": zone,
            "treeOfLifeCovered": np.random.uniform(),
            "isValid": True,
            "endemicRatio": np.random.uniform(),
            "stateDatetime": stateDatetime,
            "discoveredSpecies": speciesListForJson
        }
        zoneStates.append(zoneState)
   
    toBeJson["data"]["zoneStates"] = zoneStates
    #json.dumps(toBeJson, sort_keys=True, indent=4)
    path = "public/v5/history/" + zone + "/monthly.json"
    
    # todo: create folders <--------
    path = "test.json"
    with open(path, 'x') as historyFile:
        json.dump(toBeJson, historyFile, indent=4)

# create a folder and a json file for each zone
# public/v5/history/zoneId/monthly.json

# perhaps work inside electricity maps repo
# create pyenv inside history folder for data generation