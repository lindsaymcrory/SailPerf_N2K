# sailperf_n2k
S A I L P E R F - N2K is an open-source Python library for logging and displaying NMEA2000 data specifically for sail performance analysis.
=======

<!--  ![SailPerf-N2K Logo](assets/logo.png)  -->


<!--  [![Get Started](https://img.shields.io/badge/Get-Started-brightgreen)](https://example.com/get-started) -->

<!-- [![Documentation](https://img.shields.io/badge/Docs-Read-blue)](https://example.com/docs) -->



## S A I L P E R F - N2K* is an open-source Python library for logging and displaying NMEA2000 data for sailboat performance analysis.  

⚠️ **Caution:** S A I L P E R F - N2K is in early beta development, many functions are still being developed and tested.

<img src="assets/functional_block.png" width = "800">


### Features

- Connects to NMEA 2000 Actisense  W2K1 reader or a  PI CAN M Raspberry pie hat(in testing).
- Runs on Raspberry PI ( 3 or higher ) or windows / Mac/ Linux device. 
- Can operate headless (no screen/ keyboard needed)



### Functions:
- Identify N2K devices   
- Broadcast N2K data to any browser  
- Logging N2K data specific to analyzing boat performance
- Aggregate data from non N2K devices (i.e. Velociteck / Varakos) 
- Export data to other analsysis tools (CSV)   
- Creating synthetic simulation data  
- Post Race Anaysis
- - Same speed on different tacks.
-  - Boat trim consistency (fore-aft, heel).
- - Start line acceleration.
- - Sail to theoretical polars.
- - Acceleration times for start time (from sails flapping to hull speed, wind, crew).
- - Time at hull speed (minutes).
- - Comparative analysis and benchmarking.


<img src="assets/data_flows.png" width = "800">

1.  AsctiSence.
2.  Signal K.
3.  NEMA File Reader
4.  Course Simulator
5.  NMEA Handler
6.  Stream Reader
7.  WebServer. 
8.  SensorPipeline
9.  Raw Logs
10. SQLite. 


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/lindsaymcrory/SailPerf-N2K.git  


##### **Usage**
Explain how users can run the project and interact with it.

```markdown
## Usage
1. Connect your NMEA2000 network to the system.
2. Access the web dashboard via your browser at `http://<device-ip>:<port>`.
3. View real-time data, log files, or use the API for advanced analysis.

### Limitations 
-Not a e

### Futures.
-Support NEMA Hat on pi 
-Ananysis support 
-data merge with none NMEA - oe. prostart.

## Screenshots
![Dashboard](https://example.com/screenshot.png)

## License
Licensed under the [Apache 2.0 License](LICENSE).
