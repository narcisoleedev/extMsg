import pandas as pd
import re

msgs = []

def msgToTxt():

    df = pd.read_csv('./msg.csv', sep='|')

    principal = df[df['Grupo'] == 'principal']  
    nprincipal = df[df['Grupo'] != 'principal']

    dfOrd = pd.concat([principal, nprincipal]) #Organiza por grupo "principal"

    for i, r in dfOrd.iterrows(): #Itera sobre o DataFrame
        if pd.notna(r['Message']): #Se a mensagem não for vazia ele adiciona ao array de msgs
            if(r['TipoMsg']=='payload'): #Se for payload ele faz o tratamento e adiciona a msgs
                match = re.findall(r"'(.*?)'", r['Message'])
                matchVar = re.findall(r"([^\s,]+),\s*'([^']+)'", r['Message'])
                print(matchVar)
                if match: #Se não retornar nada:
                    for m in match: 
                        if m!='text': #Se for 
                            msgs.append(m)
                else:
                    for m in matchVar:  
                        msgs.append(m)
            else: #Adiciona as messages ao array
                msgs.append(r['Message'])
    #print(msgs)

    with open('./msg.txt', 'w') as f:
        for msg in msgs:
            cleaned_msg = msg.strip()
            if cleaned_msg and ('\n' not in cleaned_msg):
                f.write(cleaned_msg + '\n\n')

