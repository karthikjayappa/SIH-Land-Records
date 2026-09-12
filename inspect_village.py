import requests
import json

BASE_API = "https://mobservice.sujala3lri.karnataka.gov.in/api"

hoblis = ["ANAGODU", "KASABA", "MAYAKONDA"]

for hobli in hoblis:

    print("\n")
    print("#" * 70)
    print("HOBLI:", hobli)
    print("#" * 70)

    url = f"{BASE_API}/GetVillage"

    params = {
        "hobliID": hobli,
        "talukID": "Davanagere",
        "culture": 1
    }

    response = requests.get(url, params=params, timeout=30)

    print("STATUS:", response.status_code)
    print("URL:", response.url)

    print("\nRAW RESPONSE:")
    print(response.text)

    # Save exact response
    filename = f"inspect_{hobli}.json"

    try:
        data = response.json()

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print("\nSAVED:", filename)

    except Exception as e:
        print("\nJSON ERROR:", e)