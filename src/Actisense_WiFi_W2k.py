
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



import socket

class Actisense_WiFi_W2K:
    """ 
    """

    def test(self):
        """ """
        # Actisense W2K-1 IP and Port
        server_ip = "192.168.4.1"
        server_port = 60001
        max_lines = 100

        try:
            # Create and bind the client socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(10)  # Set a timeout
            #client_socket.bind(("192.168.4.X", 0))  # Use Raspberry Pi's IP on the same subnet

            # Connect to the Actisense W2K-1
            print(f"Connecting to {server_ip}:{server_port}...")
            client_socket.connect((server_ip, server_port))
            print("Connected!")

            # Read data from the server
            lines_read = 0
            while lines_read < max_lines:
                data = client_socket.recv(1024).decode('ascii')
                if not data:
                    print("No more data received.")
                    break
                    print(f"Line {lines_read + 1}: {data.strip()}")
                    lines_read += 1

            print("Completed reading 100 lines of data.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Close the socket
            client_socket.close()
            print("Socket closed.")

        return

        


