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

# Creating a Python dictionary from the provided data

talker_ids = {
    "AB": "Independent AIS Base Station",
    "AD": "Dependent AIS Base Station",
    "AG": "Autopilot - General",
    "AI": "Mobile AIS Station",
    "AN": "AIS Aid to Navigation",
    "AP": "Autopilot - Magnetic",
    "AR": "AIS Receiving Station",
    "AT": "AIS Transmitting Station",
    "AX": "AIS Simplex Repeater",
    "BD": "BeiDou (China)",
    "BI": "Bilge System",
    "BN": "Bridge navigational watch alarm system",
    "CA": "Central Alarm",
    "CC": "Computer - Programmed Calculator (obsolete)",
    "CD": "Communications - Digital Selective Calling (DSC)",
    "CM": "Computer - Memory Data (obsolete)",
    "CR": "Data Receiver",
    "CS": "Communications - Satellite",
    "CT": "Communications - Radio-Telephone (MF/HF)",
    "CV": "Communications - Radio-Telephone (VHF)",
    "CX": "Communications - Scanning Receiver",
    "DE": "DECCA Navigation (obsolete)",
    "DF": "Direction Finder",
    "DM": "Velocity Sensor, Speed Log, Water, Magnetic",
    "DP": "Dynamic Position",
    "DU": "Duplex repeater station",
    "EC": "Electronic Chart Display & Information System (ECDIS)",
    "EP": "Emergency Position Indicating Beacon (EPIRB)",
    "ER": "Engine Room Monitoring Systems",
    "FD": "Fire Door",
    "FS": "Fire Sprinkler",
    "GA": "Galileo Positioning System",
    "GB": "BeiDou (China)",
    "GI": "NavIC, IRNSS (India)",
    "GL": "GLONASS, according to IEIC 61162-1",
    "GN": "Combination of multiple satellite systems (NMEA 1083)",
    "GP": "Global Positioning System receiver",
    "GQ": "QZSS regional GPS augmentation system (Japan)",
    "HC": "Heading - Magnetic Compass",
    "HD": "Hull Door",
    "HE": "Heading - North Seeking Gyro",
    "HF": "Heading - Fluxgate",
    "HN": "Heading - Non North Seeking Gyro",
    "HS": "Hull Stress",
    "II": "Integrated Instrumentation",
    "IN": "Integrated Navigation",
    "JA": "Alarm and Monitoring",
    "JB": "Water Monitoring",
    "JC": "Power Management",
    "JD": "Propulsion Control",
    "JE": "Engine Control",
    "JF": "Propulsion Boiler",
    "JG": "Aux Boiler",
    "JH": "Engine Governor",
    "LA": "Loran A (obsolete)",
    "LC": "Loran C (obsolete)",
    "MP": "Microwave Positioning System (obsolete)",
    "MX": "Multiplexer",
    "NL": "Navigation light controller",
    "OM": "OMEGA Navigation System (obsolete)",
    "OS": "Distress Alarm System (obsolete)",
    "P": "Vendor specific",
    "QZ": "QZSS regional GPS augmentation system (Japan)",
    "RA": "RADAR and/or ARPA",
    "RB": "Record Book",
    "RC": "Propulsion Machinery",
    "RI": "Rudder Angle Indicator",
    "SA": "Physical Shore AUS Station",
    "SD": "Depth Sounder",
    "SG": "Steering Gear",
    "SN": "Electronic Positioning System, other/general",
    "SS": "Scanning Sounder",
    "ST": "Skytraq debug output",
    "TC": "Track Control",
    "TI": "Turn Rate Indicator",
    "TR": "TRANSIT Navigation System",
    "U#": "'#' is a digit 0 …​ 9; User Configured",
    "UP": "Microprocessor controller",
    "VA": "VHF Data Exchange System (VDES), ASM",
    "VD": "Velocity Sensor, Doppler, other/general",
    "VM": "Velocity Sensor, Speed Log, Water, Magnetic",
    "VR": "Voyage Data recorder",
    "VS": "VHF Data Exchange System (VDES), Satellite",
    "VT": "VHF Data Exchange System (VDES), Terrestrial",
    "VW": "Velocity Sensor, Speed Log, Water, Mechanical",
    "WD": "Watertight Door",
    "WI": "Weather Instruments",
    "WL": "Water Level",
    "YC": "Transducer - Temperature (obsolete)",
    "YD": "Transducer - Displacement, Angular or Linear (obsolete)",
    "YF": "Transducer - Frequency (obsolete)",
    "YL": "Transducer - Level (obsolete)",
    "YP": "Transducer - Pressure (obsolete)",
    "YR": "Transducer - Flow Rate (obsolete)",
    "YT": "Transducer - Tachometer (obsolete)",
    "YV": "Transducer - Volume (obsolete)",
    "YX": "Transducer",
    "ZA": "Timekeeper - Atomic Clock",
    "ZC": "Timekeeper - Chronometer",
    "ZQ": "Timekeeper - Quartz",
    "ZV": "Timekeeper - Radio Update, WWV or WWVH"
}

