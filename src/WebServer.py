import cherrypy
import json


from SensorPipeline import sensorpipeline  # import the running class
from StreamReader import StreamReader   # need for simulator/realtime/file 


class WebServer:
    streamreader = None
    refresh_counter = 0   #
    def __init__(self):
        """ """
        self.streamreader = StreamReader()
        self.streamreader.start_thread()
        return 
        



    @cherrypy.expose
    def index(self):
        """ """  

        """Render the index page."""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>N2K Monitor</title>
        </head>
        <body>
            <h1>N2K Monitor</h1>
            <ul>
                <li>Function 1</li>
                <li><a href="/viewtalkers">View NEMA Talkers</a></li>
                <li><a href="/viewmon">Viewmon</a></li>
                <li><a href="/stream">Stream</a></li>
            </ul>
        </body>
        </html>
        """

    @cherrypy.expose
    def viewtalkers(self):
        """ """
        html_top = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>View NMEA 0183 Talkers </title>
            <body>
        """
        print("* * * * * * * * * *\n",sensorpipeline.nmea_function_counter)
        html_content = "<H3>NMEA Talker ID counts</H3>\n"
        for talker_id in sensorpipeline.nmea_function_counter:
            """ """
            count = sensorpipeline.nmea_function_counter[talker_id]
            if count > 0:
                html_content +=  talker_id + "=" + str(count) +"<BR>\n"
        
        html_bottom = """
        </body>
        </html>
        """
        return html_top + html_content + html_bottom 


    
    
    @cherrypy.expose
    def viewmon(self):
        """Render the viewmon page."""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Viewmon in real time</title>
            <script>
                async function fetchData() {
                    try {
                        // Fetch the data from the /stream endpoint
                        const response = await fetch('/stream');
                        
                        if (!response.ok) {
                            console.error('HTTP error:', response.status);
                            document.getElementById('error').textContent = 'Error fetching data: ' + response.status;
                            return;
                        }

                        const data = await response.json();

                        // Update the HTML elements with the data
                        document.getElementById('bsp').textContent = data.BSP;
                        document.getElementById('twa').textContent = data.TWA;
                        document.getElementById('tws').textContent = data.TWS;
                        document.getElementById('depth').textContent = data.DEPTH;
                    } catch (error) {
                        console.error('Fetch error:', error);
                        document.getElementById('error').textContent = 'Error fetching data: ' + error.message;
                    }
                }

                // Fetch data every 1 seconds
                setInterval(fetchData, 1000);
                window.onload = fetchData; // Fetch data immediately on page load
            </script>
        </head>
        <body>
            <h3>Viewmon</h3>
            <p><strong>Boat Speed (BSP):</strong> <span id="bsp">Loading...</span></p>
            <p><strong>True Wind Angle (TWA):</strong> <span id="twa">Loading...</span></p>
            <p><strong>True Wind Speed (TWS):</strong> <span id="tws">Loading...</span></p>
            <p><strong>Depth:</strong> <span id="depth">Loading...</span></p>
            <p id="error" style="color: red;"></p>
        </body>
        </html>
        """
    


    @cherrypy.expose
    def stream(self):
        """Return the data as a JSON object."""
        try:
            # Sample N2K data
            n2kdata = {
                "BSP": 4,     # Boat Speed
                "TWA": 21,    # True Wind Angle
                "TWS": 33,    # True Wind Speed
                "DEPTH": 10   # Depth
            }

            self.refresh_counter += 1  
            #n2kdata["DEPTH"] = n2kdata["DEPTH"] + self.refresh_counter
            n2kdata["DEPTH"] = sensorpipeline.sensors['depth_m']
            print("sensorpipeline.sensors['depth_m'] ",sensorpipeline.sensors['depth_m'])

            # Convert the dictionary to a JSON object and encode as bytes
            cherrypy.response.headers['Content-Type'] = 'application/json'
            return json.dumps(n2kdata).encode('utf-8')  # Encode to bytes
        except Exception as e:
            # Handle any exceptions
            cherrypy.response.status = 500
            return json.dumps({"error": str(e)}).encode('utf-8')
  


if __name__ == "__main__":
    # Configure CherryPy server
    cherrypy.config.update({
        "server.socket_host": "0.0.0.0",
        "server.socket_port": 8080,
        "engine.autoreload.on": True
    })

    # Mount the application
    cherrypy.quickstart(WebServer())
