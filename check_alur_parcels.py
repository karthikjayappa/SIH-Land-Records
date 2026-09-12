import json
import os

file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Alur_Real_Parcels_61_65.geojson"
)

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Total features:", len(data["features"]))
print()

for i, feature in enumerate(data["features"], start=1):

    properties = feature.get("properties", {})
    geometry = feature.get("geometry", {})

    print("Feature", i)
    print("----------------")
    print("Survey:", properties.get("survey_number"))
    print("Geometry:", geometry.get("type"))

    coordinates = geometry.get("coordinates", [])

    print("Coordinate structure exists:", bool(coordinates))
    print()
    