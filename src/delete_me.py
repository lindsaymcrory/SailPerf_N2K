import sqlite3
import datetime

class WindLogger:
    def __init__(self, db_path="./data/SailPerf_N2K.db"):
        """Initialize the database connection."""
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def insert_windlog(self):
        """Insert wind sensor data from self.sensors into the wind_log table without utc_time."""

        log_sensors = [
            "gpgll_time", "latitude", "longitude", "heading_true", "heading_mag",
            "boat_speed_nm", "wind_speed_true_nm", "wind_dir_ref", "wind_speed_apparent_nm"
        ]

        # Ensure all required sensor values exist before inserting
        if not hasattr(self, "sensors") or any(key not in self.sensors for key in log_sensors):
            print("Error: Missing required sensor values in self.sensors.")
            return

        # Retrieve sensor values
        values = [self.sensors[sensor] for sensor in log_sensors]

        # Add system timestamp (ISO format)
        timestamp = datetime.datetime.now(datetime.UTC).isoformat()

        # Construct SQL query without utc_time
        sql = f"""
            INSERT INTO wind_log (timestamp, {", ".join(log_sensors)})
            VALUES (?, {", ".join(["?" for _ in log_sensors])})
        """

        # Execute query with values
        self.cursor.execute(sql, [timestamp] + values)
        self.conn.commit()
        print("Wind log entry added successfully.")

# Example usage
if __name__ == "__main__":
    logger = WindLogger()
    logger.sensors = {
        "gpgll_time": "2024-01-30 12:34:50",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "heading_true": 180,
        "heading_mag": 175,
        "boat_speed_nm": 6.2,
        "wind_speed_true_nm": 12.5,
        "wind_dir_ref": "T",
        "wind_speed_apparent_nm": 10.3
    }
    logger.insert_windlog()
