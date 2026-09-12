import json
import os

geojson_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Alur_Survey_63_WGS84.geojson"
)

html_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Alur_Survey_63_map.html"
)

with open(geojson_file, "r", encoding="utf-8") as f:
    geojson = json.load(f)

geojson_text = json.dumps(geojson)

html = f"""
<!DOCTYPE html>
<html>
<head>

    <meta charset="UTF-8">

    <title>Alur Survey 63</title>

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <link
        rel="stylesheet"
        href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    />

    <style>

        #map {{
            height: 100vh;
            width: 100%;
        }}

        body {{
            margin: 0;
        }}

    </style>

</head>

<body>

<div id="map"></div>

<script
    src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js">
</script>

<script>

    const geojsonData = {geojson_text};

    const map = L.map('map');

    L.tileLayer(
        'https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',
        {{
            attribution: '&copy; OpenStreetMap contributors'
        }}
    ).addTo(map);

    const parcel = L.geoJSON(
        geojsonData,
        {{
            onEachFeature: function(feature, layer) {{

                layer.bindPopup(
                    "<b>Alur</b><br>" +
                    "Survey No: 63"
                );

            }}
        }}
    ).addTo(map);

    map.fitBounds(parcel.getBounds());

</script>

</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html)

print("Map created successfully!")
print()
print(html_file)
