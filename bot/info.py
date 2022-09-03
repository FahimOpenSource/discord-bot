import json

def save(data: dict):
    obj = get()
    for key, value in data.items():
        obj[key] = value

    with open("bot/info.json", "w") as file:
        json.dump(obj, file)
        

def get():
    # Opening JSON file
    try:
        with open('bot/info.json', 'r') as file:
        # Reading from json file
            return json.load(file)

    except FileNotFoundError:
        with open('bot/info.json', 'w') as file:
            json.dump({},file)
            file.close()
            # Closing the file
        return get()
    

