import json
import os
from pyproj import Transformer

print("Starting conversion...")

input_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Alur_Survey_63.geojson"
)

output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Alur_Survey_63_WGS84.geojson"
)

print("Input file:")
print(input_file)

print()
print("Output file:")
print(output_file)

# UTM Zone 43N -> WGS84 latitude/longitude
transformer = Transformer.from_crs(
    "EPSG:32643",
    "EPSG:4326",
    always_xy=True
)

with open(input_file, "r", encoding="utf-8") as f:
    geojson = json.load(f)

print()
print("Input GeoJSON loaded.")

def convert_coordinates(coords):

    # Actual coordinate: [x, y]
    if isinstance(coords[0], (int, float)):
        x, y = coords

        lon, lat = transformer.transform(x, y)

        return [lon, lat]

    # Nested coordinates
    return [convert_coordinates(c) for c in coords]


for feature in geojson["features"]:

    geometry = feature["geometry"]

    geometry["coordinates"] = convert_coordinates(
        geometry["coordinates"]
    )


with open(output_file, "w", encoding="utf-8") as f:
    json.dump(geojson, f, indent=2)

print()
print("SUCCESS!")
print("Geometry:", geojson["features"][0]["geometry"]["type"])
print("Features:", len(geojson["features"]))
print("Coordinate system: WGS84 / EPSG:4326")

print()
print("First coordinate:")

first = geojson["features"][0]["geometry"]["coordinates"][0][0][0]

print("Longitude:", first[0])
print("Latitude:", first[1])

print()
print("Saved successfully:")
print(output_file)