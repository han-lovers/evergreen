import streamlit as st
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import geodesic

# Inicializar geocodificador
geolocator = Nominatim(user_agent="pruebas")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=2)


def distanceFunction(location1, location2):
    location2Coords = tuple(map(float, location2.split(", ")))
    distance = geodesic(location1, location2Coords).kilometers
    return distance


def getState(location):
    address = location.raw['address']
    state = address.get('state', 'Not found')
    return state


st.title('Find the closest region')

option = st.radio("Choose the entry format:", ('Address', 'Coordinates'))

stringAddress = ""

try:
    if option == 'Address':
        location1Name = st.text_input("Type you address:")
        if location1Name:
            location1 = geolocator.geocode(location1Name)
            if not location1:
                st.error("Address not found, try using coordinates.")
                st.stop()
            location1Coords = (location1.latitude, location1.longitude)
            location1_coordReverse = geolocator.reverse(location1Coords)
            st.write(f"Coordinates of the given address: {location1Coords}")
            stringAddress = location1_coordReverse.address
            state = getState(location1_coordReverse)
            st.write(f"State: {state}")
    else:
        location1CoordsStr = st.text_input("Type in your coordinates.  (lat, long):")
        if location1CoordsStr:
            location1Coords = tuple(map(float, location1CoordsStr.split(", ")))
            location1 = geolocator.reverse(location1Coords)
            if not location1:
                st.error("Address not found.")
                st.stop()
            st.write(f"Address of the given coordinates: {location1.address}")
            stringAddress = location1.address
            state = getState(location1)
            st.write(f"State: {state}")

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

        st.write(f"La región más cercana es {namesList[minValueIndex]} con una distancia de {minValue:.2f} kilómetros.")
except Exception as e:
    st.error("Error, intenta usando coordenadas.")
