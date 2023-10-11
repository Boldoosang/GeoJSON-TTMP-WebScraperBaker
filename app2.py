import json

ttmapJson = open("ttmap.geojson")
constituenciesJson = open("constituencies.json")

polygonData = json.load(ttmapJson)
constituencyData = json.load(constituenciesJson)

collection = polygonData["features"]


for polygon in collection:
    for constituency in constituencyData:
        if polygon["properties"]["ID"] == constituency["constituency_code"]:
            polygon["properties"]["official"] = constituency["official"]

with open("ttmap.geojson", "w") as f:
    f.write(json.dumps(collection))
    print("Exported to ttmap.geojson!")