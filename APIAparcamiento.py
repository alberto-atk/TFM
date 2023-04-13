import requests

url = 'https://datosabiertos.malaga.eu/api/3/action/datastore_search?resource_id=0dcf7abd-26b4-42c8-af19-4992f1ee60c6&limit=5&q=title:jones'  

querystring = {"city":"Ateca"}

response = requests.request("GET", url)

print(response.text)

