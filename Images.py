import requests
def TreeImages(query):
    API_KEY = 'AIzaSyBCpNc-AXT-4oFIFovHxGrXeEmQoGex43M'
    SEARCH_ENGINE_ID = '03d887cb843cf464e'

    search_query = query + ' tree'

    url = 'https://www.googleapis.com/customsearch/v1'

    params = {
        'q': search_query,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'searchType': 'image',
    }

    response = requests.get(url, params=params)
    results = response.json()['items']

    for item in results[:5]:
        print(item['link'])
