from hale_hub.extensions import mqtt
from hale_hub.constants import LOCATION_TOPIC_LEVEL, VARIABLE_NAME_TOPIC_LEVEL, UNITS_TOPIC_LEVEL
from hale_hub.home_stats import add_room_stat
from hale_hub.utils import non_numeric_filter


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    """Subscribes to mqtt topics upon connecting"""
    mqtt.subscribe('room_stat/#')  # Subscribe to room stat topic


@mqtt.on_topic('room_stat/#')
def handle_room_stat_mqtt_message(client, userdata, message):
    """Parses mqtt message containing room stat data and sends data to an external module"""
    try:
        # Extract location and variable name
        topic_levels = message.topic.split('/')
        location = topic_levels[LOCATION_TOPIC_LEVEL]
        name = topic_levels[VARIABLE_NAME_TOPIC_LEVEL]
        units = topic_levels[UNITS_TOPIC_LEVEL]

        # Remove all non-numeric characters from payload
        value_numeric_string = non_numeric_filter.sub('', str(message.payload.decode("utf-8")))
        value = float(value_numeric_string)

        # store new room stat data
        add_room_stat(location, name, value, units)
    except IndexError:
        print("room_stat topic formatted incorrectly!")
