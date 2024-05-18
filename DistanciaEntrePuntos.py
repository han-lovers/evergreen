from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import geodesic

# Inicializar geocodificador
geolocator = Nominatim(user_agent="pruebas")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=2)

# Coordenadas de cada lugar
location1_name = input("Ingresa tu dirección o deja en blanco para usar coordenadas: ")

if location1_name:
    try:
        location1 = geolocator.geocode(location1_name)
        if not location1:
            raise ValueError("Ubicación no encontrada.")
    except Exception as e:
        print(f"Error: {e}")
else:
    try:
        location1_coords = input("Ingresa las coordenadas de tu ubicación (lat, long): ")
        location1 = geolocator.reverse(location1_coords)
        if not location1:
            raise ValueError("Ubicación no encontrada.")
    except Exception as e:
        print(f"Error: {e}")

location2 = "19.43257954644052, -99.13313474475538"

try:
    # Extraer las coordenadas de location1
    location1_coords = (location1.latitude, location1.longitude)

    # Convertir location2 a coordenadas
    location2_coords = tuple(map(float, location2.split(", ")))

    # Calcular y mostrar la distancia
    distancia = geodesic(location1_coords, location2_coords).kilometers
    print(f"La distancia entre las ubicaciones es de {distancia:.2f} kilómetros.")
except Exception as e:
    print(f"Error al calcular la distancia: {e}")
