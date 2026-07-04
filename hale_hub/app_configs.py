import os


class BaseConfig(object):
    MQTT_BROKER_PORT = 1883  # default port for non-tls connection
    MQTT_KEEPALIVE = 5  # set the time interval for sending a ping to the broker to 5 seconds
    MQTT_TLS_ENABLED = False  # set TLS to disabled for testing purposes
    MQTT_BROKER_URL = 'localhost'  # broker is local by default
    MQTT_USERNAME = ''  # set the username here if you need authentication for the broker
    MQTT_PASSWORD = ''  # set the password here if the broker demands authentication

    SQLALCHEMY_ECHO = False
    DEBUG = False

    basedir = os.path.abspath(os.path.dirname(__file__))
    baseDB = os.path.join(basedir, 'instance/instance.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + baseDB
