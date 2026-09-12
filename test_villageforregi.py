import requests
import json

BASE_API = "https://mobservice.sujala3lri.karnataka.gov.in/api"

hoblis = ["ANAGODU", "KASABA", "MAYAKONDA"]

for hobli in hoblis:

    print("\n" + "=" * 70)
    print("HOBLI:", hobli)
    print("=" * 70)

    url = f"{BASE_API}/GetVillageforRegi"

    params = {
        "hobliID": hobli,
        "talukID": "Davanagere",
        "district": "Davanagere",
        "culture": 1
    }

    try:
        response = requests.get(url, params=params, timeout=30)

        print("STATUS:", response.status_code)
        print("URL:", response.url)

        if response.status_code == 200:

            data = response.json()

            print("\nTOTAL RECORDS:", len(data))

            print("\nSEARCHING FOR SHAYAMANURU...\n")

            found = False

            for village in data:

                text = json.dumps(village, ensure_ascii=False)

                if (
                    "Shayamanuru" in text
                    or "ಶಾಯಮಾನೂರು" in text
                ):
                    print("FOUND:")
                    print(json.dumps(
                        village,
                        indent=2,
                        ensure_ascii=False
                    ))

                    found = True

            if not found:
                print("Shayamanuru NOT FOUND")

                print("\nFIRST RECORD:")
                if data:
                    print(json.dumps(
                        data[0],
                        indent=2,
                        ensure_ascii=False
                    ))

        else:
            print("ERROR RESPONSE:")
            print(response.text[:2000])

    except Exception as e:
        print("ERROR:", e)