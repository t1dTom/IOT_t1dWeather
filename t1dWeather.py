# t1dWeather
#
# This script makes API calls to the Arduino IOT cloud
# to report weather information.  An Arduino R4 Wifi
# is running and reporting weather information to the 
# Arduino IOT cloud.
#
# Author:       t1dTom
# Created:      8/22/2025
#
# Modifictions:
#
# Author:       XXXXXX
# Date:         mm/dd/yyyy
# Description:  XXXXXX

import requests
import os
from dotenv import load_dotenv

# Load credentials from .env file

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Arduino IoT Cloud API endpoints

lastUpdated = ""
lastUpdatedDateTime =""
lastUpdatedDOW = ""
location = ""
dewPoint = 0.00
heatIndex = 0.00
humidity = 0.00
pressureinHg = 0.00
tempF = 0.00

t1dWeatherThing = ""


TOKEN_URL = "https://api2.arduino.cc/iot/v1/clients/token"
THINGS_URL = "https://api2.arduino.cc/iot/v1/things"
PROPERTIES_URL_TEMPLATE = f"https://api2.arduino.cc/iot/v1/things/{t1dWeatherThing}/properties"

def get_access_token():
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": "https://api2.arduino.cc/iot"
    }
    response = requests.post(TOKEN_URL, json=payload)
    response.raise_for_status()
    return response.json()["access_token"]

def get_things(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(THINGS_URL, headers=headers)
    response.raise_for_status()
    return response.json()

def get_properties(token, thing_id):
    headers = {"Authorization": f"Bearer {token}"}
    url = PROPERTIES_URL_TEMPLATE.format(thing_id=thing_id)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    try:
        token = get_access_token()
        #print(token)
        things = get_things(token)
        #print(things)
        for thing in things:

            if thing['name'] == "t1dWeather":
                t1dWeatherThing = thing['id']

        PROPERTIES_URL_TEMPLATE = f"https://api2.arduino.cc/iot/v1/things/{t1dWeatherThing}/properties"

        properties = get_properties(token, t1dWeatherThing)

        for prop in properties:

            if prop['name'] == "lastUpdated":
                lastUpdatedDateTime = prop['last_value']

            if prop['name'] == "lastUpdatedDOW":
                lastUpdatedDOW = prop['last_value']

            if prop['name'] == "location":
                location = prop['last_value']

            if prop['name'] == "dewPointF":
                dewPoint = prop['last_value']

            if prop['name'] == "heatIndex":
                heatIndex = prop['last_value']

            if prop['name'] == "humidity":
                humidity = prop['last_value']

            if prop['name'] == "pressure_inHg":
                pressureinHg = prop['last_value']

            if prop['name'] == "tempF":
                tempF = prop['last_value']

        lastUpdated = f"{lastUpdatedDOW} {lastUpdatedDateTime}"

        print (location)
        print (lastUpdated)
        print ("Temperature: ",round(tempF,1),"f")
        print ("Humidity: ",round(humidity,1),"%")
        print ("Heat Index: ",round(heatIndex,1),"f")
        print ("Dew Point: ",round(dewPoint,1),"f")
        print ("Pressure: ",round(pressureinHg,2),"inHg")

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}")
    except Exception as e:
        print(f"Error: {e}")