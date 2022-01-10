from hale_hub.date_helpers import get_now_time
from datetime import datetime


class TimeMonitor:
    def __init__(self, alarm_hour, alarm_minute):
        self.alarm_time = datetime(1, 1, 1, alarm_hour, alarm_minute, 0).strftime("%H:%M")

    def did_alarm_trigger(self):
        now_time = get_now_time().strftime("%H:%M")

        if now_time == self.alarm_time:
            return True
        else:
            return False
