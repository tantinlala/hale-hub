from app_configs import BaseConfig
from hale_hub.automations import add_automation, reset_automations
from hale_hub.monitors.sunset_monitor import is_sun_set, set_latitude_and_longitude, set_offset_before_sunset
from hale_hub.monitors.time_monitor import TimeMonitor
from hale_hub.outlet_interface import set_outlet_name, set_outlet_serial_interface, turn_off_outlet, turn_on_outlet


def _load_instance_config(config_path):
    config = {}
    try:
        with open(config_path, 'r', encoding='utf-8') as file_obj:
            exec(compile(file_obj.read(), config_path, 'exec'), config)
    except FileNotFoundError:
        pass
    return config


def _get_config_value(instance_config, key):
    if key in instance_config:
        return instance_config[key]
    return getattr(BaseConfig, key)


def create_hub(config_path='instance/instance_config.py'):
    instance_config = _load_instance_config(config_path)

    set_outlet_serial_interface(_get_config_value(instance_config, 'SERIAL_INTERFACE'))
    set_outlet_name(_get_config_value(instance_config, 'OUTLET_0_NAME'), 0)
    set_outlet_name(_get_config_value(instance_config, 'OUTLET_1_NAME'), 1)
    set_outlet_name(_get_config_value(instance_config, 'OUTLET_2_NAME'), 2)

    set_latitude_and_longitude(
        _get_config_value(instance_config, 'LATITUDE'),
        _get_config_value(instance_config, 'LONGITUDE'),
    )
    set_offset_before_sunset(_get_config_value(instance_config, 'SUNSET_OFFSET_MINUTES'))

    auto_light_outlet_id = _get_config_value(instance_config, 'AUTO_LIGHT_OUTLET_ID')

    reset_automations()

    def _turn_on_light():
        return turn_on_outlet(auto_light_outlet_id)

    add_automation(is_sun_set, _turn_on_light, "Light on at sunset")

    light_off_monitor = TimeMonitor(
        _get_config_value(instance_config, 'LIGHT_OFF_HOUR'),
        _get_config_value(instance_config, 'LIGHT_OFF_MINUTE'),
    )

    def _turn_off_light():
        return turn_off_outlet(auto_light_outlet_id)

    add_automation(light_off_monitor.did_alarm_trigger, _turn_off_light, "Light off at night time", data=light_off_monitor)

    return instance_config
