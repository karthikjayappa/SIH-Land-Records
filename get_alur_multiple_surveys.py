import requests
import json
import os
import time

BASE_URL = "https://sujala3lri.karnataka.gov.in"

url = BASE_URL + "/DSSCommonFunctions/getAoiEnvelop"

surveys = ["61", "62", "63", "64", "65"]

features = []

for survey in surveys:

    print("Getting Survey", survey, "...")

    data = {
        "District": "Davanagere",
        "Taluk": "Davanagere",
        "Village": "Alur",
        "surveyNumber": survey,
        "watershedType": "",
        "watershedName": ""
    }

    response = requests.post(url, data=data)

    if response.status_code != 200:
        print("  ERROR:", response.status_code)
        continue

    try:
        result = response.json()

        # API returns JSON inside a JSON string
        if isinstance(result, str):
            result = json.loads(result)

        if result.get("type") != "FeatureCollection":
            print("  Invalid GeoJSON response")
            continue

        for feature in result.get("features", []):

            # Add our own useful properties
            feature["properties"] = {
                "district": "Davanagere",
                "taluk": "Davanagere",
                "village": "Alur",
                "survey_number": survey,
                "source": "Karnataka LRI"
            }

            features.append(feature)

        print("  SUCCESS")

    except Exception as e:
        print("  ERROR:", e)

    # Small delay between requests
    time.sleep(0.5)


# Create one FeatureCollection
output = {
    "type": "FeatureCollection",
    "features": features
}


output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Alur_Real_Parcels_61_65.geojson"
)


with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)


print()
print("================================")
print("DONE")
print("================================")
print()
print("Parcels retrieved:", len(features))
print()
print("Saved:")
print(output_file)
