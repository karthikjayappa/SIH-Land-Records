import json
import os

folder = os.path.dirname(os.path.abspath(__file__))

geojson_file = os.path.join(
    folder,
    "Alur_All_Real_Parcels_WGS84.geojson"
)

html_file = os.path.join(
    folder,
    "Alur_All_Real_Parcels_map.html"
)

with open(geojson_file, "r", encoding="utf-8") as f:
    geojson = json.load(f)

geojson_text = json.dumps(geojson)

html = f"""
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<title>Alur Real LRI Parcels</title>

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<link
rel="stylesheet"
href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
/>

<style>

html, body {{
    margin: 0;
    height: 100%;
}}

#map {{
    height: 100%;
    width: 100%;
}}

.info {{
    position: absolute;
    top: 10px;
    left: 50px;
    z-index: 1000;
    background: white;
    padding: 10px;
    border-radius: 5px;
    box-shadow: 0 1px 5px rgba(0,0,0,0.3);
}}

</style>

</head>

<body>

<div class="info">
    <b>Alur - Karnataka LRI</b><br>
    Real LRI spatial features: {len(geojson["features"])}
</div>

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


const parcels = L.geoJSON(
    geojsonData,
    {{

        onEachFeature: function(feature, layer) {{

            const properties = feature.properties || {{}};

            const survey =
                properties.survey_number || "Unknown";

            layer.bindPopup(
                "<b>Alur</b><br>" +
                "Survey No: " + survey + "<br>" +
                "Source: Karnataka LRI"
            );

            layer.on({{

                mouseover: function(e) {{
                    e.target.setStyle({{
                        weight: 3
                    }});
                }},

                mouseout: function(e) {{
                    parcels.resetStyle(e.target);
                }}

            }});

        }}

    }}
).addTo(map);


map.fitBounds(parcels.getBounds());

</script>

</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html)

print("Map created successfully!")
print()
print("Features:", len(geojson["features"]))
print()
print("Saved:")
print(html_file)