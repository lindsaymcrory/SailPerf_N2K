# SailPerf N2K - NMEA2000 Sailing Performance Analysis Tool
# Copyright 2025 OceanPilot
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Attribution Notice:
# This software was created as part of the OceanPilot initiative and is
# distributed under the Apache License 2.0. If you use this code, please
# attribute it to "N2K Sail Perf by OceanPilot."


import datetime 
import sqlite3
import os

class SensorPipeline:
    """ 
    Collect data from the stream (or inidvidual records) and log.

    SensorLogPipeline performs the following: 
     * collects the individual sensor data an maps it to single common field.
       Needed as different NMEA sentences can provide the same data.
       i.e. heading_m is provided by both $IIVHW and $HCHDM sentences.    
     * Log to file 
     """
    
    verbose_logging = True                  # Log sensor data in dictionary forme for debugging 
    # current (last read) values
    sensors = { "boat_speed_nm":0,          # boat speed in knots
               "depth_m":0,                 # Depth below transducer in meters
               "turnrate_deg":0,            # Rate of turn in degrees per minute          
               "heading_mag":0,        # compass heading magnetic ( 0 ~ 369 ) 
               "deviation_deg":0,      # Magnetic Deviation in degrees (optional).
               "deviation_dir":0,      # Magnetic Deviation direction 'E'ast or 'W'est.
               "variation_deg":0,      # Magnetic variation in degrees (optional)
               "variation_dir":0,      # Magnetic variation direction 'E'ast or 'W'est.
               "heading_true":0,
 

               "latitude":0,                # current lat: 44.65252
               "longitude":0,               # current lon: -63.4722
               "gpgll_time":0,              # last GPS update 220102.5: UTC time (22:01:02.5). Used to order other readings.
               "wind_angle_rel":0, # wind angle relative to the vessel’s bow
               "wind_speed_true_nm":0,       # wind speed in knots 
               "wind_dir_ref":'R',     # Wind direction relative to the vessel L or R (Left or Right)
               "wind_speed_apparent_nm":0,    # apparent wind speed
               "wind_speed_units":""          # Unit of wind speed: K: Kilometers per hour	M: Meters per second N: Knots

               }
    
    """
    Status contains session level information.
    """
    
    session_status = {
            "check_sum_errors":0,
            "updates":0,  
            "time_start":0,
            "time_last":0
    }
    
    
    """ 
    Session Counters
    Use primarily for debugging and status information. 
    A session can be:
        Reading a Log file, session ending when the last  record is read.  
        Reading from a W2K-1, session ending when the power is turned off.
        Reading from a N2K, session ending when the power is turned off.
    
    """
    sensor_counter = {}  # the number of updates for a sensor type
    nmea_function_counter = {} # count of talker IDs { "GPGAA":0, ..}
    #raw_nmea_headers= {} # #{ '$header':count,...} of all headers, including ones NOT processed.


    def add_nmea_function_counter(self, talker_id):
        """  
        Increment the number of times a talker_id was called during the session.
        Params:
            talker_id a valid NMEA talker id : GPGAA, GPGLL,GPGNS
        return:
            None 
        """
        self.nmea_function_counter[talker_id] = self.nmea_function_counter.get(talker_id,0) + 1
        return
    
    
    def insert_tracks(self):
        """ 
        
        """
        log_sensors = ["gpgll_time","latitude","longitude","heading_true","heading_mag","boat_speed_nm",
                       "wind_speed_true_nm", "wind_dir_ref" ,"wind_speed_apparent_nm" ]
       
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
            INSERT INTO tracks (timestamp, {", ".join(log_sensors)})
            VALUES (?, {", ".join(["?" for _ in log_sensors])})
        """

        # Execute query with values
        self.cursor.execute(sql, [timestamp] + values)
        self.conn.commit()

        return
  


    
    def append_log(self):
        """
        Append log with sensor. 
        This is called when a Trigger sensor indicates that the sequence has started again. 
        """
        
        
        sensors_to_log = ['gpgll_time','latitude','longitude','boat_speed_nm','heading_true','depth_m']

        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y%m%d %H:%M:%S.%f")[:-3]
        
        
        log_rec = formatted_datetime

        if self.verbose_logging is True:
            for sensor_label in self.sensors:
                log_rec += ", " + sensor_label +"="+str(self.sensors[sensor_label])
                log_rec += "\n"
        
        else:
            log_rec += ","+ str(self.sensors['latitude']) + "," + str(self.sensors['longitude'])


        log_file = open('SP_N2K_LOG.txt',"a")
        log_file.write(log_rec)
        log_file.close()
    

    #def add_raw_nmea_header(self, header):
    #    """
    #    Adds a NMEA header for counting. All headers, including headers 
    #    that are NOT processed with a handler are counted. This helps idenify new 
    #    devices on the network.  
    #    """
    #    self.raw_nmea_headers[header] = self.raw_nmea_headers.get(header,0) + 1 
    #    return
    
    
    def increment_checksum_errors(self):
        """ 
        Adds 1 to the number of checksum errors for the session.
        Params: 
            None
        Returns:
            None
        """
        self.session_status['check_sum_errors'] = self.session_status.get('check_sum_errors',0) + 1
        return   
    
    
    def add_reading(self, sensor_type_label, sensor_value):
        """ 
        Adds a value to the appropriate type of sensor and determines if a record can be written.      
        The same sensor types (like boat speed or lat/lon) can come from multiple NMEA Talker IDs.            
        """
        # time updates
        
        self.session_status['time_last'] = datetime.datetime.now()
        if self.session_status['time_start'] == 0:
            self.session_status['time_start'] = datetime.datetime.now()

        self.session_status['updates'] = self.session_status.get('updates',0)+1


        # Update the sensor value and count
        self.sensors[sensor_type_label] = sensor_value
        self.sensor_counter[sensor_type_label] = self.sensor_counter.get(sensor_type_label, 0) + 1

        # Handle numeric sensor values
        if isinstance(sensor_value, (int, float)) or (isinstance(sensor_value, str) and sensor_value.isdigit()):
            # Convert sensor_value to a numeric type if it's a string
            numeric_value = float(sensor_value) if isinstance(sensor_value, str) else sensor_value


        # gpgll_time' is the last fild of a GPGLL sentence.
        if sensor_type_label == 'gpgll_time':
            self.append_log()
            self.insert_tracks()
        return
    
    def insert_wind_log(self, wind_speed, wind_angle):
        """Inserts wind data into the database."""
        timestamp = datetime.datetime.now(datetime.UTC).isoformat()
        self.cursor.execute("INSERT INTO wind_log (timestamp, wind_speed, wind_angle) VALUES (?, ?, ?)",
                            (timestamp, wind_speed, wind_angle))
        self.conn.commit()
        return
    
    def insert_boat_speed_log(self, boat_speed):
        """Inserts boat speed data into the database."""
        timestamp = datetime.datetime.now(datetime.UTC).isoformat()
        self.cursor.execute("INSERT INTO boat_speed_log (timestamp, boat_speed) VALUES (?, ?)",
                            (timestamp, boat_speed))
        self.conn.commit()
        return
    
    def insert_gps_log(self, latitude, longitude):
        """Inserts GPS data into the database."""
        timestamp = datetime.datetime.now(datetime.UTC).isoformat()
        self.cursor.execute("INSERT INTO gps_log (timestamp, latitude, longitude) VALUES (?, ?, ?)",
                            (timestamp, latitude, longitude))
        self.conn.commit()
    
    def __init__(self):
        """ """
        relative_db_path = "./data/SailPerf_N2K.db"
        self.conn = sqlite3.connect(relative_db_path)
        self.cursor = self.conn.cursor()
        return
        

"""
The sensorpipeline instance is used by NMEAHandlers.py. server.py, NM0183.py.

"""
sensorpipeline = SensorPipeline()


if __name__ == "__main__":
    sensorpipeline.add_reading('latitude',44.44)
    sensorpipeline.insert_wind_data(10,25)
    print(sensorpipeline.session_status)