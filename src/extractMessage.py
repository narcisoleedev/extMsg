import json
import pandas as pd
import re

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
    200: "Contexto aberto"} #Mapeia as siglas com os nomes dos blocos

getMsg = ['message', 'messageDidNotUnderstand', 'questions', 'title', 'payload'] #Tipos de chaves de mensagem

df = pd.DataFrame(columns=['Grupo', 'Entente', 'TipoBloco', 'Message', 'TipoMsg']) #Dados das mensagens
dfRequest = pd.DataFrame(columns=['Grupo', 'Entente', 'Request']) #Dados das funções de request

def treatPayload(grupo, entente, payload):

    patternRequest = r'request\(.*?\)\);' 
    patternMsg = r"msg\((.*?)\);"

    matchRequest = re.findall(patternRequest, payload, re.DOTALL) #Acha todos os patterns de request() e retorna como lista
    matchMsg = re.findall(patternMsg, payload, re.DOTALL) #Acha todos os patterns de msg() e retorna como lista

    global dfRequest
    if matchRequest: #Verifica se a lista de matchRequest() é vazia, se não ele itera e coloca no dataframe por item
        for row in matchRequest:
            dfRequest = pd.concat([dfRequest, pd.DataFrame([{
                'Grupo': grupo,
                'Entente': entente,
                'Request': row,
            }])], ignore_index=True)

    if(matchMsg): #Se tiver um array de msg(), retorna como resultado da função.
        return matchMsg
    else:
        return None

def recursive(data, group, entente, tipoBloco): #Função recursiva que insere uma linha no DataFrame de Msg
    for key, value in data.items(): #Itera sobre as chaves e os valores
        if key in getMsg: #Verifica se a chave está na lista de getMsg
            if key == 'questions' and isinstance(value, list): #Como question é uma lista, ele itera para inserir todos os elementos dessa lista
                for question in value: 
                    appendToDf(group, entente, tipoBloco, question, key)
            elif key=='title': #Verifica se o atributo 'title' está acompanhado de 'isChip'
                if('isChip' in data): 
                    if data.get('isChip', 'true'):
                        appendToDf(group, entente, tipoBloco, value, key)
            elif key == 'payload': #Verifica-se é payload, se sim, ele trata pela função treatPlayload
                payload = treatPayload(group, entente, value)
                if(isinstance(payload, list)):
                    for e in payload:
                        appendToDf(group, entente, tipoBloco, e, key)
            elif isinstance(value, str): 
                appendToDf(group, entente, tipoBloco, value, key)
    
        elif isinstance(value, dict): #Se for um dict, "recursiva"
            recursive(value, group, entente, tipoBloco)
        
        elif isinstance(value, list): #Se for um array de dict's, "recursiva"
            for item in value:
                if isinstance(item, dict):
                    recursive(item, group, entente, tipoBloco)

def appendToDf(group, entente, tipoBloco, message, tipoMsg): #Função de adicionar 
    global df
    row = {
        'Grupo': group,
        'Entente': entente,
        'TipoBloco': tipoBloco,
        'Message': message,
        'TipoMsg': tipoMsg
    }
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

def iterateIntent(data): #Itera sobre o dicionário do JSON
    for g in data["groups"]: 
        for b in (((g["blocks"])['drawflow'])['Home'])['data'].values():  #Itera sobre os valores dentro de cada grupo
            group = b['data']['groupId']
            entente = b['data']['name']
            tipoBloco = tipoIntent[b['data']['intentType']]
            recursive(b, group, entente, tipoBloco)

    #Salva os arquivos em csv
    df.to_csv('./msg.csv', sep='|', index=False) 
    dfRequest.to_csv('./req.csv', sep='|', index=False) 
    df.to_excel('./msg.xlsx', index=False) 
    dfRequest.to_excel('./req.xlsx', index=False) 





