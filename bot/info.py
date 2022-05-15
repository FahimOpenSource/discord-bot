
import json

def save(data: dict):
    obj = get()
    for key, value in data.items():
        obj[key] = value

    with open("test.json", "w") as file:
        json.dump(obj, file)
        

def get():
    # Opening JSON file
    with open('test.json', 'r') as file:
        # Reading from json file
        return json.load(file)
    
    