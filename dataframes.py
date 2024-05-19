import pandas as pd
from Costo import Cost
# import math
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from itertools import combinations
# from thefuzz import fuzz, process

# Function to get all the states in the main dataframe
# NOTE: mainDataFrame MUST be a dataframe
def get_df_states(mainDataFrame):
    # Check how many states are in the db
    statesList = []
    for element in mainDataFrame['STATE']:
        if element not in statesList:
            statesList.append(element)  # Store the element in the statesList

    # Return type is a list
    return statesList

# Function to create a list with the regions of the states
# NOTE: the parameter MUST be a list with the states in the main df
def create_regions_list(states_list):
    # Create the regions list to store every state region
    regsList = []

    # Iterate over the states to find their region
    for i in states_list:
        foundRegion = None

        for x, y in regionsDict.items():
            if i in y:
                foundRegion = x
                break

        regsList.append(foundRegion)  # Store the region

    # Return datatype is a list
    return regsList

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

# Function to add the regions to the main df
# NOTE: first parameter must be the main dataframe, second must be the states list
# And third parameter must be a regions list
def add_regions(mainDataFrame, statesList, regionsList):
    # Create a df of only the states
    onlyStatesDf = pd.DataFrame(statesList, columns=['STATE'])
    # Create a df of only the regions
    onlyRegionsDf = pd.DataFrame(regionsList, columns=['REGION'])

    # Concat both of the previous df into one
    regionsDf = pd.concat([onlyStatesDf, onlyRegionsDf], axis=1)

    # Merge the original DataFrame with the regions DataFrame on the 'STATE' column
    mainDataFrame = pd.merge(mainDataFrame, regionsDf, on='STATE', how='left')

    # Return type is a dataframe
    return mainDataFrame

# Get the df of the mexican trees
mexicanTreesDf = pd.read_csv('mexican_trees.csv')

# Get the states list
states = get_df_states(mexicanTreesDf)

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

# Create the regions list
regions = create_regions_list(states)

# Add the regions to the main dataframe
mexicanTreesDf = add_regions(mexicanTreesDf, states, regions)

# Implement function get_top_five
topFiveTrees = get_top_five(mexicanTreesDf, 'Durango', 'Northwest')

# Iterate in the top 5 to print them 1 by 1
for i in range(len(topFiveTrees)):
    print(f'The option {i + 1} is: {topFiveTrees[i]}')

# Implement the Cost class
estimatedCost = Cost('Durango', 456) # Let's assume we are working again with Durango state

# Ask user for the infrastructure
estimatedCost.setInfrastructure()
# Calculate the estimated cost
estimatedCost = estimatedCost.calculate()
print(estimatedCost) # Print the estimated cost