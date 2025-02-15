from fastapi import FastAPI
from main import main

app = FastAPI()

import json

@app.get("/output")
async def root():
    return main()
