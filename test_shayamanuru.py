import requests
import json

BASE_API = "https://mobservice.sujala3lri.karnataka.gov.in/api"

url = f"{BASE_API}/GetVillage"

params = {
    "hobliID": "ANAGODU",
    "talukID": "Davanagere",
    "culture": 1
}

response = requests.get(url, params=params, timeout=30)

print("STATUS:", response.status_code)

data = response.json()

print("\nSEARCHING FOR SHAYAMANURU...\n")

for village in data:
    code = village.get("Village_Code", "")
    name = village.get("Village_Name", "")

    if "Shaya" in code or "ಶಾಯ" in name:
        print("FOUND:")
        print(json.dumps(village, indent=2, ensure_ascii=False))