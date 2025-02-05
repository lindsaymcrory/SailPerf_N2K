
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


import math

class CoureseSimulator:

    def __init__(self):
        """   """
        print("Cours Similator")



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
    sim = CoureseSimulator()
    #sim.thread_test() 