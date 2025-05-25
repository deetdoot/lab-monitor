from datetime import datetime
from collections import defaultdict
import json

class DurationMonitor:
    def __init__(self):
        self.track_data = defaultdict(lambda: {"first_seen": None, "last_seen": None})

    def process_frame(self, timestamp_str, detections):
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")

        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is not None:
                if self.track_data[track_id]["first_seen"] is None:
                    self.track_data[track_id]["first_seen"] = timestamp
                self.track_data[track_id]["last_seen"] = timestamp

    def get_durations(self):
        durations = {}
        for track_id, times in self.track_data.items():
            if times["first_seen"] and times["last_seen"]:
                durations[track_id] = (times["last_seen"] - times["first_seen"]).total_seconds()
        return durations

# Example usage
if __name__ == "__main__":
    monitor = DurationMonitor()

    with open("instances.json", "r") as f:
        data_stream = json.load(f)


    for timestamp_str, detections in data_stream.items():
        print(f"Timestamp: {timestamp_str}, Detections: {detections}")
        monitor.process_frame(timestamp_str, detections)

    durations = monitor.get_durations()
    for track_id, duration in durations.items():
        print(f"Track ID {track_id} duration: {duration:.2f} seconds")
