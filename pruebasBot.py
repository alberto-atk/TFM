import openai

#export OPENAI_API_KEY="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"

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