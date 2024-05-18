import pandas as pd
# import math
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from itertools import combinations
# from thefuzz import fuzz, process

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
    'Southwest': ['Chiapas',  'Guerrero', 'Oaxaca'],
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

regionsDf = pd.concat([onlyStatesDf, onlyRegionsDf], axis=1)
print(regionsDf)