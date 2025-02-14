from fastapi import FastAPI


app = FastAPI()

import json

sample_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Sample Location"},
            "geometry": {
                "type": "Point",
                "coordinates": [10.0, 50.0]  # [longitude, latitude]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Sample Polygon"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [10.0, 50.0],
                        [10.5, 50.0],
                        [10.5, 50.5],
                        [10.0, 50.5],
                        [10.0, 50.0]
                    ]
                ]
            }
        }
    ]
}




@app.get("/output")
async def root():
    return {"data": sample_geojson}