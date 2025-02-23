import streamlit as st
import streamlit.components.v1 as components

# Streamlit app
st.title("Exaggerated Elevation WebScene with Cesium")

# Cesium HTML template
cesium_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cesium</title>
    <script src="https://cesium.com/downloads/cesiumjs/releases/1.88/Build/Cesium/Cesium.js"></script>
    <link href="https://cesium.com/downloads/cesiumjs/releases/1.88/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
    <style>
        #cesiumContainer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
    </style>
</head>
<body>
    <div id="cesiumContainer"></div>
    <script>
        Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIxOTFhZTVmZi1hNzVmLTQ4MWYtYWZkMC04ZWJmMmViZmM5MTgiLCJpZCI6Mjc4MzMzLCJpYXQiOjE3NDAyODQxNDZ9.YkN71tVYUgvc8vG88JrCIrcp6Vhjvk38ga_v7MvSp_k';
        var viewer = new Cesium.Viewer('cesiumContainer', {
            terrainProvider: new Cesium.CesiumTerrainProvider({
                url: Cesium.IonResource.fromAssetId(eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIxOTFhZTVmZi1hNzVmLTQ4MWYtYWZkMC04ZWJmMmViZmM5MTgiLCJpZCI6Mjc4MzMzLCJpYXQiOjE3NDAyODQxNDZ9.YkN71tVYUgvc8vG88JrCIrcp6Vhjvk38ga_v7MvSp_k),
                requestVertexNormals: true
            })
        });

        var exaggeration = 70;
        viewer.scene.globe.terrainExaggeration = exaggeration;

        viewer.scene.globe.enableLighting = true;
    </script>
</body>
</html>
"""

# Display the Cesium scene
components.html(cesium_html, height=600)
