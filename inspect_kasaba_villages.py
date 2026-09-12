import requests
import json

BASE_API = "https://mobservice.sujala3lri.karnataka.gov.in/api"

url = f"{BASE_API}/GetVillageforRegi"

params = {
    "hobliID": "KASABA",
    "talukID": "Davanagere",
    "district": "Davanagere",
    "culture": 1
}

response = requests.get(url, params=params, timeout=30)

print("STATUS:", response.status_code)
print("URL:", response.url)

if response.status_code == 200:

    data = response.json()

    print("\nTOTAL VILLAGES:", len(data))

    print("\n--- SHAYAMANURU RECORD ---")

    for village in data:
        if village.get("Village_Code") == "Shayamanuru":
            print(json.dumps(
                village,
                indent=2,
                ensure_ascii=False
            ))

else:
    print(response.text)