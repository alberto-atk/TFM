import openai
import json, requests, urllib, os
import pandas as pd
from openai.api_resources import Completion
#export OPENAI_API_KEY="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"

def getResponse(data):
    openai.api_key = "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"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=1500,
        messages=[
                {"role": "user", "content": data},
            ]
    )
    """
    with open('respuestaCompletion.json', 'r') as archivo:
        contenido_json = archivo.read()
    response = json.loads(contenido_json)
    """
    return(response.choices[0]["message"]["content"])



def getAction(sentence):
    
    openai.api_key = "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"
    
    response = openai.Completion.create(
        model="ada:ft-personal:tfm-v2-2023-06-19-16-16-31",
        prompt=sentence+" ->",
        max_tokens=100,
        stop="}}")
    try:
        diccionario_respuesta = json.loads(response.choices[0].text+"}}")
    except ValueError:
        diccionario_respuesta = json.loads("{\"intent\":\"\",\"entities\":\"\"}")
        
    #diccionario_respuesta = json.loads("{\"intent\": \"get-electric-charger\",\"entities\":{\"avenue\": \"Calle María Curie\"}}")
    
    #print(diccionario_respuesta)
    switch = {
        "get-free-parkings": getParkingsFunction,
        "get_monument_location": getMonumentsFunction,
        "get_weather": getTemperatureFunction,
        "get-electric-charger": getElectricChargersFunction
    }
    print(diccionario_respuesta)
    accionEscogida = switch.get(diccionario_respuesta["intent"], funcionNoEncontrada)
    return accionEscogida(diccionario_respuesta["entities"])

def getParkingsFunction(entities):
    return ("ñslñk")

def getDataAPIMalaga(url):
    apis = {
        ("https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/"+
         "equipamientos/da_cultura_ocio_monumentos-25830.csv"):"monumentos.csv",
        ("https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/"+
         "equipamientos/da_cve-25830.csv"):"cargadores.csv"
    }
    if url in apis.keys():
        archivo = requests.get(url, stream=True)

        with open(apis[url], 'wb') as f:
            for ch in archivo:
                f.write(ch)
        df = pd.read_csv(apis[url])
        return df.set_index("ID")
    else:
        return None

from sentence_transformers import SentenceTransformer, util
def checkSimilarity(texto1, texto2):
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    similarity_score = util.cos_sim(model.encode([texto1]), model.encode([texto2]))
    #print(similarity_score.item())
    return True if similarity_score.item() >= 0.7 else False

def getMonumentsFunction(entities):
    url = "https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/equipamientos/da_cultura_ocio_monumentos-25830.csv"
    monuments = getDataAPIMalaga(url)
    
    for indice, fila in monuments.iterrows():
        #Versión biblio, sin sentence-similarity
        """
        if entities["monument"].lower() == fila["NOMBRE"].lower():
            mensajeCompletion = ("Explica los detalles del monumento desde los siguientes datos:\n" + 
                "Nombre: " + str(fila["NOMBRE"]).replace("\n"," ") + "\n"
                "Descripción: " + str(fila["DESCRIPCION"]).replace("\n"," ") + "\n"
                "Dirección: " + str(fila["DIRECCION"]).replace("\n"," ") + "\n"
                "Horarios: " + str(fila["HORARIOS"]).replace("\n"," ") + "\n"
                "Precios: " + str(fila["PRECIOS"]).replace("\n"," ") + "\n"
                "Tarjeta Joven: " + str(fila["TARJETAJOVEN"]).replace("\n"," ") + "\n")
            return getResponse(mensajeCompletion)
        """
        similarity = checkSimilarity(entities["monument"].lower(),fila["NOMBRE"].lower())
        #print(entities["monument"].lower() + " " +fila["NOMBRE"].lower())
        if similarity == True:
            mensajeCompletion = ("Explica los detalles del monumento desde los siguientes datos:\n" + 
                "Nombre: " + str(fila["NOMBRE"]).replace("\n"," ") + "\n"
                "Descripción: " + str(fila["DESCRIPCION"]).replace("\n"," ") + "\n"
                "Dirección: " + str(fila["DIRECCION"]).replace("\n"," ") + "\n"
                "Horarios: " + str(fila["HORARIOS"]).replace("\n"," ") + "\n"
                "Precios: " + str(fila["PRECIOS"]).replace("\n"," ") + "\n"
                "Tarjeta Joven: " + str(fila["TARJETAJOVEN"]).replace("\n"," ") + "\n")
            return getResponse(mensajeCompletion)
    return "Monumento no encontrado"
        
def getTemperatureFunction(entities):
    url = "https://weather-by-api-ninjas.p.rapidapi.com/v1/weather"

    querystring = {"city":entities["city"]}

    headers = {
        "X-RapidAPI-Key": "d08972acafmsh47671a8215e3be1p1fa5afjsncfa144723584",
        "X-RapidAPI-Host": "weather-by-api-ninjas.p.rapidapi.com"
    }

    response = json.loads(str(requests.request("GET", url, headers=headers, params=querystring).text))
    if "error" in response.keys():
        return "Localidad no encontrada en nuestros datos"
    mensajeCompletion = ("Elabora un pronóstico del tiempo basado en estos datos:\n"+
                        "Ciudad: " + str(entities["city"]) + "\n"+
                        "Temperatura: " + str(response["temp"]) + "\n"+
                        "Sensación Térmica: " + str(response["feels_like"]) + "\n"+
                        "Humedad: " + str(response["humidity"]) + "\n"     +              
                        "Temperatura Mínima: " + str(response["min_temp"]) + "\n"+
                        "Temperatura Máxima: " + str(response["max_temp"]) + "\n"+
                        "Velocidad del viento: " + str(response["wind_speed"]) + "\n")
    return getResponse(mensajeCompletion)

def getElectricChargersFunction(entities):
    url = "https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/equipamientos/da_cve-25830.csv"
    parkings = getDataAPIMalaga(url)
    for indice, fila in parkings.iterrows():
        #Versión biblio, sin sentence-similarity

        #print(entities["avenue"].lower())
        #print(' '.join(fila["NOMBRE"].split()[1:]).lower())
        #if entities["avenue"].lower() == ' '.join(fila["NOMBRE"].split()[1:]).lower():
        #    aux = dict(eval(fila["INFOESP"])[0])
        #    mensajeCompletion = ("Explica los detalles del punto de carga eléctrica basado en los siguientes datos:\n" + 
        #        "Dirección: " + str(fila["DIRECCION"]).replace("\n"," ") + "\n"
        #        "Descripción: " + str(fila["DESCRIPCION"]).replace("\n"," ") + "\n"
        #        "Tipo de carga: " + str(aux["Tipologia_de_carga"]).replace("\n"," ") + "\n"
        #        "Plazas disponibles: " + str(aux["Plazas_de_vehiculo_disponibles_para_recarga"]).replace("\n"," ") + "\n"
        #        "Número de puntos: " + str(aux["Numero_de_puntos_de_recarga"]).replace("\n"," ") + "\n")
        #    return getResponse(mensajeCompletion)
        
        similarity = checkSimilarity(entities["avenue"].lower(),' '.join(fila["NOMBRE"].split()[1:]).lower())
        #print(entities["avenue"].lower() + " " +' '.join(fila["NOMBRE"].split()[1:]).lower())
        if similarity == True:
            aux = dict(eval(fila["INFOESP"])[0])
            mensajeCompletion = ("Explica los detalles del punto de carga eléctrica basado en los siguientes datos:\n" + 
                "Dirección: " + str(fila["DIRECCION"]).replace("\n"," ") + "\n"
                "Descripción: " + str(fila["DESCRIPCION"]).replace("\n"," ") + "\n"
                "Tipo de carga: " + str(aux["Tipologia_de_carga"]).replace("\n"," ") + "\n"
                "Plazas disponibles: " + str(aux["Plazas_de_vehiculo_disponibles_para_recarga"]).replace("\n"," ") + "\n"
                "Número de puntos: " + str(aux["Numero_de_puntos_de_recarga"]).replace("\n"," ") + "\n")
            return getResponse(mensajeCompletion)
    return "Cargador eléctrico no encontrado"

def funcionNoEncontrada(entities):
    return("Lo siento, no soy capaz de realizar esta función")

bot_name = "Personalized-ChatGPT"
print("\033[37mHola! Soy un modelo de lenguaje basado en GPT-3-Ada, capaz de conectarse\n"+
      "con algunas aplicaciones en tiempo real, pudiendo realizar estas funciones: \n"+
      "- Información sobre monumentos de Málaga\n"+
      "- Información sobre ocupación de parkings en Málaga\n"+
      "- Información sobre cargadores eléctricos en Málaga\n"+
      "- Información sobre el tiempo en tiempo actual en un lugar concreto\n"+
      "¿Qué desea? (Escriba exit si quiere salir)")
while True:
    # sentence = "do you use credit cards?"
    sentence = input("\033[33;4mUsuario:\033[0m ")
    if sentence == "exit":
        break
    else:

        print(f"\n\033[4;36m{bot_name}:\033[0m" + "  \033[37m"+ getAction(sentence) + "\n" )