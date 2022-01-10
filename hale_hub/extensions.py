from flask_mqtt import Mqtt
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

# Single instance of each extension

db = SQLAlchemy()

# Note: if I want the app context to be automatically available
# upon calling on_topic decorated function, I'll need to pass
# app into this constructor
# https://github.com/stlehmann/Flask-MQTT/issues/86
mqtt = Mqtt()

scheduler = APScheduler()
