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

from datetime import datetime
import time 

from talker_ids import talker_ids   # get the dict.
from SensorPipeline import sensorpipeline 
from NMEAHandlers import NMEAHandlers


class NMEAFileReader:
    """ 

    """
   
  
    nmea_handler = None   # will be a instance of NMEA Handler 
    test_filename = ""
        
    def __init__(self):
        """ """
        self.nmea_handler = NMEAHandlers()
        self.test_filename =  "/Users/lindsaymcrory/Dev/SailPerf_N2K/data/W2K_Log.txt"
        return
    
    def test(self):
        """ """
        #self.read_log("../data/W2K_Log.txt")
        self.read_log("/Users/lindsaymcrory/Dev/SailPerf_N2K/data/W2K_Log.txt")
        
        #time_str = self.last_update.strftime("%Y%m%d %H:%M:%S.%f")[:-4]  # Trim microseconds to 2 digits
        #print("*****  Session   Status   ****") 
        #print(*(f"{status_rec} {sensorpipeline.session_status[status_rec]}\n" for status_rec in sensorpipeline.session_status))
        
        #print("\n*****   SESSION COUNTERS  ****") 
        #print(*(f"{counter} {sensorpipeline.sensor_counter[counter]}\n" for counter in sensorpipeline.sensor_counter))

        #print("\n*****   SENSOR READINGS  ****") 
        #print(*(f"{sensor} {sensorpipeline.sensors[sensor]}\n" for sensor in sensorpipeline.sensors))
        return
    
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
     

    def read_NMEA_file(self,fname):
        """ 
         
        """
        f = open(fname, "r")
        limit = 1000
        count = 0 

        # Match the sentence ID (nmea_id) with function (NMEAHandler..) that parces it. 
        nmea_handlers = {
            "$GPGLL": self.nmea_handler.GPGLL,
            "$HCHDM": self.nmea_handler.HCHDM,
            "$HCHDG": self.nmea_handler.HCHDG,
            "$HCHDM": self.nmea_handler.HCHDM,
            "$IIVHW": self.nmea_handler.IIVHW,
            "$SDDPT": self.nmea_handler.SDDPT,
            "$TROT": self.nmea_handler.TIROT, 
            "$WIMWV": self.nmea_handler.WIMWV,
            "$WIVWR": self.nmea_handler.WIVWR
            }


        for rec in f:
            if limit < count:
                break
            count += 1
            #print(rec[:-1])
            rec = str(rec)  # Should be a string, but could be a None 
            rec = rec.replace("\n","")
            rec = rec.strip()
            parts = rec.split(",")
            #print(parts[0])
            nmea_id = parts[0]

            if nmea_id.startswith("$"):
                # Send all headers for counting so we can see what devices are missing.
                sensorpipeline.add_nmea_function_counter(nmea_id)
                
            if nmea_id in nmea_handlers:
                # Only process NMEA sentences 
                
                if self.validate_nmea_checksum(rec)== False:
                    sensorpipeline.increment_checksum_errors()

                else:
                    # 
                    #  This possibly strange looking piece of code 
                    #  executes the corresponding NMEA handler for the NMEA ID. This approach 
                    #  saves a water fall of 'if' and 'else' statements.
                    #  Example: a NMEA ID of "$HCHDG" will call the function  self.nmea_handler.HCHDG(rec)
                    #  

                    handler = nmea_handlers.get(nmea_id)
                    if handler:
                        handler(rec)  #pass the entire record to the handler.
            #time.sleep(.5) # simulate the latency from a bus

        f.close()

        return()

if __name__ == "__main__":
    print("Starting NMEAFileReader as __main__ ")
    fr = NMEAFileReader()
    fr.read_NMEA_file(fr.test_filename)
    print(sensorpipeline.nmea_function_counter)
    print(sensorpipeline.sensors)
    