import json
from pprint import pprint

with open('city.list.json') as f:
    data = json.load(f)

for country in data:
    if "aachen" in country["name"].lower():
        print(country["id"])
        print(country["name"])
