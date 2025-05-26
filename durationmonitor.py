from datetime import datetime
import json
import time
import mysql.connector

class DurationMonitor:
    def __init__(self):
        self.start_times = {}
        self.durations = {}

    def process_frame(self, timestamp_str, detections):
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is not None:
                if track_id not in self.start_times:
                    self.start_times[track_id] = timestamp
                self.durations[track_id] = (timestamp - self.start_times[track_id]).total_seconds()

    def get_durations(self):
        return self.durations

# Example usage
if __name__ == "__main__":
    monitor = DurationMonitor()
    while True:
        with open("instances.json", "r") as f:
            while True:
                try:
                    data_stream = json.load(f)
                    break
                except json.JSONDecodeError:
                    f.seek(0)
                    time.sleep(0.1)

            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='1234',
                database='lab-monitor'
            )
            cursor = conn.cursor()

        # Process each frame in the data stream using its own timestamp from the JSON
        for timestamp, detections in data_stream.items():
            print(f"Timestamp: {timestamp}, Detections: {detections}")
            monitor.process_frame(timestamp, detections)

        durations = monitor.get_durations()
        for track_id, duration in durations.items():
            print(f"Track ID {track_id} duration: {duration:.2f} seconds")

        for track_id, duration in durations.items():
            # Check if the track_id already exists
            cursor.execute(
            '''
            SELECT Duration FROM PrimaryTable WHERE Track_ID = %s ORDER BY Timestamp DESC LIMIT 1
            ''',
            (track_id,)
            )
            result = cursor.fetchone()
            if result:
                # Update the existing duration
                new_duration = result[0] + duration
                cursor.execute(
                    '''
                    UPDATE PrimaryTable
                    SET Duration = %s, Timestamp = %s
                    WHERE Track_ID = %s
                    ''',
                    (new_duration, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), track_id)
                )
            else:
                # Insert as new
                cursor.execute(
                    '''
                    INSERT INTO PrimaryTable (Timestamp, Track_ID, Duration)
                    VALUES (%s, %s, %s)
                    ''',
                    (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), track_id, duration)
                )
        conn.commit()
        time.sleep(1)  # Sleep for a second before the next iteration
    
    conn.close()
