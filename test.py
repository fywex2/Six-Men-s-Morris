import json

with open('GameData.json', 'r') as file:
    existing_data = json.load(file)
for key in my_dict:
    if key in seen_keys:
        print(True)
    seen_keys.add(key)