import openai
openai.api_key = "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"
date = "18/06/2023"
response = openai.Completion.create(
    model="ada:ft-personal:tfm-2023-06-18-17-15-30",
    prompt="Como esta el día por Terrer? Asumiendo que hoy es: "+ date+" ->",
    max_tokens=100,
    stop="}}")



print(response.choices[0].text+"}}")