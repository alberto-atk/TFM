import openai
import json
from openai.api_resources import Completion
#export OPENAI_API_KEY="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"

def getAction(sentence):
    """
    openai.api_key = "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"
    date = "18/06/2023"
    response = openai.Completion.create(
        model="ada:ft-personal:tfm-2023-06-18-17-15-30",
        prompt=" Que me puedes contar de la giralda. Asumiendo que hoy es: "+ date+" ->",
        max_tokens=100,
        stop="}}")
    
    diccionario_respuesta = dict(print(response.choices[0].text+"}}"))
    """
    diccionario_respuesta = json.loads("{\"intent\": \"get_weather\",\"entities\":{\"city\": \"Giralda\",\"date\": \"18/06/2023\"}}")
    print(diccionario_respuesta["entities"])
    """
    switch = {
        "caso1": getParkingsFunction,
        "caso2": getMonumentsFunction,
        "caso3": getTemperatureFunction,
        "caso4": getElectricChargersFunction
    }

    accionEscogida = switch.get(diccionario_respuesta["intent"], funcionNoEncontrada)
    accionEscogida(diccionario_respuesta["entitities"])
"""
    return ""

def getParkingsFunction(entities):
    print("El parking es tal:" + entities)

def getMonumentsFunction(entities):
    print("El monumento es tal:" + entities)

def getTemperatureFunction(entities):
    print("La ciudad es tal:" + entities)

def getElectricChargersFunction(entities):
    print("El cargador es tal:" + entities)

def funcionNoEncontrada():
    print("Lo siento, no soy capaz de realizar esta función")

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
    sentence = input("\033[37mUsuario: ")
    if sentence == "exit":
        break
    else:

        print(f"\033[4;36m{bot_name}:\033[0m" + "  \033[37m"+ getAction(sentence) )