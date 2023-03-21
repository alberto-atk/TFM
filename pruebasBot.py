

def response(sentence):
    if sentence == "Rafa cabron":
        return "Si es"
    else:
        return "Esto lo consultaré con la API..."

bot_name = "Sam"
print("Let's chat! (type 'quit' to exit)")
while True:
    # sentence = "do you use credit cards?"
    sentence = input("You: ")
    if sentence == "quit":
        break
    else:
        print(f"{bot_name}: " + response(sentence) )