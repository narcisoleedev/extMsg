Pra rodar esse programa, primeiramente baixe o Python 3.12, e as seguintes bibliotecas pelo pip:

- Pandas
- Seaborn e MatplotLib (se quiser rodar o verifyIntent)

Baixe o json do bot, como "data-json.json" na root do projeto.

Crie também uma pasta **out** na root do projeto e dentro dela, crie três pastas: **csv**, **txt**, **excel**.

Assim, use "python main.py" na root do projeto.
Ele gerará, arquivos csv e xlsx com tabelas com **todas os outputs textuais** e todos os blocos com **chamadas de api**, e também um arquivo txt como específicado nos documentos de treino do 123Fala.

### NOTES:

Teoricamente esse programa funciona para todos os fluxos de bot, entretanto, deve-se adicionar as intents faltantes no dicionário de tipoIntent no programa extractMessage.py.

Não deu pra comentar o código de verifyIntents, mas ele não é essencial para o plot.
