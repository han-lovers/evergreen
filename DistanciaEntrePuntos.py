from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import geodesic

# Inicializar geocodificador
geolocator = Nominatim(user_agent="pruebas")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)

# Coordenadas de cada lugar
location1_name = "Escuela Militar de Clases de Transmisiónes"
location2_name = "Olivos Residencial"

location1 = geolocator.geocode(location1_name)
location2 = geolocator.geocode(location2_name)

# Verificar que las ubicaciones se encontraron
if location1 is None:
    print(f"No se pudo encontrar la ubicación para: {location1_name}")
if location2 is None:
    print(f"No se pudo encontrar la ubicación para: {location2_name}")

if location1 and location2:
    # Crear tuplas de coordenadas en el formato correcto (latitud, longitud)
    location1Coords = (location1.latitude, location1.longitude)
    location2Coords = (location2.latitude, location2.longitude)

    # Calcular y mostrar la distancia
    distancia = geodesic(location1Coords, location2Coords).kilometers
    print(f"La distancia entre {location1_name} y {location2_name} es de {distancia:.2f} kilómetros.")
else:
    print("No se pudo calcular la distancia debido a ubicaciones no encontradas.")
