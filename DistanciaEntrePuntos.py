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

# Obtener ubicación del usuario
location1_name = input("Ingresa tu dirección o deja en blanco para usar coordenadas: ")

try:
    if location1_name:
        location1 = geolocator.geocode(location1_name)
        if not location1:
            raise ValueError("Ubicación no encontrada.")
        location1_coords = (location1.latitude, location1.longitude)
    else:
        location1_coords_str = input("Ingresa las coordenadas de tu ubicación (lat, long): ")
        location1_coords = tuple(map(float, location1_coords_str.split(", ")))
        location1 = geolocator.reverse(location1_coords)
        if not location1:
            raise ValueError("Ubicación no encontrada.")
except Exception as e:
    print(f"Error: {e}")
    exit()

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

print(f"La región más cercana es {listaNombres[indiceValorMinimo]} con una distancia de {valorMinimo:.2f} kilómetros.")


