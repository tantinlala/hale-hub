# Hale Hub: A home automation server
### Hale means home in Hawaiian!
## Summary
This web application allows you to do the following from electronic devices such as your computer or your iPhone:
- Turn radio-controlled outlet switches on and off 
- Request current temperature and humidity readings from multiple rooms

The following automations can also be turned on or off from your electronic device:
- Automatically have one of your outlets turn on at sundown (e.g. a light switch) 
- Automatically have that same outlet turn off before your bedtime
- Automatically send an IFTTT notification to your phone if the humidity or temperature in any room is outside your comfort zone

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
SERIAL_INTERFACE = 'replace_with_transmitter_arduino_usb_name'
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

## Setup instructions - RC Transmitter Arduino 
One Arduino / ESP8266 can be used to control the RC outlets via a 433MHz RF transmitter module.

1. Install the RCSwitch library in your Arduino IDE: https://github.com/sui77/rc-switch
2. Connect the IR transmitter pin to GPIO 5 on your Arduino board
3. Connect the Vcc pin of the 433MHz transmitter module to Vin from your Arduino board
4. Connect the GND side to GND on your arduino board
5. Load the code in arduino/Hale_RC/Hale_RC.ino onto your arduino board
6. Directly connect the arduino to your Raspberry pi via usb
7. On the Raspberry Pi, run "lsusb"
8. In your instance/instance_config.py file, set SERIAL_INTERFACE equal to the name that shows up for the Arduino device e.g.
```buildoutcfg
pi@neptr:~/Code/hale-hub/instance $ lsusb
Bus 001 Device 004: ID 10c4:ea60 Cygnal Integrated Products, Inc. CP2102/CP2109 UART Bridge Controller [CP210x family]
```

![alt text](https://github.com/tantinlala/hale-hub/blob/main/images/transmitter.jpg?raw=true)

### Testing functionality
1. Connect the arduino to your computer
2. Open the serial monitor (Baud rate: 9600)
3. For testing purposes, you can type the corresponding character on the serial monitor to control the outlet(s):
 
'¨': Turn outlet 0 off

'©': Turn outlet 0 on

'ª': Turn outlet 1 off

'«': Turn outlet 1 on

'¬': Turn outlet 2 off

Press enter to send the command

## Setup instructions - ESP8266
ESP8266's are used to read the temperature and humidity from DHT22 (AM2302) sensors. These readings are published via MQTT. The data is published to a topic on an MQTT broker over WiFi using the PubSubClient library.

### Required Libraries
- PubSubClient - This library provides functions for connecting to an MQTT broker, publishing data to an MQTT topic, and subscribing to MQTT topics.
- Adafruit Unified Sensor - This library provides a common interface for interacting with a variety of sensors, including the DHT22 sensor used in this sketch.
- DHT Sensor Library - This library provides functions for reading temperature and humidity data from the DHT22 sensor.

###Instructions
1. Install the ESP8266 board add-on https://randomnerdtutorials.com/how-to-install-esp8266-board-arduino-ide/ 
2. Install the required libraries in the Arduino IDE.
3. Open the Hale_Climate sketch in the Arduino IDE.
4. Replace the following placeholders with your own values:
- ssid - Replace with the name of your WiFi network.
- password - Replace with the password for your WiFi network.
- mqtt_server - Replace with the IP address of your MQTT broker.
- room_name - Replace with a name for your room.
4. Upload the sketch to your ESP8266 board.
5. Disconnect the ESP8266 board from power and wire up the DHT sensor to your ESP8266 according to your board's specific pinouts
![alt text](https://github.com/tantinlala/hale-hub/blob/main/images/climate.jpeg?raw=true)

### Testing functionality
1. Apply power to the board.
2. Open the Serial Monitor in Arduino IDE to view the output of the sketch. The device should connect to the WiFi network and MQTT broker and begin publishing temperature and humidity data to the specified topic.
3. Verify that the data is being published to the MQTT broker using the command line tool mosquitto_sub: http://www.steves-internet-guide.com/mosquitto_pub-sub-clients/ 
4. Verify that the Hale-Hub app running on the raspberry pi is printing up-to-date temperature and humidity readings periodically
5. If the humidity reading is offset from the truth by a constant amount, you can apply an additive offset by changing the HUMIDITY_CALIBRATION value in the arduino sketch