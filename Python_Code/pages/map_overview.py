import streamlit as st
import streamlit.components.v1 as components

def st_cesium(height=600, token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIxOTFhZTVmZi1hNzVmLTQ4MWYtYWZkMC04ZWJmMmViZmM5MTgiLCJpZCI6Mjc4MzMzLCJpYXQiOjE3NDAyODQxNDZ9.YkN71tVYUgvc8vG88JrCIrcp6Vhjvk38ga_v7MvSp_k"):
    cesium_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cesium</title>
        <script src="https://cesium.com/downloads/cesiumjs/releases/1.83/Build/Cesium/Cesium.js"></script>
        <link href="https://cesium.com/downloads/cesiumjs/releases/1.83/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
        <style>
            #cesiumContainer {{
                width: 100%;
                height: {height}px;
                margin: 0;
                padding: 0;
                overflow: hidden;
            }}
        </style>
    </head>
    <body>
        <div id="cesiumContainer"></div>
        <script>
            Cesium.Ion.defaultAccessToken = '{token}';
            var viewer = new Cesium.Viewer('cesiumContainer', {{
                terrainProvider: Cesium.createWorldTerrain(),
                geocoder: true
            }});

            viewer.geocoder.viewModel.search.beforeExecute.addEventListener(function(e) {{
                var query = e.query;
                fetch('/search', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{query: query}})
                }})
                .then(response => response.json())
                .then(data => {{
                    console.log(data);
                }});
            }});
        </script>
    </body>
    </html>
    """
    components.html(cesium_html, height=height)

# Use the custom st_cesium function

# Set the page title
st.title("Map Overview Of Wildlife Reports")

# Display the Cesium 3D Earth model with your token
st_cesium(height=600, token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIxOTFhZTVmZi1hNzVmLTQ4MWYtYWZkMC04ZWJmMmViZmM5MTgiLCJpZCI6Mjc4MzMzLCJpYXQiOjE3NDAyODQxNDZ9.YkN71tVYUgvc8vG88JrCIrcp6Vhjvk38ga_v7MvSp_k")
# Add a text input for the city
city = st.text_input("Enter city name:")

# Add a selectbox for the animal
animal = st.selectbox("Select animal:", ["Tiger", "Elephant", "Leopard", "Bear", "Deer"])

# Display the selected city and animal
if city and animal:
    st.write(f"City: {city}")
    st.write(f"Animal: {animal}")

    # Add JavaScript to display the city and animal on the map
    cesium_js = f"""
    <script>
        var city = '{city}';
        var animal = '{animal}';
        viewer.entities.add({{
            name: animal,
            position: Cesium.Cartesian3.fromDegrees(-75.1641667, 39.9522222), // Example coordinates
            point: {{
                pixelSize: 10,
                color: Cesium.Color.RED
            }},
            label: {{
                text: animal,
                font: '14pt monospace',
                style: Cesium.LabelStyle.FILL_AND_OUTLINE,
                outlineWidth: 2,
                verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
                pixelOffset: new Cesium.Cartesian2(0, -9)
            }}
        }});
    </script>
    """
    components.html(cesium_js, height=0)