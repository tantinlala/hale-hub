# Hale Hub

Lights-only home automation server.

## Summary
This application now supports only:
- Turning radio-controlled outlets (lights) on and off remotely
- Managing light automations (sunset-on and scheduled-off)

The app keeps a Flask REST API for remote control and outlet state reporting.

## Example Picture
![alt text](https://github.com/tantinlala/hale-hub/blob/main/images/outlet_controls.png?raw=true)

## Hardware
- Etekcity Remote Control Outlet - https://www.amazon.com/gp/product/B00DQ2KGNK/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1
- Raspberry Pi 2
- 433Mhz RF Transmitter and receiver - https://www.amazon.com/WWZMDiB-Transmitter-Receiver-Control-Raspberry/dp/B0BDFK55YN/ref=sr_1_1_sspa?crid=Y2G3LES9F6EW&keywords=433+mhz&qid=1680823338&sprefix=433+mhz%2Caps%2C83&sr=8-1-spons&psc=1

## Setup Instructions
1. Pull this repository onto your host.
2. Create an instance_config.py file under instance with your deployment values:

```python
SERIAL_INTERFACE = 'replace_with_transmitter_arduino_usb_name'
OUTLET_0_NAME = 'replace_with_your_outlet_name'
OUTLET_1_NAME = 'replace_with_your_outlet_name'
OUTLET_2_NAME = 'replace_with_your_outlet_name'
AUTO_LIGHT_OUTLET_ID = 0
LIGHT_OFF_HOUR = 22
LIGHT_OFF_MINUTE = 45
LATITUDE = 0.0
LONGITUDE = 0.0
SUNSET_OFFSET_MINUTES = 50
```

3. Create and activate a virtual environment in the repository root.
4. Run pip install -e .
5. Start the app with hale_hub_run.

## REST API
- GET /api/home_stats: current outlet states
- POST /api/outlets/on: turn outlet IDs on
- POST /api/outlets/off: turn outlet IDs off
- POST /api/outlets/toggle: toggle outlet IDs
- GET /api/get_automation_states: view automation enabled/disabled state
- POST /api/toggle_automation: enable/disable automation by key

For outlet control requests, send JSON in the form:

```json
{"outlet_ids": [0, 1]}
```

## Setup Instructions - RC Transmitter Arduino
One Arduino / ESP8266 can be used to control the RC outlets via a 433MHz RF transmitter module.

1. Install the RCSwitch library in your Arduino IDE: https://github.com/sui77/rc-switch
2. Connect the IR transmitter pin to GPIO 5 on your Arduino board.
3. Connect Vcc on the 433MHz transmitter module to Vin from your Arduino board.
4. Connect GND on the 433MHz transmitter module to GND on your Arduino board.
5. Load arduino/Hale_RC/Hale_RC.ino onto your Arduino board.
6. Connect the Arduino to your host via USB.