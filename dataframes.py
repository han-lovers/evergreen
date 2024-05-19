import pandas as pd
# import math
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from itertools import combinations
# from thefuzz import fuzz, process

# Function to get the top five trees from a specific region
# NOTE: The first parameter MUST be the main dataframe, second and third parameters
# MUST be strings and fourth and fifth parameters are optional
def get_top_five(mainDataFrame, state, region, dataFrameRegion='REGION', dataFrameState='STATE'):
    # Look for the trees in a specific region and state
    specificZoneTrees = mainDataFrame.loc[
        (mainDataFrame[dataFrameRegion] == region) & (mainDataFrame[dataFrameState] == state)]
    # Get the top 5 trees in a specific region and state
    topFiveTrees = (specificZoneTrees['SPECIES'].value_counts()).head()
    topFiveTrees = topFiveTrees.index.to_list()  # Transform the values into a list with the Species

    # Return type is a list
    return topFiveTrees


# Get the df of the mexican trees
mexicanTreesDf = pd.read_csv('mexican_trees.csv')

# Check how many states are in the db
states = []
for state in mexicanTreesDf['STATE']:
    if state not in states:
        states.append(state) # Store the states in states list

# Create regions dictionary
regionsDict = {
    'Northwest': ['Baja California', 'Baja California Sur', 'Chihuahua',
                   'Durango', 'Sinaloa', 'Sonora'],
    'Northeast': ['Coahuila', 'Nuevo León', 'Tamaulipas'],
    'West': ['Colima', 'Jalisco', 'Michoacán', 'Nayarit'],
    'East': ['Hidalgo', 'Puebla', 'Tlaxcala', 'Veracruz'],
    'Northcenter': ['Aguascalientes', 'Guanajuato', 'Querétaro', 'San Luis Potosí',
               'Zacatecas'],
    'Southcenter': ['Ciudad de México', 'México', 'Morelos'],
    'Southwest': ['Chiapas', 'Guerrero', 'Oaxaca'],
    'Southeast': ['Campeche', 'Quintana Roo', 'Tabasco', 'Yucatán']
}

# Create the regions list to store every state region
regions = []

# Iterate over the states to find their region
for state in states:
    foundRegion = None

    for region, statesList in regionsDict.items():
        if state in statesList:
            foundRegion = region
            break

    regions.append(foundRegion) # Store the region

# Create a df of only the states
onlyStatesDf = pd.DataFrame(states, columns=['STATE'])
# Create a df of only the regions
onlyRegionsDf = pd.DataFrame(regions, columns=['REGION'])

# Concat both of the previous df into one
regionsDf = pd.concat([onlyStatesDf, onlyRegionsDf], axis=1)

# Merge the original DataFrame with the regions DataFrame on the 'STATE' column
mexicanTreesDf = pd.merge(mexicanTreesDf, regionsDf, on='STATE', how='left')

# Implement function get_top_five
topFiveTrees = get_top_five(mexicanTreesDf, 'Durango', 'Northwest')

# Iterate in the top 5 to print them 1 by 1
for i in range(len(topFiveTrees)):
    print(f'The option {i + 1} is: {topFiveTrees[i]}')
