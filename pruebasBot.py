

def response(sentence):
    return "Llamada a ChatGPT"



bot_name = "Sam"
print("Let's chat! (type 'quit' to exit)")
while True:
    # sentence = "do you use credit cards?"
    sentence = input("You: ")
    if sentence == "quit":
        break
    else:
        print(f"{bot_name}: " + response(sentence) )