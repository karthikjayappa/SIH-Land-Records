import json
import time
import urllib.error
import urllib.parse
import urllib.request


# ============================================================
# SETTINGS
# ============================================================

BASE = "https://mobservice.sujala3lri.karnataka.gov.in/api"

TIMEOUT = 90
CULTURE = 1

TARGET_DISTRICT = "Davanagere"
TARGET_TALUK = "Davanagere"
TARGET_VILLAGE = "Shamanuru"


# ============================================================
# API REQUEST
# ============================================================

def get(endpoint, params):

    url = f"{BASE}/{endpoint}"

    print("\n================================================")
    print("GET")
    print(url)
    print("PARAMS:", params)
    print("================================================")

    try:

        query = urllib.parse.urlencode(params)

        full_url = f"{url}?{query}"

        request = urllib.request.Request(
            full_url,
            method="GET",
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=TIMEOUT
        ) as r:

            status = r.status
            final_url = r.geturl()

            text = r.read().decode(
                "utf-8",
                errors="replace"
            )

            print("STATUS:", status)
            print("URL:", final_url)

            if not text.strip():

                print("EMPTY RESPONSE")
                return None

            try:

                data = json.loads(text)

            except Exception:

                print("NOT JSON")
                print(text[:5000])

                return None

            return data

    except urllib.error.HTTPError as e:

        print("HTTP ERROR:", repr(e))

        try:

            error_text = e.read().decode(
                "utf-8",
                errors="replace"
            )

            print(error_text[:5000])

        except Exception:

            pass

        return None

    except Exception as e:

        print("ERROR:", repr(e))

        return None


# ============================================================
# SAVE JSON
# ============================================================

def save(filename, data):

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("\nSAVED:", filename)


# ============================================================
# PRINT JSON
# ============================================================

def show(data):

    print(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )
    )


# ============================================================
# FIND LIST INSIDE RESPONSE
# ============================================================

def extract_list(data):

    if isinstance(data, list):

        return data

    if isinstance(data, dict):

        possible_fields = [

            "list",
            "List",

            "data",
            "Data",

            "items",
            "Items",

            "talukList",
            "TalukList",

            "hobliList",
            "HobliList",

            "villageList",
            "VillageList",

            "dssVillageList",
            "DSSVillageList"

        ]

        for field in possible_fields:

            value = data.get(field)

            if isinstance(value, list):

                return value

        # If no known field,
        # search all dictionary values

        for value in data.values():

            if isinstance(value, list):

                return value

    return []


# ============================================================
# PRINT OBJECTS
# ============================================================

def print_codes(data, title):

    print("\n\n==============================")
    print(title)
    print("==============================")

    items = extract_list(data)

    if items:

        for i, item in enumerate(items):

            print(f"\n[{i}]")

            if isinstance(item, dict):

                for k, v in item.items():

                    print(f"{k}: {v}")

            else:

                print(item)

    else:

        show(data)


# ============================================================
# FIND OBJECT BY ANY FIELD
# ============================================================

def find_location(data, target, fields):

    target = str(target).strip().lower()

    result = []

    def walk(obj):

        if isinstance(obj, list):

            for item in obj:

                walk(item)

        elif isinstance(obj, dict):

            # Check this object

            for field in fields:

                if field in obj:

                    value = obj[field]

                    if value is not None:

                        value = str(value).strip().lower()

                        if value == target:

                            result.append(obj)

                            return

            # Search nested values

            for value in obj.values():

                if isinstance(value, (dict, list)):

                    walk(value)

    walk(data)

    return result


# ============================================================
# FIND VALUE RECURSIVELY
# ============================================================

def find_value(data, fields):

    found = []

    def walk(obj):

        if isinstance(obj, dict):

            for key, value in obj.items():

                if key in fields and value is not None:

                    found.append(
                        (key, value)
                    )

                if isinstance(value, (dict, list)):

                    walk(value)

        elif isinstance(obj, list):

            for item in obj:

                walk(item)

    walk(data)

    return found


# ============================================================
# 1. DESKTOP DISTRICTS
# ============================================================

print("\n\n############################################")
print("# 1. DESKTOP DISTRICTS")
print("############################################")


districts = get(
    "GetdesktopDistrict",
    {
        "culture": CULTURE
    }
)


if districts is None:

    print("Could not retrieve districts.")
    exit()


save(
    "01_desktop_districts.json",
    districts
)


print_codes(
    districts,
    "DISTRICTS"
)


# ============================================================
# FIND DAVANAGERE DISTRICT
# ============================================================

district_matches = find_location(
    districts,
    TARGET_DISTRICT,
    [
        "District_Code",
        "District_Name",

        "district_code",
        "district_name",

        "DistrictID",
        "District_Id",
        "districtId",

        "ID",
        "Id",

        "Name",
        "name"
    ]
)


print("\n\nDAVANAGERE DISTRICT MATCHES:")


if not district_matches:

    print("NO MATCH FOUND")

    print("\nAvailable Districts:")
    show(districts)

    exit()


for item in district_matches:

    show(item)


district = district_matches[0]


district_id = (

    district.get("District_Code")

    or district.get("DistrictID")

    or district.get("District_Id")

    or district.get("districtId")

    or district.get("ID")

    or district.get("Id")
)


print("\nDISTRICT ID/CODE:", district_id)


# ============================================================
# 2. DESKTOP TALUKS
# ============================================================

print("\n\n############################################")
print("# 2. DESKTOP TALUKS")
print("############################################")


taluks = get(
    "GetdesktopTaluk",
    {
        "district": district_id,
        "culture": CULTURE
    }
)


if taluks is None:

    print("Desktop Taluk failed.")
    exit()


save(
    "02_desktop_taluks.json",
    taluks
)


print_codes(
    taluks,
    "TALUKS"
)


# ============================================================
# FIND DAVANAGERE TALUK
# ============================================================

taluk_matches = find_location(
    taluks,
    TARGET_TALUK,
    [
        "Taluk_Code",
        "Taluk_Name",

        "TalukID",
        "Taluk_Id",

        "Taluka_Code",
        "Taluka_Name",

        "taluk_code",
        "taluk_name",

        "talukId",

        "ID",
        "Id",

        "Name",
        "name"
    ]
)


print("\n\nDAVANAGERE TALUK MATCHES:")


if not taluk_matches:

    print("NO MATCH FOUND")

    print("\nAvailable Taluks:")
    show(taluks)

    exit()


for item in taluk_matches:

    show(item)


taluk = taluk_matches[0]


taluk_id = (

    taluk.get("Taluk_Code")

    or taluk.get("TalukID")

    or taluk.get("Taluk_Id")

    or taluk.get("Taluka_Code")

    or taluk.get("talukId")

    or taluk.get("ID")

    or taluk.get("Id")
)


print("\nTALUK ID/CODE:", taluk_id)


# ============================================================
# 3. DESKTOP HOBLIS
# ============================================================

print("\n\n############################################")
print("# 3. DESKTOP HOBLIS")
print("############################################")


hoblis = get(
    "GetdesktopHobli",
    {
        "TalukID": taluk_id,
        "DistrictID": district_id,
        "culture": CULTURE
    }
)


if hoblis is None:

    print("Desktop Hobli failed.")
    exit()


save(
    "03_hoblis.json",
    hoblis
)


print_codes(
    hoblis,
    "HOBLIS"
)


# ============================================================
# EXTRACT HOBLI LIST
# ============================================================

hobli_list = extract_list(hoblis)


print(
    "\n\nNUMBER OF HOBLIS:",
    len(hobli_list)
)


# ============================================================
# 4. TEST DSS VILLAGE APIs
# ============================================================

print("\n\n############################################")
print("# 4. TESTING DSS VILLAGE APIs")
print("############################################")


village_found = None
village_hobli = None


for h in hobli_list:

    if not isinstance(h, dict):

        continue


    # --------------------------------------------------------
    # HOBLI ID
    # --------------------------------------------------------

    hobli_id = (

        h.get("KGISHobliID")

        or h.get("HobliID")

        or h.get("Hobli_Id")

        or h.get("Hobli_Code")

        or h.get("hobliId")

        or h.get("ID")

        or h.get("Id")
    )


    # --------------------------------------------------------
    # HOBLI NAME
    # --------------------------------------------------------

    hobli_name = (

        h.get("KGISHobliName")

        or h.get("HobliName")

        or h.get("Hobli_Name")

        or h.get("Name")

        or h.get("name")

        or ""
    )


    print("\n--------------------------------------------")
    print("HOBLI")
    print("ID   :", hobli_id)
    print("NAME :", hobli_name)
    print("--------------------------------------------")


    if hobli_id is None:

        print("No Hobli ID found.")
        continue


    # ========================================================
    # 4A. DSS VILLAGE
    # ========================================================

    print("\n\n>>> GET DSS VILLAGE")


    dss_villages = get(
        "GetDSSVillage",
        {
            "hobliID": hobli_id,
            "talukID": taluk_id,
            "culture": CULTURE
        }
    )


    if dss_villages is None:

        print(
            "GetDSSVillage returned no data."
        )

    else:

        save(
            f"dss_villages_{hobli_id}.json",
            dss_villages
        )


        print(
            "\nDSS VILLAGE RESPONSE:"
        )

        show(dss_villages)


    # ========================================================
    # SEARCH SHAMANURU IN DSS VILLAGE
    # ========================================================

    if dss_villages is not None:

        dss_matches = find_location(
            dss_villages,
            TARGET_VILLAGE,
            [

                "Village_Code",
                "Village_Name",

                "VillageID",
                "Village_Id",

                "village_code",
                "village_name",

                "villageId",

                "KGIVillageID",
                "KGIVillageName",

                "KGI_VillageID",
                "KGI_VillageName",

                "VillageCode",
                "VillageName",

                "DSSVillageID",
                "DSSVillageName",

                "DSS_VillageID",
                "DSS_VillageName",

                "ID",
                "Id",

                "Name",
                "name"
            ]
        )


        if dss_matches:

            print("\n\n############################################")
            print("# SHAMANURU FOUND IN DSS VILLAGE!")
            print("############################################")


            for m in dss_matches:

                show(m)


            village_found = dss_matches[0]
            village_hobli = h

            save(
                "04_shamanuru.json",
                village_found
            )

            break


    # ========================================================
    # 4B. DSS VILLAGE + WATERSHED
    # ========================================================

    print("\n\n>>> GET DSS VILLAGE + WATERSHED")


    dss_watershed = get(
        "GetDSSVillageAndWatershed",
        {
            "hobliID": hobli_id,
            "talukID": taluk_id,
            "culture": CULTURE
        }
    )


    if dss_watershed is None:

        print(
            "GetDSSVillageAndWatershed returned no data."
        )

    else:

        save(
            f"dss_villages_watershed_{hobli_id}.json",
            dss_watershed
        )


        print(
            "\nDSS VILLAGE + WATERSHED RESPONSE:"
        )

        show(dss_watershed)


    # ========================================================
    # SEARCH SHAMANURU IN DSS WATERSHED
    # ========================================================

    if dss_watershed is not None:

        watershed_matches = find_location(
            dss_watershed,
            TARGET_VILLAGE,
            [

                "Village_Code",
                "Village_Name",

                "VillageID",
                "Village_Id",

                "village_code",
                "village_name",

                "villageId",

                "KGIVillageID",
                "KGIVillageName",

                "KGI_VillageID",
                "KGI_VillageName",

                "VillageCode",
                "VillageName",

                "DSSVillageID",
                "DSSVillageName",

                "DSS_VillageID",
                "DSS_VillageName",

                "WatershedVillageID",
                "WatershedVillageName",

                "ID",
                "Id",

                "Name",
                "name"
            ]
        )


        if watershed_matches:

            print("\n\n############################################")
            print("# SHAMANURU FOUND IN DSS WATERSHED!")
            print("############################################")


            for m in watershed_matches:

                show(m)


            village_found = watershed_matches[0]
            village_hobli = h

            save(
                "04_shamanuru.json",
                village_found
            )

            break


    print(
        "\nShamanuru not found in this Hobli."
    )


    time.sleep(0.5)


# ============================================================
# 5. VILLAGE RESULT
# ============================================================

if village_found is None:

    print("\n\n############################################")
    print("# SHAMANURU NOT FOUND")
    print("############################################")

    print(
        """
The District → Taluk → Hobli hierarchy
was successfully resolved.

However, Shamanuru was not found
inside the DSS Village responses.

The following files were saved:

    dss_villages_ANAGODU.json
    dss_villages_KASABA.json
    dss_villages_MAYAKONDA.json

and, if returned:

    dss_villages_watershed_ANAGODU.json
    dss_villages_watershed_KASABA.json
    dss_villages_watershed_MAYAKONDA.json

We need to inspect the actual DSS
response schema before continuing.
"""
    )

    exit()


# ============================================================
# 6. EXTRACT VILLAGE ID
# ============================================================

village_id = (

    village_found.get("Village_Code")

    or village_found.get("VillageID")

    or village_found.get("Village_Id")

    or village_found.get("villageId")

    or village_found.get("KGIVillageID")

    or village_found.get("KGI_VillageID")

    or village_found.get("DSSVillageID")

    or village_found.get("DSS_VillageID")

    or village_found.get("ID")

    or village_found.get("Id")
)


# ============================================================
# 7. EXTRACT VILLAGE NAME
# ============================================================

village_name = (

    village_found.get("Village_Name")

    or village_found.get("VillageName")

    or village_found.get("village_name")

    or village_found.get("KGIVillageName")

    or village_found.get("KGI_VillageName")

    or village_found.get("DSSVillageName")

    or village_found.get("DSS_VillageName")

    or village_found.get("Name")

    or village_found.get("name")
)


# ============================================================
# 8. HOBLI ID
# ============================================================

hobli_id = (

    village_hobli.get("KGISHobliID")

    or village_hobli.get("HobliID")

    or village_hobli.get("Hobli_Id")

    or village_hobli.get("Hobli_Code")

    or village_hobli.get("hobliId")

    or village_hobli.get("ID")

    or village_hobli.get("Id")
)


# ============================================================
# 9. RESOLVED LOCATION
# ============================================================

print("\n\n############################################")
print("# RESOLVED LOCATION")
print("############################################")


print("District    :", TARGET_DISTRICT)
print("District ID :", district_id)

print("Taluk       :", TARGET_TALUK)
print("Taluk ID    :", taluk_id)

print("Hobli       :", village_hobli.get(
    "KGISHobliName",
    ""
))

print("Hobli ID    :", hobli_id)

print("Village     :", village_name)
print("Village ID  :", village_id)


# ============================================================
# 10. SHOW ALL POSSIBLE IDs/CODES
# ============================================================

print("\n\n############################################")
print("# POSSIBLE VILLAGE IDENTIFIERS")
print("############################################")


possible_ids = find_value(
    village_found,
    [

        "Village_Code",
        "VillageID",
        "Village_Id",

        "village_code",
        "villageId",

        "KGIVillageID",
        "KGI_VillageID",

        "DSSVillageID",
        "DSS_VillageID",

        "VillageCode",

        "ID",
        "Id"
    ]
)


if possible_ids:

    for key, value in possible_ids:

        print(
            f"{key}: {value}"
        )

else:

    print(
        "No standard village ID field found."
    )


# ============================================================
# 11. SAVE FINAL LOCATION INFORMATION
# ============================================================

location_info = {

    "district": TARGET_DISTRICT,

    "district_id": district_id,

    "taluk": TARGET_TALUK,

    "taluk_id": taluk_id,

    "hobli": village_hobli.get(
        "KGISHobliName"
    ),

    "hobli_id": hobli_id,

    "village": village_name,

    "village_id": village_id,

    "raw_village_record": village_found

}


save(
    "05_resolved_shamanuru_location.json",
    location_info
)


# ============================================================
# 12. COMPLETE
# ============================================================

print("\n\n############################################")
print("# LOCATION SEARCH COMPLETE")
print("############################################")


print(
    """
Resolved hierarchy:

Davanagere District
        ↓
Davanagere Taluk
        ↓
Correct Hobli
        ↓
Shamanuru
        ↓
Village ID / Code

Next step:

Village ID / WSCODE
        ↓
GetdssSurvey
        ↓
Survey numbers
        ↓
Cadastral ID
        ↓
GetCadastral
        ↓
Actual parcel geometry
"""
)