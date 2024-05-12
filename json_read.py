import json
def json_read():

    with open(".\\config\\config.json", "r") as jsonfile:
        global config
        config = json.load(jsonfile)
        return config
