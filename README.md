t1dWeather.py

This script calls three Arduino IOT Cloud APIs.

1.  Get an access token
2.  Get a list of avaialble "Things"
3.  Get the "Properties" of a selected "Thing"

The assembled sensor data is stored in JSON format file "SensorData.json"

The process starts with an Arduino R4 Wifi attached to a real time clock, 
a temperature,humidity sensor, and TFT 1.28 round display.  See project:
https://github.com/t1dTom/t1dWeather.git

The Arduino R4 Wifi reads the sensor data every 3 seconds and reports the
data to the Arduino IOT Cloud.  The Arduino IOT Cloud servers the data 
through it's built in APIs.
