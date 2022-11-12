import json

def test_read_json():
    with open('test.json', 'r') as f:
        json_data = json.load(f)
        print(type(json_data))
        json_data['batters']['batter'][3]['type'] = "horzsolt"
        #json_data[4][1][3][1] = "horzsolt"

    with open("test.json", "w") as write_file:
        json.dump(json_data, write_file, indent=4)
