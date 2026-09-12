import json
import os
from pyproj import Transformer

print("Starting Alur parcel conversion...")
print()

folder = os.path.dirname(os.path.abspath(__file__))

input_file = os.path.join(
    folder,
    "Alur_All_Real_Parcels.geojson"
)

output_file = os.path.join(
    folder,
    "Alur_All_Real_Parcels_WGS84.geojson"
)

# Karnataka LRI coordinates:
# UTM Zone 43N / WGS84
# EPSG:32643
#
# Convert to:
# WGS84 longitude/latitude
# EPSG:4326

transformer = Transformer.from_crs(
    "EPSG:32643",
    "EPSG:4326",
    always_xy=True
)


# -----------------------------
# Load GeoJSON
# -----------------------------

with open(
    input_file,
    "r",
    encoding="utf-8"
) as f:

    geojson = json.load(f)


print("Input loaded.")
print("Features:", len(geojson["features"]))
print()


# -----------------------------
# Coordinate conversion
# -----------------------------

def convert_coordinates(coords):

    # Actual coordinate:
    # [x, y]

    if isinstance(coords[0], (int, float)):

        x = coords[0]
        y = coords[1]

        lon, lat = transformer.transform(x, y)

        return [lon, lat]

    # Nested coordinates

    return [
        convert_coordinates(c)
        for c in coords
    ]


# -----------------------------
# Convert every feature
# -----------------------------

for index, feature in enumerate(
    geojson["features"],
    start=1
):

    geometry = feature.get("geometry")

    if geometry and geometry.get("coordinates"):

        geometry["coordinates"] = convert_coordinates(
            geometry["coordinates"]
        )

    if index % 10 == 0:
        print(
            "Converted",
            index,
            "/",
            len(geojson["features"])
        )


# -----------------------------
# Add CRS information
# -----------------------------

geojson["crs"] = {
    "type": "name",
    "properties": {
        "name": "EPSG:4326"
    }
}


# -----------------------------
# Save
# -----------------------------

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        geojson,
        f,
        indent=2
    )


# -----------------------------
# Verify
# -----------------------------

first_feature = geojson["features"][0]

first_coordinate = (
    first_feature["geometry"]
    ["coordinates"][0][0][0]
)


print()
print("======================================")
print("CONVERSION COMPLETE")
print("======================================")
print()

print("Total features:", len(geojson["features"]))

print()
print("First coordinate:")
print("Longitude:", first_coordinate[0])
print("Latitude:", first_coordinate[1])

print()
print("Coordinate system:")
print("WGS84 / EPSG:4326")

print()
print("Saved:")
print(output_file)