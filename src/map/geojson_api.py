from fastapi import FastAPI


app = FastAPI()

import json

sample_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "River Section 1"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [10.0, 50.0],
                        [10.4, 50.1],
                        [10.3, 50.3],
                        [10.5, 50.5],
                        [10.7, 50.7],
                        [10.2, 50.8],
                        [10.1, 50.6],
                        [10.1, 50.6],
                        [9.9, 50.2],
                        [10.0, 50.0]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "River Section 4 (Connected to Section 3)"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [11.0, 50.4], 
                        [10.7, 50.5],
                        [10.5, 50.5],
                        [10.7, 50.7],
                        [11.2, 50.5], 
                        [11.3, 50.2],
                        [11.1, 50]
                        
                    ]
                ]
            }
        }
    ]
}






@app.get("/output")
async def root():
    return {"data": sample_geojson}