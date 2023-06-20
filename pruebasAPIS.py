import requests
import urllib
import json

url = "https://weather-by-api-ninjas.p.rapidapi.com/v1/weather"

querystring = {"city":"Palma de Mallorca"}

headers = {
	"X-RapidAPI-Key": "d08972acafmsh47671a8215e3be1p1fa5afjsncfa144723584",
	"X-RapidAPI-Host": "weather-by-api-ninjas.p.rapidapi.com"
}

response = json.loads(str(requests.request("GET", url, headers=headers, params=querystring).text))

print("True" if "error" in response.keys() else "False")

"""
#url = "https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/equipamientos/da_cultura_ocio_monumentos-25830.csv"

#response = requests.request("GET", url)
#response.encoding = response.apparent_encoding

#parkings_list=response.text
#print(parkings_list)
#df=pd.DataFrame(parkings_list)
#print(df.head())
#df.to_csv("pruebasMonumentos.csv",encoding="UTF-8")
df = pd.read_csv("da_cultura_ocio_monumentos-25830 (1).csv")
print(df.head())
"""