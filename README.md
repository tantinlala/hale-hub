# Hale Hub

A minimal home lighting automation service.

## Supported Functionality
- Turn radio-controlled outlets on and off.
- Run light automations.
  - Turn a light on at sunset.
  - Turn a light off at a configured time.

All MQTT, SQLite, Flask, temperature, and humidity features have been removed.

## Configuration
Create or edit `instance/instance_config.py` with the values below:

```python
SERIAL_INTERFACE = 'CP2102'
OUTLET_0_NAME = 'Corner Light'
OUTLET_1_NAME = 'Side Light'
OUTLET_2_NAME = 'Bedroom Light'
AUTO_LIGHT_OUTLET_ID = 0
LIGHT_OFF_HOUR = 23
LIGHT_OFF_MINUTE = 0
LATITUDE = 42
LONGITUDE = -71
SUNSET_OFFSET_MINUTES = 50
```

## Run
1. Create and activate a virtual environment.
2. Install the project:

```bash
pip install -e .
```

3. Start automation polling loop:

```bash
hale_hub_run
```

`hale_hub_setup` is retained for compatibility and is now a no-op.
