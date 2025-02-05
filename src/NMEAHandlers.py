
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



"""
This Python program defines a class NMEAHandlers for parsing and handling various types of NMEA sentences commonly used in marine navigation and sensor data collection. The program integrates with a SensorPipeline to process, transform, and store extracted data for real-time or post-processing applications. Key functionalities include:
	1.	NMEA Sentence Parsing:
        Handles multiple NMEA sentence types (e.g., $GPGGA, $GPGLL, $HCHDG) to extract relevant information such as GPS coordinates, heading, wind speed, water depth, and meteorological data.
	2.	Data Transformation:
        Converts raw data fields (e.g., DMM coordinates) into more usable formats such as fractional degrees for latitude and longitude.
	3.	Data Integration:
        Sends processed data to a SensorPipeline for logging or further analysis. This pipeline acts as a centralized system for managing sensor readings.
	4.	Call Frequency Tracking:
        Maintains a dictionary in SensorPipeLine to track the number of times each handler function is invoked. Useful for debugging and performance monitoring.
	5.	Error Handling and Defaults:
        Provides robust casting methods (cast_to_float and cast_to_int) to ensure graceful handling of invalid or missing data.
	6.	Supported NMEA Sentences:
        Includes handlers for various NMEA sentences:
	        •	$GPGGA (GPS Fix Data)
	        •	$GPGLL (Geographic Position)
	        •	$HCHDG (Heading and Magnetic Deviation)
	        •	$WIMWV (Wind Speed and Angle)
	        •	$SDDPT (Water Depth)
	        •	$TIROT (Rate of Turn)
	        •   Many others, covering a wide range of marine sensor data.
	7.	Documentation:
        Each handler function includes detailed inline documentation explaining the format, fields, and 
        examples of the respective NMEA sentence, aiding maintainability and future development.

"""

from SensorPipeline import sensorpipeline  # import the running class


class NMEAHandlers:
  
    def __init__(self):
        """ """

        return
        
    def GPGAA(self, nmea_sentence):
        """
        $GPGGA: Global Positioning System Fix Data

        Description:
            Provides detailed GPS fix data, including time, position, and fix quality.

        Format:
            $GPGGA,<time>,<latitude>,<N/S>,<longitude>,<E/W>,<fix_quality>,<num_satellites>,<hdop>,
            <altitude>,<altitude_units>,<geoidal_separation>,<geoidal_separation_units>,<checksum>
        
        Fields:

            <time>: UTC time (hhmmss.sss).
	        <latitude>: Latitude in ddmm.mmmm format.
	        <N/S>: North/South indicator.
	        <longitude>: Longitude in dddmm.mmmm format.
	        <E/W>: East/West indicator.
	        <fix_quality>: GPS fix quality (0: Invalid, 1: GPS fix, 2: DGPS fix).
	        <num_satellites>: Number of satellites in use.
	        <hdop>: Horizontal dilution of precision.
	        <altitude>: Altitude above mean sea level.
	        <altitude_units>: Units of altitude (M = meters).
	        <geoidal_separation>: Geoidal separation (difference between the ellipsoid and geoid).
	        <geoidal_separation_units>: Units of geoidal separation (M = meters).
	        <checksum>: XOR checksum for validation.

        Example:

            $GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47
            
            123519: Time is 12:35:19 UTC.
	        4807.038,N: Latitude is 48°07.038' N.
	        01131.000,E: Longitude is 11°31.000' E.
	        GPS fix quality is 1 (valid).
	        08: 8 satellites are in use.
	        0.9: HDOP is 0.9 (high precision).
	        545.4,M: Altitude is 545.4 meters.
	        46.9,M: Geoidal separation is 46.9 meters.
	        *47: Checksum for validation.

        
        """
        sensorpipeline.add_nmea_function_counter('GPGAA')
        parts = nmea_sentence.split(",")
        stamp = self.cast_to_float(parts[1])
        lat = self.cast_to_float(parts[2])  # will return a lat in format: 4439.1518
        hemi = parts[3]
        lat = self.convert_to_fractional_degrees(lat,hemisphere=hemi)
        
        lon = self.cast_to_float(parts[3])
        lon = self.convert_to_fractional_degrees(lon,hemisphere=parts[4])
        

        sensorpipeline.add_reading('latitude',lat)
        sensorpipeline.add_reading('longitude',lon)
        sensorpipeline.add_reading('gpgaa_time',stamp)


        return
    
    
    def GPGLL(self, nmea_sentence):
        """
        $GPGLL: Geographic Position (Latitude and Longitude)
		Description: 
            Reports the current geographic position.

		Format:
            $GPGLL,<Latitude>,<N/S>,<Longitude>,<E/W>,<UTC Time>,<Status>*<Checksum>

        Fields:
	    	<Latitude>: Latitude in degrees and minutes (ddmm.mmmm).
	    	<N/S>: Hemisphere indicator (N for north, S for south).
		    <Longitude>: Longitude in degrees and minutes (dddmm.mmmm).
		    <E/W>: Hemisphere indicator (E for east, W for west).
		    <UTC Time>: Time in HHMMSS.ss format.
		    <Status>: A for valid data, V for invalid data.
		
        Example:
            $GPGLL,4439.1514,N,06328.3343,W,220102.5,A,A*4E
            4439.1514,N: Latitude 44°39.1514’N.
		    06328.3343,W: Longitude 63°28.3343’W.
		    220102.5: UTC time (22:01:02.5).
		    A: Data is valid.
        """
        sensorpipeline.add_nmea_function_counter('GPGLL')
        parts = nmea_sentence.split(",")
        lat = self.cast_to_float(parts[1])  # will return a lat in format: 4439.1518
        hemi = parts[2]
        lat = self.convert_to_fractional_degrees(lat,hemisphere=hemi)
        
        lon = self.cast_to_float(parts[3])
        lon = self.convert_to_fractional_degrees(lon,hemisphere=parts[4])
        sensorpipeline.insert_gps_log(lat,lon)
        stamp = self.cast_to_float(parts[5])

        sensorpipeline.add_reading('latitude',lat)
        sensorpipeline.add_reading('longitude',lon)
        sensorpipeline.add_reading('gpgll_time',stamp)
        return()
    
    def GPGNS(self,nmea_sentence):
        """
        $GPGNS: GNSS Fix Data

        Description:
            Provides GNSS fix data, including mode and satellite information.
        
        Format:
            $GPGNS,<time>,<latitude>,<N/S>,<longitude>,<E/W>,<mode>,<num_satellites>,
            <hdop>,<altitude>,<geoidal_separation>,<checksum>

        Fields:
	        <time>: UTC time (hhmmss.sss).
	        <latitude>: Latitude in ddmm.mmmm format.
	        <N/S>: North/South indicator.
	        <longitude>: Longitude in dddmm.mmmm format.
	        <E/W>: East/West indicator.
	        <mode>: Fix mode (e.g., A: Autonomous, D: Differential).
	        <num_satellites>: Number of satellites used.
	        <hdop>: Horizontal dilution of precision.
	        <altitude>: Altitude above sea level.
	        <geoidal_separation>: Geoidal separation.
	        <checksum>: XOR checksum for validation.

        Example:

            $GPGNS,123519,4807.038,N,01131.000,E,A,8,0.95,545.4,46.9*52

            123519: Time is 12:35:19 UTC.
	        4807.038,N: Latitude is 48°07.038' N.
	        01131.000,E: Longitude is 11°31.000' E.
	        A: Fix mode is Autonomous.
	        8: 8 satellites are used.
	        0.95: HDOP is 0.95.
	        545.4: Altitude is 545.4 meters.
	        46.9: Geoidal separation is 46.9 meters.
	        *52: Checksum for validation.


        
        """
        sensorpipeline.add_nmea_function_counter('GPGNS')
        return
    
 
    def GPMRC(self,nmea_sentence):
        """
        $GPMRC Recommended Minimum Specific GNSS Data
        
        Description:
            Provides essential GPS data, including position, velocity, and time.

        Format:
            $GPRMC,<time>,<status>,<latitude>,<N/S>,<longitude>,<E/W>,<speed_knots>,<track_angle>,
            <date>,<magnetic_variation>,<E/W>,<checksum>

        Fields:
            <time>: UTC time in hhmmss.sss format.
	        <status>: Data validity (A = valid, V = invalid).
	        <latitude>: Latitude in ddmm.mmmm format.
	        <N/S>: North or South indicator.
	        <longitude>: Longitude in dddmm.mmmm format.
	        <E/W>: East or West indicator.
	        <speed_knots>: Speed over ground in knots.
	        <track_angle>: Track angle in degrees.
	        <date>: Date in ddmmyy format.
	        <magnetic_variation>: Magnetic variation (optional).
	        <E/W>: Direction of magnetic variation (optional).
	        <checksum>: Checksum for validation.

        Example:
            $GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A
            123519: Time is 12:35:19 UTC.
	        A: Data is valid.
	        4807.038,N: Latitude is 48°07.038' N.
	        01131.000,E: Longitude is 11°31.000' E.
	        022.4: Speed over ground is 22.4 knots.
	        084.4: Track angle is 84.4°.
	        230394: Date is 23 March 1994.
	        003.1,W: Magnetic variation is 3.1° W.
	        *6A: Checksum for validation.
        """
        sensorpipeline.add_nmea_function_counter('GPRMC')
        return
    

    
    def HCHDG(self,nmea_sentence):
        """ 
        $HCHDG: Heading, Deviation, and Variation
        
        Description:
            This sentence provides the magnetic heading, 
            magnetic deviation, and magnetic variation. It is primarily used for compass data.

        Format:
            $HCHDG,<heading>,<deviation>,<deviation_dir>,<variation>,<variation_dir>*<checksum>
        
        Fields:
            <heading>: Magnetic heading in degrees (0 to 359.9).
	        <deviation>: Magnetic deviation in degrees (optional).
	        <deviation_dir>: Deviation direction: E: East , W: West
	        <variation>: Magnetic variation in degrees (optional).
	        <variation_dir>: Variation direction: E: East, W: West
	        <checksum>: Checksum for error detection, preceded by *.

        Example:
            $HCHDG,123.4,2.0,E,3.1,W*3F
            123.4: Magnetic heading is 123.4°.
	        2.0: Magnetic deviation is 2.0° east.
	        3.1: Magnetic variation is 3.1° west.
	        *3F: Checksum for validation.
        
        """
    
        sensorpipeline.add_nmea_function_counter('HGCHDG')
        
        parts = nmea_sentence.split(",")
       
        sensorpipeline.add_reading('heading_mag',self.cast_to_float(parts[1]))
        sensorpipeline.add_reading('deviation_deg',self.cast_to_float(parts[2]))
        sensorpipeline.add_reading('deviation_ref',self.cast_to_float(parts[3]))
        sensorpipeline.add_reading('variation_deg',self.cast_to_float(parts[4]))
        sensorpipeline.add_reading('variation_ref',str(parts[5]))
        return
       
    def HCHDM(self, nmea_sentence):
        """
        $HCHDM: Heading, Magnetic
		Description: Reports the vessel’s magnetic heading.
		
        Format:
            $HCHDM,<Heading>,M*<Checksum>
        Fields:
		    <Heading>: Vessel’s heading in degrees (magnetic north).
		    M: Indicates magnetic heading.	
        Example:
            $HCHDM,43,M*00
            43: Magnetic heading in degrees.

        """
        sensorpipeline.add_nmea_function_counter('HCHDM')
        parts = nmea_sentence.split(",")
        sensorpipeline.add_reading('heading_mag',self.cast_to_int(parts[1]))
        return()
    
    def IIMDA(self,nmea_sentence):
        """ 
        $IIMDA meteorological data 
        
        Description:
            Provides a composite of meteorological data such as barometric 
            pressure, air temperature, and relative humidity.

        Format:
            $IIMDA,<baro_pressure_mb>,I,<baro_pressure_inHg>,B,<air_temp>,C,<water_temp>,C,<rel_humidity>,,<abs_humidity>,,<dew_point>,C*<checksum>

        Fields:
            <baro_pressure_mb>: Barometric pressure in millibars.
	        I: Unit for barometric pressure (millibars).
	        <baro_pressure_inHg>: Barometric pressure in inches of mercury.
	        B: Unit for barometric pressure (inHg).
	        <air_temp>: Air temperature in degrees Celsius.
	        C: Unit for temperature (Celsius).
	        <water_temp>: Water temperature in degrees Celsius.
	        C: Unit for temperature (Celsius).
	        <rel_humidity>: Relative humidity (percentage).
	        (Empty Field): Placeholder for absolute humidity.
	        <abs_humidity>: Absolute humidity (optional, rarely used).
	        (Empty Field): Placeholder for additional data.
	        <dew_point>: Dew point temperature in degrees Celsius.
	        C: Unit for temperature (Celsius).
	        <checksum>: Checksum for error detection, preceded by *.

        Example:
            $IIMDA,1013.2,I,29.92,B,25.0,C,20.0,C,50.0,,10.0,,12.0,C*76
            1013.2: Barometric pressure is 1013.2 millibars.
	        29.92: Barometric pressure is 29.92 inches of mercury.
	        25.0: Air temperature is 25.0°C.
	        20.0: Water temperature is 20.0°C.
	        50.0: Relative humidity is 50%.
	        12.0: Dew point is 12.0°C.
	        *76: Checksum for validation.
        
        """
    
        sensorpipeline.add_nmea_function_counter('IIDMA')
        parts = nmea_sentence.split(",")
       
        sensorpipeline.add_reading('baro_pres_mb',self.cast_to_int(parts[1]))
        sensorpipeline.add_reading('baro_pres_in',self.cast_to_int(parts[3]))
        sensorpipeline.add_reading('temp_c',self.cast_to_int(parts[5]))
        
        return
    

    def IIMDA(self,nmea_sentance):
        """
        $IIMDA - Meteorological Data (Barometric Pressure, Temperature, Humidity, etc.)
        Description:
            The $IIMDA sentence provides meteorological data such as barometric pressure, 
            air temperature, water temperature, and relative humidity. It is commonly output by 
            weather sensors on marine vessels.
        
        Format:
            $IIMDA,<Pressure_Inches>,I,<Pressure_Bars>,B,<Air_Temp_C>,C,<Water_Temp_C>,C,<Rel_Humidity>,,<Abs_Humidity>,,<Dew_Point_C>,C*hh
        
        Fields:
            Talker ID	II	Integrated Instrumentation (NMEA 0183)
            Sentence Type	MDA	Meteorological Data
            Pressure (InHg)	29.92	Barometric pressure in inches of mercury
            Units (InHg)	I	Unit identifier (I = inches of mercury)
            Pressure (Bars)	1.013	Barometric pressure in bars
            Units (Bars)	B	Unit identifier (B = bars)
            Air Temp (°C)	25.4	Air temperature in degrees Celsius
            Units (°C)	C	Unit identifier (C = Celsius)
            Water Temp (°C)	20.5	Water temperature in degrees Celsius
            Units (°C)	C	Unit identifier (C = Celsius)
            Relative Humidity (%)	65.0	Relative humidity as a percentage
            (Empty Field)	(empty)	Field left blank (Reserved for future use)
            Absolute Humidity (g/m³)	14.5	Absolute humidity in grams per cubic meter
            (Empty Field)	(empty)	Field left blank (Reserved for future use)
            Dew Point (°C)	18.3	Dew point temperature in degrees Celsius
            Units (°C)	C	Unit identifier (C = Celsius)
            Checksum	*hh	NMEA 0183 checksum (hexadecimal)
        
        """
        # Do not need this now.
    
        return
    

    def IIVHW(self,nmea_sentence):
        """
        $IIVHW: Water Speed and Heading 
        Description:
            Reports water speed and heading information.
        Format:
            $IIVHW,<True Heading>,T,<Magnetic Heading>,M,<Speed in Knots>,N,<Speed in km/h>,K*<Checksum>

        Fields:
        	<True Heading>: Vessel’s heading in degrees (true north).
         	T: Indicates true heading.
         	<Magnetic Heading>: Vessel’s heading in degrees (magnetic north).
        	M: Indicates magnetic heading.
        	<Speed in Knots>: Speed through the water in knots.
        	N: Indicates speed in knots.
        	<Speed in km/h>: Speed through the water in kilometers per hour.
        	K: Indicates speed in km/h.
        
        Example:
            $IIVHW,,T,43,M,0,N,0,K*52
            True Heading: Not provided.
		    Magnetic Heading: 43°.
		    Speed in Knots: 0.
		    Speed in km/h: 0.

        """
        sensorpipeline.add_nmea_function_counter('IIVHW')
        parts = nmea_sentence.split(",")
        sensorpipeline.add_reading('heading_true',self.cast_to_int(parts[1]))
        sensorpipeline.add_reading('heading_mag',self.cast_to_int(parts[3]))
        sensorpipeline.add_reading('boat_speed_nm',self.cast_to_float(parts[5]))
        sensorpipeline.insert_boat_speed_log(self.cast_to_float(parts[5]))
        return
    
 
    
    def SDDPT(self,nmea_sentence):
        """
         $SDDPT: Depth Below Transducer
		Description: 
            Reports the water depth measured from the transducer.
		
        Format:
            $SDDPT,<Depth>,<Offset>,<Maximum Depth>*<Checksum>

        Fields:
	    	<Depth>: Depth below the transducer in meters.
		    <Offset>: Distance from the transducer to the waterline (positive) or keel (negative).
		    <Maximum Depth>: Maximum range depth in meters (optional).
		Example:
            $SDDPT,,0,210*78
            Depth: Not provided.
		    Offset: 0 (no offset from transducer).
		    Maximum Depth: 210.

        """
    
        sensorpipeline.add_nmea_function_counter('SDDPT')
        
        parts = nmea_sentence.split(',')
        depth = parts[1]
        if len(depth) == 0:
            depth = 0
        sensorpipeline.add_reading('depth_m',self.cast_to_float(depth))
        return()
    
    
    def TIROT(self,nmea_sentence):
        """
        $TIROT: Rate of Turn
        Description: 
            Reports the vessel’s rate of turn in degrees per minute.
        Format: 
            $TIROT,<Rate>,<Status>*<Checksum>
            <Rate>: The rate of turn in degrees per minute, where positive values indicate a turn to starboard (right) and negative values indicate a turn to port (left).
	•	    <Status>: A for valid data or V for invalid data.
    	Example:
            $TIROT,-0.76,A*27
            -0.76: Turning to port at 0.76° per minute.
	•	    A: Data is valid.

        """
    
        sensorpipeline.add_nmea_function_counter('TIROT')
        parts = nmea_sentence.split(",")
        sensorpipeline.add_reading('turnrate',self.cast_to_float(parts[1]))
        return 
    
    
    def WIMWV(self,nmea_sentance):
        """
        The $WIMWV  provides wind speed and angle information.
        Description

            The $WIMWV sentence reports the wind angle and wind speed relative to the boat. 
            It includes information on whether the wind is apparent or true and specifies the units 
            for the wind speed measurement.
        Format:
            WIMWV,<wind_angle>,<reference>,<wind_speed>,<units>,<status>*<checksum>
        
        Fields:
            <wind_angle>: Wind angle in degrees (0 to 359). Indicates the direction of the wind relative to the boat.
	        <reference>: Reference for wind angle:  R: Relative (apparent wind) T: True (true wind)
	        <wind_speed>: Wind speed as a floating-point number.
	        <units>: Unit of wind speed: K: Kilometers per hour	M: Meters per second N: Knots
            <status>: Status indicator: A: Data valid V: Data invalid
	        <checksum>: Checksum for error detection, preceded by *.
        
        Example:    
            $WIMWV,045.0,R,12.5,N,A*0C
            045.0: Wind angle is 45.0° relative to the boat.
	    	R: Wind angle is relative (apparent wind).
	    	12.5: Wind speed is 12.5 knots.
	    	N: Wind speed is measured in knots.
	    	A: Data is valid.
	    	*0C: Checksum for the sentence.
        """
        sensorpipeline.add_nmea_function_counter('WIMWV')
        parts = nmea_sentance.split(",")
        sensorpipeline.add_reading('wind_angle_rel',self.cast_to_float(parts[1]))
        sensorpipeline.add_reading('wind_ref',str(parts[2]))  # L-Port, R = Starboard
        sensorpipeline.add_reading('wind_speed_nm',self.cast_to_float(parts[3]))    
        sensorpipeline.add_reading('wind_speed_units',str(parts[4]))

        sensorpipeline.insert_wind_log(self.cast_to_float(parts[3]),self.cast_to_float(parts[1]))
        return
    


    def WIVWR(self,nmea_sentence):
        """
        $WIVWR: Wind Speed and Angle (Relative)
        Description: 
            Reports apparent wind speed and direction relative to the vessel.
		Format:
            WIVWR,<Wind Angle>,<Reference>,<Wind Speed in Knots>,N,<Wind Speed in m/s>,M,<Wind Speed in km/h>,K*<Checksum>
        
        Fields:
		    <Wind Angle>: Apparent wind angle in degrees relative to the vessel’s bow.
		    <Reference>: R for relative wind angle or T for true wind angle.
		    <Wind Speed in Knots>: Apparent wind speed in knots.
		    N: Indicates speed in knots.
		    <Wind Speed in m/s>: Apparent wind speed in meters per second.
		    M: Indicates speed in meters per second.
		    <Wind Speed in km/h>: Apparent wind speed in kilometers per hour.
		    K: Indicates speed in kilometers per hour. 


        Example:
            $WIVWR,41.4,R,5,N,2.6,M,9.3,K*73
            41.4: Wind angle relative to the vessel’s bow.
	    	R: Relative wind angle.
	    	5: Wind speed in knots.
	    	2.6: Wind speed in meters per second.
	    	9.3: Wind speed in kilometers per hour.

        """
    
        sensorpipeline.add_nmea_function_counter('WIVWR')
        parts = nmea_sentence.split(",")
        sensorpipeline.add_reading('wind_angle_relative',self.cast_to_int(parts[1]))
        sensorpipeline.add_reading('wind_speed_kn',self.cast_to_float(parts[3]))
        return()
    
    def convert_to_fractional_degrees(self, dmm, hemisphere):
        """
        Converts latitude/longitude from DMM format to fractional degrees.
    
        :param dmm: Latitude or longitude in DMM format (e.g., 4439.1518 or 06328.3343)
        :param hemisphere: Hemisphere as a single character ('N', 'S', 'E', 'W')
        :return: Fractional degrees as a float
        """
        # Extract degrees and minutes
        degrees = int(dmm // 100)  # Get whole degrees
        minutes = dmm % 100       # Get the minutes portion
    
        # Convert to fractional degrees
        fractional_degrees = degrees + (minutes / 60)
    
        # Adjust sign based on hemisphere
        if hemisphere in ['S', 'W']:
            fractional_degrees *= -1
        return(fractional_degrees)
    
    
    
    def cast_to_float(self,value: str, default: float = 0.0) -> float:
        """
        Safely cast a string to a double (float in Python).
        If the conversion fails, it returns a default value.

        :param value: The string to convert to a double.
        :param default: The default value to return if conversion fails.
        :return: The converted double value or the default.
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
        
    def cast_to_int(self,value: str, default: int = 0.0) -> int:
        """
        Safely cast a string to a int.
        If the conversion fails, it returns a default value.

        :param value: The string to convert to a double.
        :param default: The default value to return if conversion fails.
        :return: The converted double value or the default.
        """
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    