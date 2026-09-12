import requests
import json

BASE_URL = "https://mobservice.sujala3lri.karnataka.gov.in"

url = BASE_URL + "/DSSCommonFunctions/OnTalukaChange"

data = {
    "TaukaId": "Davanagere"
}

response = requests.post(url, data=data)

print("Status:", response.status_code)
print("Raw response:")
print(response.text)

if response.status_code == 200:
    states = response.json()

    # API returns JSON containing another JSON string
    if isinstance(states, str):
        states = json.loads(states)

    village_list = states.get("Villagelist", [])

    print("\nALUR SEARCH RESULT:")
    print("-------------------")

    for village in village_list:
        name = village.get("Village_Name")
        code = village.get("Village_Code")

        if name and ("Alur" in name or "Alur" in str(code)):
            print("Village Name:", name)
            print("Village Code:", code)

    print("\nALL VILLAGES:")
    print("-------------")

    for village in village_list:
        print(
            village.get("Village_Code"),
            " -> ",
            village.get("Village_Name")
        )