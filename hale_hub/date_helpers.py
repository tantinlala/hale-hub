from datetime import datetime, timedelta


def get_now_time():
    return datetime.now()


def apply_offset_mins(unmodified_datetime, applied_offset_mins):
    modified_time = unmodified_datetime.replace(tzinfo=None)
    time_delta = timedelta(minutes=applied_offset_mins)
    modified_time = modified_time + time_delta
    return modified_time


class DateSnapper:
    def __init__(self):
        self.date = datetime.utcnow()

    def get_date(self):
        return self.date

    def did_time_elapse_secs(self, date_snapper_prev, time_elapsed_secs):
        if abs(date_snapper_prev.get_date() - self.date) < timedelta(seconds=time_elapsed_secs):
            return False
        else:
            return True

    def get_time_from_hours_ago(self, hours_ago):
        return self.date - timedelta(hours=hours_ago)

    def __repr__(self):
        return self.date.__repr__()
