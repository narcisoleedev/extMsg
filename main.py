import json

from src.verifyIntent import verifyIntent
  
def main():
    with open('./data-json.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    verifyIntent(data)

if __name__ == "__main__":
    main()

