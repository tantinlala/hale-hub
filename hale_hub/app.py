import os
from flask import Flask
from hale_hub.extensions import scheduler

# For blueprints
from hale_hub import rest_api

# For making sure that scheduler is set up properly
from hale_hub import task_scheduler

# For configuring coordinates and custom offsets for sunset checking
from hale_hub.monitors.sunset_monitor import set_latitude_and_longitude, set_offset_before_sunset

# For making sure serial interface is set up properly
from hale_hub.outlet_interface import set_outlet_serial_interface, set_outlet_name

# For default automations
from hale_hub.automations import add_automation
from hale_hub.monitors.sunset_monitor import is_sun_set
from hale_hub.monitors.time_monitor import TimeMonitor
from hale_hub.outlet_interface import turn_on_outlet, turn_off_outlet

config = {
    "base": "app_configs.BaseConfig",
}


def create_app():
    """Create a Flask app."""
    app = Flask(__name__, instance_relative_config=True)
    configure_app(app)
    register_extensions(app)
    register_blueprints(app)
    configure_other_modules(app)
    configure_default_automations(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


def configure_app(app):
    """Set up configuration dictionary"""
    config_name = os.getenv('FLASK_CONFIGURATION', 'base')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('instance_config.py', silent=True)


def register_extensions(app):
    """Register flask extensions."""
    scheduler.init_app(app)
    scheduler.start()


def register_blueprints(app):
    """Register blueprints in views."""
    app.register_blueprint(rest_api.rest_api_blueprint, url_prefix='/api')


def configure_other_modules(app):
    set_outlet_serial_interface(app.config['SERIAL_INTERFACE'])

    try:
        set_outlet_name(app.config['OUTLET_0_NAME'], 0)
        set_outlet_name(app.config['OUTLET_1_NAME'], 1)
        set_outlet_name(app.config['OUTLET_2_NAME'], 2)
    except KeyError:
        print("Using default outlet name!")


def configure_default_automations(app):
    # Light on at sunset
    def _turn_on_light(): return turn_on_outlet(app.config['AUTO_LIGHT_OUTLET_ID'])
    set_latitude_and_longitude(app.config['LATITUDE'], app.config['LONGITUDE'])
    set_offset_before_sunset(app.config['SUNSET_OFFSET_MINUTES'])
    add_automation(is_sun_set, _turn_on_light, "Light on at sunset")

    # Light off at night time
    def _turn_off_light(): return turn_off_outlet(app.config['AUTO_LIGHT_OUTLET_ID'])
    time_monitor = TimeMonitor(app.config['LIGHT_OFF_HOUR'], app.config['LIGHT_OFF_MINUTE'])
    add_automation(time_monitor.did_alarm_trigger, _turn_off_light, "Light off at night time", data=time_monitor)
