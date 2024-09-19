import json

from src.verifyIntent import verifyIntent
from src.extractMessage import iterateIntent
from src.msgToTxt import msgToTxt
  
def main():
    with open('./data-json.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    iterateIntent(data)
    msgToTxt()
    
if __name__ == "__main__":
    main()
