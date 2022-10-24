import pandas as pd
import numpy as np
import json

pathCounties = "monthly.json"
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
dfForEachZone = [df.copy for _ in range(numOfZones)]

# each copy replacement of values in one of the following columns
colsToBeManipulated = [
    'Number of Sequences',
    'Average of % of identical matches',
    'Average reference alignment length'
]
# make list of each column
numOfSeqList = df[colsToBeManipulated[0]].tolist()
avgPercOfIdenticalMatches = df[colsToBeManipulated[1]].tolist()
avgRefAlignmentLength = df[colsToBeManipulated[2]].tolist()
# in each zone are only the species present that were not sampled twice or more from U[0,n-1] n=numOfSpeciesOriginalSample
matrixWithDuplicates = np.random.uniform(low=0, high=numMaxSpecies-1, size=(numOfZones, numMaxSpecies)).round()
print(matrixWithDuplicates)
# df.drop([0, 1])
# for each zone (ie. df) get sampled species
# i = 1
# dfForEachZone = [df.drop(matrixWithDuplicates[i], inplace=False) for i, df in enumerate(dfForEachZone)]
# dfForEachZone = [df.removeDuplicated(axis=0) for df in dfForEachZone]

dfPseudoSampledSpecies = df.drop(matrixWithDuplicates[0], inplace=False).drop_duplicates()
print(dfPseudoSampledSpecies)
numSpeciesForZoneA = len(dfPseudoSampledSpecies.index)
# draw from existing values e.g numOfSeqList, dimensions numSpeciesForZoneA x 1
# replace the column of 'Number of Sequences'


numOfSequences = np.random.choice(numOfSeqList,size=numMaxSpecies)
dfPseudoSampledSpecies[colsToBeManipulated[0]] = pd.Series(numOfSequences)

avgPercOfIdenticalMatchesSampled = np.random.choice(avgPercOfIdenticalMatches,size=numMaxSpecies)
dfPseudoSampledSpecies[colsToBeManipulated[1]] = pd.Series(avgPercOfIdenticalMatchesSampled)

avgRefAlignmentLengthSampled = np.random.choice(avgRefAlignmentLength,size=numMaxSpecies)
dfPseudoSampledSpecies[colsToBeManipulated[2]] = pd.Series(avgRefAlignmentLengthSampled)

# do this for all dfs
# make each df a json, and put all jsons into a big json

# make for each df (ie. each zone) a json
df['json'] = df.apply(lambda x: x.to_json(), axis=1)
# print(df['json'].tolist()[0])