# Hale Hub: A home automation server
Hale means home in Hawaiian

## Summary
This repository provides the following functionality via a RESTful API (I've set up my iPhone to make these requests via Apple shortcuts)
- Turn radio-controlled outlet switches on and off 
- Enable and disable automations (see below)
- Request current temperature and humidity readings from multiple rooms

The following automations are also available:
- Turn outlets (e.g. light switches) on at sundown and off at time of your choosing
- Send an IFTTT notification to your phone if the humidity or temperature in any room is outside of your comfort zone

In addition, a frontend is available that plots temperature and humidity over the last 12 hours over time for multiple rooms

## Example Pictures
![alt text](https://github.com/tantinlala/hale-hub/blob/main/images/outlet_controls.png?raw=true)

![alt text](https://github.com/tantinlala/hale-hub/blob/main/images/home_stats.png?raw=true)

![alt text](https://github.com/tantinlala/hale-hub/blob/main/images/climate_plot.png?raw=true)

## Hardware
- Etekcity Remote Control Outlet - https://www.amazon.com/gp/product/B00DQ2KGNK/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1 
- Raspberry Pi 2
- ESP8266 development boards - https://www.amazon.com/Organizer-ESP8266-Internet-Development-Compatible/dp/B081PX9YFV/ref=sr_1_5?crid=1SNMBM1MISBND&keywords=esp8266&qid=1680823253&sprefix=esp8266%2Caps%2C86&sr=8-5&th=1
- 433Mhz RF Transmitter and receiver - https://www.amazon.com/WWZMDiB-Transmitter-Receiver-Control-Raspberry/dp/B0BDFK55YN/ref=sr_1_1_sspa?crid=Y2G3LES9F6EW&keywords=433+mhz&qid=1680823338&sprefix=433+mhz%2Caps%2C83&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExOExSWFJGMDRHUU1VJmVuY3J5cHRlZElkPUExMDIxMDcwVEk1SVRBNDhYQVgzJmVuY3J5cHRlZEFkSWQ9QTA4ODY1MTMzNVo4R1hOSFo0VEZKJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==
- Temperature and humidity sensor modules - https://www.amazon.com/gp/product/B0795F19W6/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1

## Setup instructions - Raspberry Pi
1. Make sure that your Raspberry Pi has mosquitto installed and is configured to be an MQTT broker https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/
2. Pull this repository onto your Raspberry Pi
3. Create an instance_config.py file under a folder named 'instance' (located in the root directory of the repository) with the following user-configurable parameters:

```MQTT_BROKER_URL = 'replace_with_broker'  # use the free broker from HIVEMQ
MQTT_USERNAME = ''  # set the username here if you need authentication for the broker
MQTT_PASSWORD = ''  # set the password here if the broker demands authentication
SERIAL_INTERFACE = 'replace_with_connected_esp8266s_name'
IFTTT_SECRET_KEY = 'replace_with_your_ifttt_key'
IFTTT_EVENT_NAME = 'replace_with_your_ifttt_configured_event_name'
INSTANCE_TIMEZONE = 'replace_with_your_timezone_string'
OUTLET_0_NAME = 'replace_with_your_outlet_name'
OUTLET_1_NAME = 'replace_with_your_outlet_name'
OUTLET_2_NAME = 'replace_with_your_outlet_name'
AUTO_LIGHT_OUTLET_ID = 0
BASEMENT_HUMIDITY_LOW_TO_HIGH_THRESHOLD = 61.0
BASEMENT_HUMIDITY_HIGH_TO_LOW_THRESHOLD = 59.0
BEDROOM_HUMIDITY_LOW_TO_HIGH_THRESHOLD = 34.0
BEDROOM_HUMIDITY_HIGH_TO_LOW_THRESHOLD = 32.0
LIGHT_OFF_HOUR = 22
LIGHT_OFF_MINUTE = 45
CHECK_BEDROOM_HUMIDITY_HOUR = 20
CHECK_BEDROOM_HUMIDITY_MINUTE = 0
LATITUDE = replace_with_your_latitude
LONGITUDE = replace_with_your_longitude
SUNSET_OFFSET_MINUTES = 50
```

4. Create a venv (virtual environment folder) in the root directory of the repository
5. Activate the virtual environment
6. Run `pip install -e .` in the root directory of the repository with the virtual environment active
7. With the virtual environment still active, run `hale_hub_setup`, which will create a sqlite database under the instance folder
8. Set up a systemd service so that it activates your virtual environment and then subsequently runs `hale_hub_run`
   1. This lets you set up your raspberry pi to run the web server at startup

## Setup instructions - ESP8266
One ESP8266 is used to control the 433MHz RF transmitter and receiver module. This ESP8266 is directly connected to the Raspberry Pi via a usb-to-serial connection.

Other ESP8266's are used to read the temperature and humidity from sensors. These readings are published via MQTT.

(Please check back later for more detailed instructions)
