import json

from src.verifyIntent import verifyIntent
from src.extractMessage import verifyIntent2
  
def main():
    with open('./data-json.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    #verifyIntent(data)
    verifyIntent2(data)
    

if __name__ == "__main__":
    main()

