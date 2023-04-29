from hale_hub.extensions import db
from hale_hub.models import RoomStatModel
from hale_hub.date_helpers import DateSnapper
from hale_hub.constants import MAX_NUM_ROWS_ROOM_STAT_MODEL, STALE_TIME_SECONDS, BASEMENT_HUMIDITY_CALIBRATION
from hale_hub.outlet_interface import get_outlets


class _HomeStat:
    def __init__(self, value, pub_date):
        self.value = value
        self.pub_date = pub_date


class _RoomStat(_HomeStat):
    def __init__(self, value, pub_date, units):
        super().__init__(value, pub_date)
        self.units = units
        self.status = ""

    def __repr__(self):
        return '<Date %r, Value %f, Units %r, Status %r>' % (self.pub_date, self.value, self.units, self.status)


class _HomeStatsCollection:

    def __init__(self):
        self.newest_room_stats = dict()

    def add_room_stat(self, location, name, value, units):
        if location not in self.newest_room_stats.keys():
            self.newest_room_stats[location] = dict()

        self.newest_room_stats[location][name] = _RoomStat(value, DateSnapper(), units)
        print(self.newest_room_stats)

    def get_newest_room_stat(self, location, name):
        return self.newest_room_stats[location][name].value

    def get_formatted_home_stats(self):
        """Returns a dictionary formatted as follows:
        {
            Group 0: [statusString0, statusString1, ...],
            Group 1: [statusString0, statusString1, ...],
            Group 2: [statusString0, statusString1, ...],
            ...
        } """
        formatted_home_stats = dict()

        outlets = get_outlets()
        outlets_key = 'Outlets'
        formatted_home_stats[outlets_key] = list()
        for outlet in outlets:
            if not outlet.state:
                outlet_state_string = "Off"
            else:
                outlet_state_string = "On"
            outlet_string = '{}: {}'.format(outlet.name, outlet_state_string)
            formatted_home_stats[outlets_key].append(outlet_string)

        for location in sorted(self.newest_room_stats.keys()):
            formatted_home_stats[location] = list()
            for variable_name in sorted(self.newest_room_stats[location].keys()):
                variable_data = self.newest_room_stats[location][variable_name]
                formatted_home_stats[location].append("{}: {:.2f}{} {}".format(variable_name,
                                                                               variable_data.value,
                                                                               variable_data.units,
                                                                               variable_data.status))
        print(formatted_home_stats)
        return formatted_home_stats

    def get_home_stat_time_series(self, location, stat_name, num_hours):
        current_date = DateSnapper()
        oldest_date = current_date.get_time_from_hours_ago(num_hours)
        home_stat_time_series = RoomStatModel.query.filter_by(location=location).filter_by(variable_name=stat_name).\
            filter(RoomStatModel.date >= oldest_date).all()
        return home_stat_time_series

    def health_check_room_stats(self):
        """Makes marks status as empty if good, updates with appropriate status if bad"""
        date_data_checked = DateSnapper()

        for location in self.newest_room_stats.keys():
            for variable_name in self.newest_room_stats[location].keys():
                date_data_published = self.newest_room_stats[location][variable_name].pub_date
                if date_data_published.did_time_elapse_secs(date_data_checked, STALE_TIME_SECONDS):
                    stale_string = "(Stale)"
                else:
                    stale_string = ""
                self.newest_room_stats[location][variable_name].status = stale_string

    # TODO: instead of using db.session directly, call functions in RoomStatModel?
    def commit_newest_home_stats(self):
        """Deletes oldest data and stores newest data to database"""
        while db.session.query(RoomStatModel).count() > MAX_NUM_ROWS_ROOM_STAT_MODEL:
            obj = db.session.query(RoomStatModel).order_by(RoomStatModel.id).first()
            db.session.delete(obj)

        date_data_stored = DateSnapper()

        for location in self.newest_room_stats.keys():
            for variable_name in self.newest_room_stats[location].keys():
                variable_data = self.newest_room_stats[location][variable_name]
                new_room_stat_row = RoomStatModel(date=date_data_stored.get_date(),
                                                  location=location,
                                                  variable_name=variable_name,
                                                  units=variable_data.units,
                                                  value=variable_data.value,
                                                  status=variable_data.status)

                print(new_room_stat_row)
                db.session.add(new_room_stat_row)

        db.session.commit()


# Expose these functions
_home_stats = _HomeStatsCollection()
add_room_stat = _home_stats.add_room_stat
get_formatted_home_stats = _home_stats.get_formatted_home_stats
commit_newest_home_stats = _home_stats.commit_newest_home_stats
health_check_room_stats = _home_stats.health_check_room_stats
get_newest_room_stat = _home_stats.get_newest_room_stat
get_home_stat_time_series = _home_stats.get_home_stat_time_series
