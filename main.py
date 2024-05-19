import os
import pandas as pd
import streamlit as st
from PIL import Image
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import geodesic
from vision import Trees
import supervision as sv
from fertileLand import fertileLand
from thefuzz import fuzz, process
import requests

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
    specificZoneTrees = mainDataFrame.loc[(mainDataFrame[dataFrameRegion] == region) & (mainDataFrame[dataFrameState] == state)]

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
def distanceFunction(location1, location2):
    location2Coords = tuple(map(float, location2.split(", ")))
    distance = geodesic(location1, location2Coords).kilometers
    return distance

def getState(location):
    address = location.raw['address']
    state = address.get('state', 'Not found')
    return state

# Function to compare two strings
# NOTE: stringOne MUST be the one that's not in the df
def compare_strings(stringOne, stringTwo):
    score = fuzz.partial_ratio(stringOne, stringTwo)

    if score >= 90:
        stringTwo = stringOne

    return stringTwo

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
        #st.image(item['link'])
        st.write(item['link'])

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

editedphoto = None
#file upload
uploaded_file = st.file_uploader("Upload photo")
# Get the directory of the current script
current_dir = os.path.dirname(os.path.realpath(__file__))

if os.path.exists('saved_image.jpeg'):
    os.remove('saved_image.jpeg')

if uploaded_file is not None:
    #image = Image.open(uploaded_file)
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    # Save the image
    image_path = os.path.join(current_dir, 'saved_image.jpeg')  # specify the path to save the image
    image.save(image_path)
    col1, col2, col3 = st.columns(3)

    if st.button('Hacer estudio'):
        tree = Trees(700, "saved_image.jpeg")
        count = tree.get_count()
        a = tree.get_image()
        with col2:
            st.image(a, caption='Found ' + str(count) + " main trees.", use_column_width=True)
        land = fertileLand("saved_image.jpeg", 11000)
        grass, dirt = land.get_image()
        with col1:
            st.image(grass, caption='Grass.', use_column_width=True)
        with col3:
            st.image(dirt, caption='Dirt.', use_column_width=True)

        b = tree.get_intersection_points()

        st.image(b, caption='Recommended trees on red spots.', use_column_width=True)

# Inicializar geocodificador
geolocator = Nominatim(user_agent="pruebas")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=2)

st.title('Find the closest region')

option = st.radio("Choose the entry format:", ('Address', 'Coordinates'))

stringAddress = ""

state = ''
region = ''
try:
    if option == 'Address':
        location1Name = st.text_input("Type your address:")
        if location1Name:
            location1 = geolocator.geocode(location1Name)
            if not location1:
                st.error("Address not found, try using coordinates.")
                st.stop()
            location1Coords = (location1.latitude, location1.longitude)
            location1_coordReverse = geolocator.reverse(location1Coords)
            stringAddress = location1_coordReverse.address
            state = getState(location1_coordReverse)
            st.write(f"Coordinates for the given coordinates: {location1Coords}")
    else:
        location1CoordsStr = st.text_input("Type in your coordinates.  (lat, long):")
        if location1CoordsStr:
            location1Coords = tuple(map(float, location1CoordsStr.split(", ")))
            location1 = geolocator.reverse(location1Coords)
            if not location1:
                st.error("Address not found.")
                st.stop()
            stringAddress = location1.address
            state = getState(location1)
            st.write(f"Address for the given coordinates: {location1.address}")

    if (option == 'Address' and location1Name) or (option == 'Coordinates' and location1CoordsStr):
        # Coordenadas de las regiones
        northWest = "28.77068233170991, -110.61761330069028"
        northEast = "27.3477085247903, -101.89562544155896"
        northCenter = "22.414706207933026, -101.69666847368826"
        west = "20.63446861402605, -103.36662687985577"
        east = "19.193128608378363, -96.40063880385492"
        southCenter = "19.55583193741181, -99.86956345401865"
        southWest = "16.31636212721643, -96.54839051155398"
        southEast = "19.89338541488356, -88.94002917586535"

        regionList = [northWest, northEast, northCenter, west, east, southCenter, southWest, southEast]
        namesList = ["North West", "North East", "North Center", "West",
                        "East", "South Center", "South West", "South East"]

        # Calcular distancias y encontrar la mínima
        distanceList = [distanceFunction(location1Coords, region) for region in regionList]
        minValue = min(distanceList)
        minValueIndex = distanceList.index(minValue)

        region = namesList[minValueIndex]

        # Verify the similarity on the strings
        state = compare_strings(state, mexicanTreesDf['STATE'])
        region = compare_strings(region, mexicanTreesDf['REGION'])

        # Calculate top 5 trees acoording to the state and region
        topFiveTrees = get_top_five(mexicanTreesDf, state, region, 'REGION', 'STATE')

        # Display title with the top five trees
        st.title('Top 5 trees in the region.')

        # Iterate over the top five trees and print them
        for i in range(len(topFiveTrees)):
            st.write(f"The option {i + 1} is: {topFiveTrees[i]}")

        # Shows the first 5 images of the top five trees
        st.title('Images of the trees:')

        if st.button('View'):
            for i in range(len(topFiveTrees)):
                st.write(f"{topFiveTrees[i]}")
                TreeImages(topFiveTrees[i])
                #st.image(TreeImages(topFiveTrees[i]))

except Exception as e:
    st.error("Error, try using coordinates.")

