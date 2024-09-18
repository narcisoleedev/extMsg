import json
import pandas as pd

# Mapping of intent types
tipoIntent = {
    120: "Lógica",
    110: "Pergunta",
    100: "Mensagem",
    7: "Envio",
    131: "Carrosel Vertical",
    130: "Múltipla Escolha",
    170: "Teste A/B",
    8: "Boas-vindas",
    9: "Não entendi",
    10: "Cancelar",
    200: "Contexto aberto"
}

# Messages to extract
getMsg = ['message', 'messageDidNotUnderstand', 'questions', 'title']

# Global DataFrame to store extracted messages
df = pd.DataFrame(columns=['Grupo', 'Entente', 'TipoBloco', 'Message', 'TipoMsg'])

def recursive_extraction(data, group, entente, tipoBloco):
    for key, value in data.items():
        # If key is in getMsg array, handle it accordingly
        if key in getMsg:
            # Special handling for 'questions' (which is an array)
            if key == 'questions' and isinstance(value, list):
                for question in value:
                    if isinstance(question, dict):
                        msg = question.get('title', '')
                        append_to_df(group, entente, tipoBloco, msg, 'question')
            # Handle other message types
            elif isinstance(value, str):
                append_to_df(group, entente, tipoBloco, value, key)
        
        # If the value is a dictionary, recursively process it
        elif isinstance(value, dict):
            recursive_extraction(value, group, entente, tipoBloco)
        
        # If the value is a list, process each item if it's a dictionary
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    recursive_extraction(item, group, entente, tipoBloco)

# Append data to the DataFrame
def append_to_df(group, entente, tipoBloco, message, tipoMsg):
    global df
    new_row = {
        'Grupo': group,
        'Entente': entente,
        'TipoBloco': tipoBloco,
        'Message': message,
        'TipoMsg': tipoMsg
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# Main function to start extraction from 'groups' and 'blocks'
def verifyIntent2(data):
    for g in data["groups"]:
        for b in g["blocks"]['drawflow']['Home'].values():
            group = b['data']['groupId']
            entente = b['data']['name']
            tipoBloco = tipoIntent.get(b['data']['intentType'], 'Unknown')  # Fetching the intent type
            recursive_extraction(b, group, entente, tipoBloco)  # Recursively extract data

# Print DataFrame or further process the data
print(df)
