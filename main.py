import streamlit as st
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import geodesic

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
