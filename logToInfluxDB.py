import time
import sys
import datetime
from influxdb import InfluxDBClient
import temperhum

# Configure InfluxDB connection variables
host = "localhost"
port = 8086 # default port
user = "rpi-4" # the user/password created for the pi, with write access
password = "rpi-4" 
dbname = "sensor_data" # the database we created earlier
interval = 1 # Sample period in seconds

# Create the InfluxDB client object
client = InfluxDBClient(host, port, user, password, dbname)

measurement = "temperhum"
# location will be used as a grouping tag later
location = "sunshed"

# Run until you get a ctrl^c
try:
    while True:
        # Read the sensor using the configured driver and gpio
        humidity, temperature = temperhum.measure()
        # iso = time.ctime() // assumes computer time is UTC
        iso = time.asctime(time.gmtime())
        # print("time: " + str(iso) + " temperature: " + str(temperature) + " humidity: " + str(humidity))
        # Print for debugging, uncomment the below line
        # print("[%s] Temp: %s, Humidity: %s" % (iso, temperature, humidity)) 
        # Create the JSON data structure
        data = [
        {
          "measurement": measurement,
              "tags": {
                  "location": location,
              },
              "time": iso,
              "fields": {
                  "temperature" : float(temperature),
                  "humidity": float(humidity)
              }
          }
        ]
        # Send the JSON data to InfluxDB
        client.write_points(data)
        # Wait until it's time to query again...
        time.sleep(interval)
 
except KeyboardInterrupt:
    pass
