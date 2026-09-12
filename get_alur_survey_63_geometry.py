import requests
import json
import os

BASE_URL = "https://sujala3lri.karnataka.gov.in"

url = BASE_URL + "/DSSCommonFunctions/getAoiEnvelop"

data = {
    "District": "Davanagere",
    "Taluk": "Davanagere",
    "Village": "Alur",
    "surveyNumber": "63",
    "watershedType": "",
    "watershedName": ""
}

print("Requesting Survey 63 geometry...")
print()

response = requests.post(url, data=data)

print("Status:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
print()

if response.status_code != 200:
    print("Request failed:")
    print(response.text)
    exit()

# The API returns JSON inside a JSON string
result = response.json()

if isinstance(result, str):
    result = json.loads(result)

# Check that we received GeoJSON
if result.get("type") != "FeatureCollection":
    print("Unexpected response:")
    print(result)
    exit()

# Save GeoJSON
output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Alur_Survey_63.geojson"
)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print("SUCCESS!")
print()
print("Geometry type:", result["features"][0]["geometry"]["type"])
print("Number of features:", len(result["features"]))
print()
print("Saved to:")
print(output_file)