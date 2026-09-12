import requests
import json

BASE_URL = "https://sujala3lri.karnataka.gov.in"

url = BASE_URL + "/DSSCommonFunctions/OnVillageChange"

data = {
    "VillageId": "Alur",
    "wscode": "0",
    "DistrictId": "Davanagere",
    "talukaId": "Davanagere",
    "Hobli": "0"
}

response = requests.post(url, data=data)

print("Status:", response.status_code)
print()

if response.status_code != 200:
    print(response.text)
    exit()

# First JSON layer
result = response.json()

# The server returns JSON as a string
if isinstance(result, str):
    result = json.loads(result)

survey_list = result.get("SurvenumberList", [])

print("Total survey entries:", len(survey_list))
print()
print("Survey numbers:")
print("----------------")

for item in survey_list:
    print(
        item.get("Survey_number"),
        "->",
        item.get("Survey_number_Text")
    )
    