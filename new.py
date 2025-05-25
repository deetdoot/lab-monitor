from ultralytics import YOLO
import csv
import requests
import json
from datetime import datetime

# Load an official or custom model
model = YOLO("yolo11n.pt")  # Load an official Detect model

# Perform tracking with the model
results = model.track(source=0, show=True, tracker="bytetrack.yaml", save=True, vid_stride = 1, classes = [0], stream= True)	 # with ByteTrack

API_URL = "http://localhost:5000/submit"  # Change to your actual API endpoint


for r in results:
    # Create a dictionary to hold the data
    instance_json = {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'): json.loads(r.to_json())}
    # Read existing data if file exists
    try:
      with open("instances.json", "r") as f:
        data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
      data = {}

    # Append new instance if changed
    if instance_json not in data.values():
      data.update(instance_json)
      with open("instances.json", "w") as f:
        json.dump(data, f, indent=4)
