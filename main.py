import pandas as pd
# import math
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from itertools import combinations
# from thefuzz import fuzz, process

# Get the df of the mexican trees
mexicanTreesDf = pd.read_csv('mexican_trees.csv')
print(mexicanTreesDf.head())

# # Count how many Species there are
# species = []
# for specie in mexicanTreesDf['SPECIES']:
#     if specie not in species:
#         species.append(specie)
#
# print(len(species))

# Check how many states are in the db
states = []
for state in mexicanTreesDf['STATE']:
    if state not in states:
        states.append(state)
print(states)

# Create a regions dataframe
regionsDf = pd.DataFrame(states, columns=['STATE'])

# Create regions
northWestRegion = ['Baja California', 'Baja California Sur', 'Chihuahua',
                   'Durango', 'Sinaloa', 'Sonora']
northEast = ['Coahuila', 'Nuevo León', 'Tamaulipas']
west = ['Colima', 'Jalisco', 'Michoacán', 'Nayarit']
east = ['Hidalgo', 'Puebla', 'Tlaxcala', 'Veracruz']
northCenter = ['Aguascalientes', 'Guanajuato', 'Querétaro', 'San Luis Potosí',
               'Zacatecas']
southCenter = ['Ciudad de México', 'México', 'Morelos']
southWest = ['Chiapas',  'Guerrero', 'Oaxaca']
southEast = ['Campeche', 'Quintana Roo', 'Tabasco', 'Yucatán']

