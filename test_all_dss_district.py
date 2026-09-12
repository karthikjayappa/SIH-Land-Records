import requests
import json

BASE_API = "https://mobservice.sujala3lri.karnataka.gov.in/api"

url = f"{BASE_API}/GetAllDSSDistrict"

params = {
    "culture": 1
}

try:
    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    print("=" * 70)
    print("ENDPOINT: GetAllDSSDistrict")
    print("STATUS:", response.status_code)
    print("URL:", response.url)

    print("\nRESPONSE:")
    print(response.text[:15000])

    if response.status_code == 200:
        try:
            data = response.json()

            print("\n\nJSON:")
            print(json.dumps(
                data,
                indent=2,
                ensure_ascii=False
            ))

        except Exception as e:
            print("\nJSON parsing error:", e)

except Exception as e:
    print("REQUEST ERROR:", e)