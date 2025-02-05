
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




import threading
import math
import time
import random  # for simulated values.

from NMEAHandlers import NMEAHandlers
#from SensorPipeline import sensorpipeline  # import the running class
from NMEAFileReader import FileReader 

class StreamReader:
    """ 
    
    The StreamReader class is responsible for reading NMEA 0183 and NMEA 2000 data from multiple sources and 
    forwarding it to a sensor pipeline for further processing. This enables the system to handle diverse data 
    sources and feed standardized data into a unified pipeline for logging, reporting, and visualization on a web server.

    The class supports:
        Simulated NMEA 0183 data generation for testing.
        Reading from an NMEA data file.
        Integration with an Actisense listener for real-time NMEA 2000 data.
        Validating and calculating NMEA checksums.
        Computing geographic distances and bearings between waypoints.

    """

    done_event = None        # Create an event to signal thread termination.
 
    simulated_waypoints = {} # will contain a sailing circle
    file_reader = None 

    def __init__(self):
        """ """

        self.done_event = threading.Event()  # Create an event to signal termination.
        self.nmea_handler = NMEAHandlers()
        self.file_reader = FileReader()
        self.create_simulated_waypoints()    # only needed if course simulation is used.
        
 
       

    def start_simulator_test(self,secs):
        """
        For testing, should only be used when called via: if __name__ == "__main__":
        
        """
        self.start_thread()
        time.sleep(secs)
        print("Thread SLeep Over")
        self.stop_thread()  
        return
    
    def create_simulated_waypoints(self):
        """ 
        Support simulation mode.
        """
        center_lat = 37.7749  # Latitude for San Francisco, CA
        center_lon = -122.4194  # Longitude for San Francisco, CA
        radius_nm = 1  # Radius of the circle in nautical miles

        # Generate circle points
        self.simulated_waypoints = self.calculate_circle_points(center_lat, center_lon, radius_nm)

        # Print some points
        #for angle, coords in list(circle.items())[:10]:  # Show the first 10 points
        #    print(f"Angle {angle}°: Latitude {coords[0]:.6f}, Longitude {coords[1]:.6f}")

        return

    
    
    
    
    def start_thread(self):
        """
        File worker threads read data from one of the following sources:
        1) simulate_worker_thread:   generates valid test data. 
        2) actisense_worker_thread:  listens (via socket) to a actisense_worker thread.
        3) file_read_worker_thread:  reads a file

        """
        #self.thread = threading.Thread(target=self.simulate_worker_thread, daemon=True)
        #self.thread = threading.Thread(target=self.actisense_worker_thread, daemon=True)
        
        self.thread = threading.Thread(target=self.file_read0183_worker_thread, daemon=True)
        self.thread.start()

    def stop_thread(self):
        self.done_event.set()  # Signal the thread to terminate.
        self.thread.join()  # Wait for the thread to finish.
    
    
    
    def test_check_sums(self):
        """ """
         # pass a known string with good check sum
        #$GPGLL,<Latitude>,<N/S>,<Longitude>,<E/W>,<UTC Time>,<Status>*<Checksum>
        
        tst1 = "$GPGLL,4439.1514,N,06328.3343,W,220102.5,A,A*4E"
        print("1) : ", tst1)
        print("2) Check validity  : ", self.validate_nmea_checksum(tst1))
        tst2 = "$GPGLL,4439.1514,N,06328.3343,W,220102.5"
        print("3) Remove status and check sum  : ", tst2)
        check_sum = self.calculate_nmea_checksum(tst2)
        print("4) Recalculate checksum: ",check_sum)
        tst2 += ",A,A*" + check_sum
        print("5) Check Validity of new String: ",self.validate_nmea_checksum(tst2))

        return

    
    
    def bearing_t(self,latitude1, longitude1, latitude2, longitude2):
        """
        Calculate the initial bearing between two points.
    
        Parameters:
            latitude1 (float): Latitude of the first point in degrees.
            longitude1 (float): Longitude of the first point in degrees.
            latitude2 (float): Latitude of the second point in degrees.
            longitude2 (float): Longitude of the second point in degrees.
    
        Returns:
            float: Bearing between the two points in degrees (0 to 360).
        """
        # Convert degrees to radians
        lat1_rad = math.radians(latitude1)
        lon1_rad = math.radians(longitude1)
        lat2_rad = math.radians(latitude2)
        lon2_rad = math.radians(longitude2)
    
        # Calculate bearing
        delta_lon = lon2_rad - lon1_rad
        x = math.sin(delta_lon) * math.cos(lat2_rad)
        y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon)
        initial_bearing = math.atan2(x, y)
    
        # Convert from radians to degrees and normalize to 0-360
        initial_bearing_deg = (math.degrees(initial_bearing) + 360) % 360
    
        return initial_bearing_deg
    
    
    def distance_nm(self,latitude1, longitude1, latitude2, longitude2):
        """
        Calculate the distance between two points in nautical miles.
    
        Parameters:
            latitude1 (float): Latitude of the first point in degrees.
            longitude1 (float): Longitude of the first point in degrees.
            latitude2 (float): Latitude of the second point in degrees.
            longitude2 (float): Longitude of the second point in degrees.
    
        Returns:
            float: Distance between the two points in nautical miles.
        """
        # Earth's radius in nautical miles
        earth_radius_nm = 3440.0
    
        # Convert degrees to radians
        lat1_rad = math.radians(latitude1)
        lon1_rad = math.radians(longitude1)
        lat2_rad = math.radians(latitude2)
        lon2_rad = math.radians(longitude2)
    
        # Haversine formula
        delta_lat = lat2_rad - lat1_rad
        delta_lon = lon2_rad - lon1_rad
        a = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = earth_radius_nm * c
        return distance
    
    
    def calculate_nmea_checksum(self,nmea_sentence):
        """
        Calculate the checksum for an NMEA 0183 sentence.
        Parameters:
            nmea_sentence (str): The NMEA sentence (without the checksum) starting with '$'.
    
        Returns:
            str: The calculated checksum as a two-character hexadecimal string.
        """
        # Ensure the sentence starts with '$' and does not include the existing checksum
        if nmea_sentence.startswith('$') and '*' in nmea_sentence:
            nmea_sentence = nmea_sentence.split('*')[0]

        # Remove the leading '$'
        nmea_data = nmea_sentence[1:]
    
        # Calculate the checksum by XORing all characters
        checksum = 0
        for char in nmea_data:
            checksum ^= ord(char)
    
        # Return the checksum as a two-character hexadecimal string
        return f"{checksum:02X}"
    
    
    def validate_nmea_checksum(self,nmea_sentence):
        """
        Validates the checksum of a given NMEA 0183 sentence.
    
        Parameters:
            nmea_sentence (str): The NMEA sentence to validate.
        
        Returns:
            bool: True if the checksum is valid, False otherwise.
        """
        # Ensure the sentence starts with '$' and contains '*'
        if not nmea_sentence.startswith("$") or "*" not in nmea_sentence:
            return False

        try:
            # Split the sentence into data and provided checksum
            data, provided_checksum = nmea_sentence[1:].split('*')
        
            # Compute the checksum by XORing all characters in the data
            calculated_checksum = 0
            for char in data:
                calculated_checksum ^= ord(char)
        
            # Convert the provided checksum to an integer
            provided_checksum = int(provided_checksum, 16)
        
            # Compare calculated checksum with the provided checksum
            return calculated_checksum == provided_checksum
        except ValueError:
        # Handle any parsing errors
            return False
    
    
    def actisense_worker_thread(self):
        """ This will call """
        return
    
    def file_read0183_worker_thread(self):
        """ 
        Read a file containing NMEA 0183 formated records. 

        """
        fileame = "../data/W2K_Log.txt"



        return

    
    
    
    def simulate_worker_thread(self):
        """
        use simulated data for testing.

        """
        sim_depth = list(range(5, 101, 10)) + list(range(95, 4, -10)) #
        simulator_counter = 0

        
        print(" *** update_thread  waypoint count: ",len(self.simulated_waypoints))
        while not self.done_event.is_set():  # Check if the event is set.
            simulator_counter += 1
            if  simulator_counter == len(self.simulated_waypoints):
                simulator_counter = 0

            from_wp = self.simulated_waypoints[simulator_counter] 

            to_wp_index = simulator_counter + 1  
            if to_wp_index == len(self.simulated_waypoints):
                to_wp_index = 0 # loop back to the begining
            to_wp = self.simulated_waypoints[to_wp_index]

            # update $GPGLL,<Latitude>,<N/S>,<Longitude>,<E/W>,<UTC Time>,<Status>*<Checksum>  
            tst1 = "$GPGLL,4439.1514,N,06328.3343,W,220102.5,A,A*4E"
            #print("Update lat/lon")
            self.nmea_handler.GPGLL(tst1)            
            time.sleep(.5)
            
            print("Update Depth")    # $SDDPT,,0,210*78
            valid_depth = sim_depth[(simulator_counter - 1) % len(sim_depth)]
            tst1 = "$SDDPT,"+str(valid_depth) +",0,210*"
            tst1 += self.calculate_nmea_checksum(tst1)
            self.nmea_handler.SDDPT(tst1) 
            time.sleep(.5)
            
            print("Update Compass / ")
            # $IIVHW,,T,43,M,0,N,0,K*52 # 
            """
               True Heading: Not provided.
		    Magnetic Heading: 43°.
		    Speed in Knots: 0.
		    Speed in km/h: 0.
            """
            tst1 = "$IIVHW,"
            tst1 += str(random.randint(0,360)) +",T,"   # True Heading
            tst1 += str(random.randint(0,360)) +",M,"   # Mag Heading
            tst1 += str(random.randint(1,5)) +",N,"   # Boat speed NM
            tst1 += str(random.randint(1,5)) +",K*"   # Boat speed KM + NMEA Terminator (*)
            tst1 += self.calculate_nmea_checksum(tst1)

            self.nmea_handler.IIVHW(tst1)
            time.sleep(.5)
            print("Update Wind")
 

        print("Thread UPDATE Thread COMPLETE")
        return


    
    
    def calculate_circle_points(self,center_lat, center_lon, radius_nm, num_points=360):
        """
        Calculate latitude and longitude points for a circle with radius in nautical miles.
    
        Parameters:
            center_lat (float): Latitude of the circle's center in degrees.
            center_lon (float): Longitude of the circle's center in degrees.
            radius_nm (float): Radius of the circle in nautical miles.
            num_points (int): Number of points in the circle (default is 360).
    
        Returns:
            dict: Dictionary with keys as angles (degrees) and values as (latitude, longitude) tuples.
        """
       
        earth_radius_nm = 3440.0  # Earth's radius in nautical miles
    
        circle_points = {}  # Dictionary to store the points
    
        # Loop through angles in degrees
        for angle in range(num_points):
            # Convert angle to radians
            angle_rad = math.radians(angle)
        
            # Calculate the offset in latitude and longitude
            delta_lat = (radius_nm / earth_radius_nm) * math.cos(angle_rad)
            delta_lon = (radius_nm / earth_radius_nm) * math.sin(angle_rad) / math.cos(math.radians(center_lat))
        
            # Calculate the new latitude and longitude
            lat = center_lat + math.degrees(delta_lat)
            lon = center_lon + math.degrees(delta_lon)
        
            # Add the point to the dictionary
            circle_points[angle] = (lat, lon)
    
        return circle_points

    
if __name__ == "__main__":
    # Configure CherryPy server
    sim = StreamReader()
    sim.start_simulator_test(5) 


    
   