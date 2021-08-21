#!/usr/bin/env python3
import configparser
from pathlib import Path

import requests

config = configparser.ConfigParser()

config.read("config.ini")

API_KEY = config["Default"]["apikey"]
VEHICLE_TYPE = "hike"

URL = f"https://graphhopper.com/api/1/match"


for f in Path.cwd().glob("*.gpx"):
    with f.open() as fp:
        data = fp.read()
    response = requests.post(
        URL,
        data=data,
        headers={"Content-Type": "application/gpx+xml"},
        params={"vehicle": VEHICLE_TYPE, "key": API_KEY, "type": "gpx"},
    )
    response.raise_for_status()
    new_path = f.with_stem(f"{f.stem}_matched")
    with new_path.open("w") as fp:
        fp.write(response.text)
