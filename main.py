import streamlit as st
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import geodesic
import requests
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from thefuzz import fuzz, process

# Inicializar geocodificador
geolocator = Nominatim(user_agent="pruebas")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=2)


def funcionDistancia(location1, location2):
    location2_coords = tuple(map(float, location2.split(", ")))
    distancia = geodesic(location1, location2_coords).kilometers
    return distancia


def obtener_estado(location):
    address = location.raw['address']
    estado = address.get('state', 'No encontrado')
    return estado


diccionarioEstados = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua",
                      "Ciudad de México", "Coahuila", "Colima", "Durango", "Estado de México", "Guanajuato",
                      "Guerrero", "Hidalgo", "Jalisco", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca",
                      "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco",
                      "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"]

st.title('Encuentra la región más cercana')

option = st.radio("Elige el método de entrada:", ('Dirección', 'Coordenadas'))

stringDireccion = ""

try:
    if option == 'Dirección':
        location1_name = st.text_input("Ingresa tu dirección:")
        if location1_name:
            location1 = geolocator.geocode(location1_name)
            if not location1:
                st.error("Ubicación no encontrada. Intenta usar coordenadas.")
                st.stop()
            location1_coords = (location1.latitude, location1.longitude)
            st.write(f"Coordenadas de la ubicación ingresada: {location1_coords}")
            stringDireccion = location1.address
            estado = obtener_estado(location1)
            st.write(f"Estado: {estado}")
    else:
        location1_coords_str = st.text_input("Ingresa las coordenadas de tu ubicación (lat, long):")
        if location1_coords_str:
            location1_coords = tuple(map(float, location1_coords_str.split(", ")))
            location1 = geolocator.reverse(location1_coords)
            if not location1:
                st.error("Ubicación no encontrada.")
                st.stop()
            st.write(f"Dirección de las coordenadas ingresadas: {location1.address}")
            stringDireccion = location1.address
            estado = obtener_estado(location1)
            st.write(f"Estado: {estado}")

    if (option == 'Dirección' and location1_name) or (option == 'Coordenadas' and location1_coords_str):
        # Coordenadas de las regiones
        noroeste = "28.77068233170991, -110.61761330069028"
        noreste = "27.3477085247903, -101.89562544155896"
        centronorte = "22.414706207933026, -101.69666847368826"
        occidente = "20.63446861402605, -103.36662687985577"
        oriente = "19.193128608378363, -96.40063880385492"
        centrosur = "19.55583193741181, -99.86956345401865"
        suroeste = "16.31636212721643, -96.54839051155398"
        sureste = "19.89338541488356, -88.94002917586535"

        listaRegiones = [noroeste, noreste, centronorte, occidente, oriente, centrosur, suroeste, sureste]
        listaNombres = ["norOeste", "norEste", "centroNorte", "occidente", "oriente", "centroSur", "surOeste", "surEste"]

        # Calcular distancias y encontrar la mínima
        listaDistancias = [funcionDistancia(location1_coords, region) for region in listaRegiones]
        valorMinimo = min(listaDistancias)
        indiceValorMinimo = listaDistancias.index(valorMinimo)

        st.write(f"La región más cercana es {listaNombres[indiceValorMinimo]} con una distancia de {valorMinimo:.2f} kilómetros.")
except Exception as e:
    st.error(f"Error: {e}")

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
topFiveTrees = get_top_five(mexicanTreesDf, state, listaNombres[indiceValorMinimo])

# Iterate in the top 5 to print them 1 by 1
for i in range(len(topFiveTrees)):
    st.write(f'The option {i + 1} is: {topFiveTrees[i]}')

# Function that shows the first 5 images from the tree selected
def TreeImages(query):
    API_KEY = 'AIzaSyBCpNc-AXT-4oFIFovHxGrXeEmQoGex43M'
    SEARCH_ENGINE_ID = '03d887cb843cf464e'

    search_query = query + ' tree'

    url = 'https://www.googleapis.com/customsearch/v1'

    params = {
        'q': search_query,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'searchType': 'image'
    }

    response = requests.get(url, params=params)
    results = response.json()['items']

    for item in results[:5]:
        st.write(item['link'])

# Shows the first 5 images of the top five trees
for i in range(len(topFiveTrees)):
    st.image(TreeImages(topFiveTrees[i]))

# User chooses the main tree
treeSelection = st.radio("\nFrom the previous trees, select the option you desire: ", (1,2,3,4,5))

# if to create the variable of the selected tree

if treeSelection == 1:
    selectedTree = topFiveTrees[0]
elif treeSelection == 2:
    selectedTree = topFiveTrees[1]
elif treeSelection == 3:
    selectedTree = topFiveTrees[2]
elif treeSelection == 4:
    selectedTree = topFiveTrees[3]
else:
    selectedTree = topFiveTrees[4]

# we calculate the estimated cost
class Cost():
    def __init__(self, state): # constructor
        self.state = state
        self.MANPOWERDICTIONARY = {'Aguascalientes':0.0,  # index of increments from every state
                                   'Baja California':11.7,
                                   'Baja California Sur':1.8,
                                   'Campeche':4.8,
                                   'Chiapas':10.0,
                                   'Chihuahua':5,
                                   'Coahuila':3.9,
                                   'Colima':4.2,
                                   'Durango':4.9,
                                   'Guanajuato':2.2,
                                   'Guerrero':8.8,
                                   'Hidalgo':10.8,
                                   'Jalisco':3.5,
                                   'México':4.3,
                                   'Michoacán':7.2,
                                   'Morelos':4.1,
                                   'Nayarit':3.2,
                                   'Nuevo León':3.7,
                                   'Oaxaca':8.5,
                                   'Puebla':6.5,
                                   'Querétaro':6.4,
                                   'Quintana Roo':6.6,
                                   'San Luis Potosí':13.9,
                                   'Sinaloa':11.0,
                                   'Sonora':5.7,
                                   'Tabasco': 6.6,
                                   'Tamaulipas':5.0,
                                   'Tlaxcala':7.2,
                                   'Veracruz':8.2,
                                   'Yucatán':0.7,
                                   'Zacatecas':-4.5}
        self.MEDIA = 111.77   # the mean cost of manpower in México

    def getManPower(self):    # getting the value of the manpower by using the mean and index of increment
        index = self.MANPOWERDICTIONARY[self.state] + 100
        manPower = (self.MEDIA * index) / 100
        return manPower

    def setInfrastructure(self): # question on the quality of the infrastructure to see how many estimated porcentage we add to the final cost
        st.write('\nFrom the following options (Good, Bad, Regular) write the correct one...')
        level = text.input('What is the level of infrastructure like? (How difficult is it to arrive to the destination place or to carry instruments): ')

        # validates the input
        valid_levels = {'good','Good','GOOD','Bad','bad','Bad','regular','Regular','REGULAR'}
        while level not in valid_levels:
            st.error('Error! The input is incorrect.')
            level =input('Try again: ')

        self.level = level

    # calculates the estimated cost
    def calculate(self):
        if self.level =='Bad'or self.level == 'bad'or self.level == 'BAD':
            cost = self.getManPower() * 1.02
        elif self.level == 'Regular'or self.level == 'regular'or self.level == 'REGULAR':
            cost = self.getManPower() * 1.01
        else:
            cost = self.getManPower() * 1.005

        result = 'The estimated cost of planting a tree in {} is: ${}'.format(self.state, cost)
        return result

# Implement the Cost class
estimatedCost = Cost(state) # Let's assume we are working again with Durango state

# Ask user for the infrastructure
estimatedCost.setInfrastructure()
# Calculate the estimated cost
estimatedCost = estimatedCost.calculate()
st.write(f"{estimatedCost}") # Print the estimated cost