import pandas as pd
import re

msgs = []

def msgToTxt():

    df = pd.read_csv('./msg.csv', sep='|')

    principal = df[df['Grupo'] == 'principal']  
    nprincipal = df[df['Grupo'] != 'principal']

    dfOrd = pd.concat([principal, nprincipal])

    for i, r in dfOrd.iterrows(): #Itera sobre o DataFrame
        if r['Message'] is not None: #Se a mensagem não for vazia ele adiciona ao array de msgs
            if(r['TipoMsg']=='payload'): #Se for payload ele faz o tratamento e adiciona a msgs
                match = re.search(r"'(.*?)'", r['Message'])
                if(match!=''): #Se não retornar nada 
                    msgs.append(match)
            else: #Adiciona as messages ao array
                msgs.append(r['Message'])
    with open('./msg.txt', 'w') as f:
        for msg in msgs:
            f.write(msg + '\n') 

