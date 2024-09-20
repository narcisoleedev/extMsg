import pandas as pd
import re

msgs = []

def msgToTxt():

    df = pd.read_csv('./out/csv/msg.csv', sep='|') #Lê o csv de msg

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

                else: #Se não retornar match:
                    for m in matchVar:  
                        msgs.append(m)

            else: #Adiciona as messages ao array
                msgs.append(r['Message'])

    #print(msgs)

    with open('./out/txt/msg.txt', 'w', encoding='utf-8') as f:

        for msg in msgs:

            cleaned_msg = msg.strip()
            if cleaned_msg and (cleaned_msg != '\\n\n' or cleaned_msg != r'\n'):
                f.write(cleaned_msg + '\n\n')
    
    with open('./out/txt/msg.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace(r'\n', '')

    with open('./out/txt/msg.txt', 'w', encoding='utf-8') as file:
        file.write(content)

    with open('./out/txt/msg.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Replace consecutive newlines with a single newline
    cleaned_text = re.sub(r'\n{3,}', '\n\n', text)
        
    # Write the cleaned text back to a new file
    with open('./out/txt/msg.txt', 'w', encoding='utf-8') as file:
        file.write(cleaned_text)


