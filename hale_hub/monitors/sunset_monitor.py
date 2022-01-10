from hale_hub.date_helpers import get_now_time, apply_offset_mins
from suntime import Sun


class _SunsetMonitor:
    def __init__(self):
        self.sun = None
        self.offset_before_sunset = 0
        self.offset_after_sunrise = 0

    def set_latitude_and_longitude(self, latitude, longitude):
        self.sun = Sun(latitude, longitude)

    def set_offset_before_sunset(self, minutes):
        self.offset_before_sunset = minutes

    def set_offset_after_sunrise(self, minutes):
        self.offset_after_sunrise = minutes

    def is_sun_set(self):
        if self.sun is not None:
            # Calculate today's sunset and sunrise time
            sunrise_time = self.sun.get_local_sunrise_time()
            sunrise_time = apply_offset_mins(sunrise_time, self.offset_after_sunrise)

            sunset_time = self.sun.get_local_sunset_time()
            sunset_time = apply_offset_mins(sunset_time, -self.offset_before_sunset)

            # Figure out whether the sun is currently set
            now = get_now_time()
            sun_is_set = False
            if now > sunset_time or now < sunrise_time:
                sun_is_set = True
            return sun_is_set
        else:
            print("No latitude and longitude set!")
            return False


_sunset_monitor = _SunsetMonitor()
is_sun_set = _sunset_monitor.is_sun_set
set_latitude_and_longitude = _sunset_monitor.set_latitude_and_longitude
set_offset_before_sunset = _sunset_monitor.set_offset_before_sunset
set_offset_after_sunrise = _sunset_monitor.set_offset_after_sunrise
