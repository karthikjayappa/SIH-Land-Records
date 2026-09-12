import requests
import json
import os
import time

BASE_URL = "https://sujala3lri.karnataka.gov.in"

url = BASE_URL + "/DSSCommonFunctions/getAoiEnvelop"

# Read the survey numbers from the API
survey_url = BASE_URL + "/DSSCommonFunctions/OnVillageChange"

survey_data = {
    "VillageId": "Alur",
    "wscode": "0",
    "DistrictId": "Davanagere",
    "talukaId": "Davanagere",
    "Hobli": "0"
}

print("Getting official survey list...")

response = requests.post(survey_url, data=survey_data)

if response.status_code != 200:
    print("Failed to get survey list:", response.status_code)
    print(response.text)
    exit()

result = response.json()

if isinstance(result, str):
    result = json.loads(result)

survey_list = result.get("SurvenumberList", [])

surveys = [
    str(item["Survey_number"])
    for item in survey_list
]

print("Total survey numbers:", len(surveys))
print()

# Store all GeoJSON features
features = []

successful_surveys = []
failed_surveys = []

# Download geometry for every survey
for index, survey in enumerate(surveys, start=1):

    print(
        f"[{index}/{len(surveys)}] "
        f"Getting Survey {survey}..."
    )

    data = {
        "District": "Davanagere",
        "Taluk": "Davanagere",
        "Village": "Alur",
        "surveyNumber": survey,
        "watershedType": "",
        "watershedName": ""
    }

    try:

        response = requests.post(
            url,
            data=data,
            timeout=30
        )

        if response.status_code != 200:
            print(
                "  FAILED - HTTP",
                response.status_code
            )

            failed_surveys.append(survey)
            continue

        result = response.json()

        # API returns JSON inside a JSON string
        if isinstance(result, str):
            result = json.loads(result)

        if result.get("type") != "FeatureCollection":
            print("  FAILED - Invalid GeoJSON")
            failed_surveys.append(survey)
            continue

        survey_features = result.get(
            "features",
            []
        )

        if not survey_features:
            print("  WARNING - No geometry")
            failed_surveys.append(survey)
            continue

        # Add metadata to every feature
        for feature in survey_features:

            feature["properties"] = {
                "district": "Davanagere",
                "taluk": "Davanagere",
                "village": "Alur",
                "survey_number": survey,
                "source": "Karnataka LRI"
            }

            features.append(feature)

        successful_surveys.append(survey)

        print(
            "  SUCCESS -",
            len(survey_features),
            "feature(s)"
        )

    except Exception as e:

        print("  ERROR:", e)

        failed_surveys.append(survey)

    # Small delay
    time.sleep(0.3)


# Create final FeatureCollection
output = {
    "type": "FeatureCollection",
    "features": features
}


output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Alur_All_Real_Parcels.geojson"
)


with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        output,
        f,
        indent=2
    )


# Save extraction report
report = {
    "district": "Davanagere",
    "taluk": "Davanagere",
    "village": "Alur",
    "total_surveys": len(surveys),
    "successful_surveys": len(successful_surveys),
    "failed_surveys": len(failed_surveys),
    "total_features": len(features),
    "failed_survey_numbers": failed_surveys
}


report_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Alur_extraction_report.json"
)


with open(
    report_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        report,
        f,
        indent=2
    )


print()
print("======================================")
print("EXTRACTION COMPLETE")
print("======================================")
print()
print("Survey numbers found:", len(surveys))
print("Successful surveys:", len(successful_surveys))
print("Failed surveys:", len(failed_surveys))
print("Total GeoJSON features:", len(features))
print()
print("GeoJSON:")
print(output_file)
print()
print("Report:")
print(report_file)