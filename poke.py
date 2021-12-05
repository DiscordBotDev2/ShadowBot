import requests
def get(endpoint):
  res = requests.get('https://pokeapi.co/api/v2/pokemon/pikachu')
  data = res.json()
  return data
