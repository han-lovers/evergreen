from geopy.geocoders import Nominatim
from geopy.distance import geodesic

#inicializar gecodificador

geolocator = Nominatim(user_agent = "geoapiExercises")

##coordenadas de cada lugar

location1 = geolocator.geocode("Andares, Guadalajara")
location2 = geolocator.geocode("Empire State Building, United States")


coordsLocation1 = (location1.latitude, location1.longitude)
coordsLocation2 = (location2.latitude, location2.longitude)

distanceBetween = geodesic(coordsLocation1, coordsLocation2).kilometers

print(f"La distancia entre los puntos es de: {distanceBetween}")




