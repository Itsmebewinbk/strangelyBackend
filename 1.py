import folium

def create_map():
    # Extract first vehicle's coordinates for centering
    first_point = [18.549022, 73.790981]  # Default fallback
    
    vehicle_data = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "date": "2025-03-21T08:39:22Z",
        "pallet_id": "PLT101",
        "start_point": True
      },
      "geometry": {
        "type": "Point",
        "coordinates": [73.790981, 18.549022]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "date": "2025-03-24T05:06:37Z",
        "pallet_id": "PLT101",
        "error_code": "E404",
        "error_description": "Pallet Offline"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [73.7909291666667, 18.5490968333333]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "date": "2025-03-24T06:59:36Z",
        "pallet_id": "PLT101",
        "error_code": "E404",
        "error_description": "Pallet Offline"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [73.7909381666667, 18.549057]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "date": "2025-03-24T07:24:20Z",
        "pallet_id": "PLT101",
        "error_code": "E404",
        "error_description": "Pallet Offline"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [73.790971, 18.5492246666667]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "date": "2025-03-24T07:35:29Z",
        "pallet_id": "PLT101",
        "error_code": "E404",
        "error_description": "Pallet Offline"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [73.7910835, 18.5489095]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "date": "2025-03-24T08:22:08Z",
        "pallet_id": "PLT101",
        "error_code": "E404",
        "error_description": "Pallet Offline"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [73.790885, 18.5489701666667]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "date": "2025-03-24T08:45:43Z",
        "pallet_id": "PLT101",
        "error_code": "E404",
        "error_description": "Pallet Offline"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [73.7909026666667, 18.5490361666667]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "date": "2025-03-24T09:36:31Z",
        "pallet_id": "PLT101",
        "error_code": "E404",
        "error_description": "Pallet Offline"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [73.7909813333333, 18.5491456666667]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "date": "2025-03-24T09:57:02Z",
        "pallet_id": "PLT101",
        "error_code": "E404",
        "error_description": "Pallet Offline"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [73.7909233333333, 18.5490466666667]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "date": "2025-03-24T10:29:57Z",
        "pallet_id": "PLT101",
        "error_code": "E404",
        "error_description": "Pallet Offline"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [73.7909441666667, 18.5490411666667]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "date": "2025-03-24T11:13:43Z",
        "pallet_id": "PLT101",
        "error_code": "E404",
        "error_description": "Pallet Offline"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [73.790942, 18.5489768333333]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "date": "2025-03-24T11:26:12Z",
        "pallet_id": "PLT101",
        "error_code": "E404",
        "error_description": "Pallet Offline"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [73.7909036666667, 18.5489983333333]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "date": "2025-03-24T11:26:12Z",
        "pallet_id": "PLT101",
        "end_point": True
      },
      "geometry": {
        "type": "Point",
        "coordinates": [73.7909036666667, 18.5489983333333]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "pallet_id": "PLT101"
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [73.7909248333333, 18.5489196666667],
          [73.7908588333333, 18.5487183333333],
          [73.7908633333333, 18.548753],
          [73.7908626666667, 18.5487635],
          [73.7909366666667, 18.5490638333333],
          [73.7909346666667, 18.5490495],
          [73.790945, 18.5490391666667],
          [73.790947, 18.5490506666667],
          [73.7910181666667, 18.549173],
          [73.7910253333333, 18.5491663333333],
          [73.7909096666667, 18.5492936666667],
          [73.790926, 18.5493231666667],
          [73.7909505, 18.5493723333333],
          [73.7909758333333, 18.5493968333333],
          [73.790986, 18.5494031666667],
          [73.790977, 18.5493923333333],
          [73.7909656666667, 18.5493813333333],
          [73.790966, 18.5493713333333],
          [73.7909575, 18.5493393333333],
          [73.7909471666667, 18.5493163333333],
          [73.7909491666667, 18.5492953333333],
          [73.79097, 18.5492648333333],
          [73.7910896666667, 18.5489271666667],
          [73.7911195, 18.5489146666667],
          [73.7908966666667, 18.5487196666667],
          [73.790914, 18.5490403333333],
          [73.7909075, 18.5490293333333],
          [73.7909038333333, 18.5490381666667],
          [73.7912596666667, 18.5485515],
          [73.7912623333333, 18.5485735],
          [73.7909783333333, 18.5490686666667],
          [73.790818, 18.5488383333333],
          [73.7909491666667, 18.549052],
          [73.790935, 18.5490323333333],
          [73.7909558333333, 18.5490701666667],
          [73.7909346666667, 18.5490518333333],
          [73.7909321666667, 18.5490406666667],
          [73.7909195, 18.5490446666667],
          [73.7909005, 18.54905],
          [73.79091, 18.5490531666667],
          [73.7909208333333, 18.5490488333333],
          [73.790925, 18.5490316666667],
          [73.7909325, 18.5490373333333],
          [73.7909233333333, 18.5490441666667],
          [73.7909266666667, 18.5490348333333],
          [73.7909888333333, 18.5489475],
          [73.7909966666667, 18.5489921666667],
          [73.7910061666667, 18.5489931666667],
          [73.7909915, 18.548977],
          [73.790987, 18.5489915],
          [73.7909825, 18.549001],
          [73.790972, 18.5490046666667],
          [73.7909613333333, 18.5490113333333],
          [73.790957, 18.5490208333333],
          [73.7909531666667, 18.5490325],
          [73.7909465, 18.5490411666667],
          [73.790951, 18.5490541666667],
          [73.7909373333334, 18.5490603333333],
          [73.7909411666667, 18.5490508333333],
          [73.7909453333333, 18.5490413333333],
          [73.7910905, 18.5489021666667],
          [73.7910491666667, 18.5489035],
          [73.7910435, 18.548912],
          [73.7910291666667, 18.5489193333333],
          [73.7910158333333, 18.5489325],
          [73.7910041666667, 18.5489491666667],
          [73.7910018333333, 18.5489588333333],
          [73.7909171666667, 18.5489733333333],
          [73.7909266666667, 18.5489825],
          [73.7909403333333, 18.5489803333333],
          [73.7909501666667, 18.5489796666667],
          [73.7909625, 18.5489838333333],
          [73.7909716666667, 18.5489891666667],
          [73.7909746666667, 18.5489805],
          [73.790985, 18.5489693333333],
          [73.7909905, 18.5489588333333],
          [73.7909788333333, 18.5489638333333],
          [73.7909648333333, 18.548957],
          [73.7909541666667, 18.5489553333333],
          [73.7909505, 18.5489663333333],
          [73.7909451666667, 18.5489741666667],
          [73.7908926666667, 18.549074],
          [73.7909011666667, 18.5490631666667],
          [73.7908941666667, 18.5490373333333],
          [73.7909003333333, 18.5490248333333],
          [73.7908911666667, 18.5490338333333],
          [73.7908961666667, 18.5490203333333],
          [73.7909015, 18.5490125],
          [73.7909108333333, 18.5490075]
        ]
      }
    }
  ]
}

    # Update first_point if data exists
    if vehicle_data["features"]:
        first_feature = vehicle_data["features"][0]
        if first_feature["geometry"]["type"] == "Point":
            first_point = list(reversed(first_feature["geometry"]["coordinates"]))  # Reverse to (lat, lon)

    # Create map centered at the first vehicle's position
    m = folium.Map(
        location=first_point,
        zoom_start=12,
        tiles="https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYmV3aW4tYmFidS1lY2luZm9zb2x1dGlvbnMiLCJhIjoiY204cXg3dmlsMGk3MjJxczh0cXh1MDdsZSJ9.rsJxBPMqiTRz25yza9pF3Q",
        attr="Mapbox"
    )

    # Add vehicle data to the map
    folium.GeoJson(
        vehicle_data,
        name="vehicles"
    ).add_to(m)

    # Save map to an HTML file
    map_filename = "gps_tracking_map.html"
    m.save(map_filename)
    print(f"Map has been saved as {map_filename}. Open this file in your browser to view the map.")

if __name__ == "__main__":
    create_map()