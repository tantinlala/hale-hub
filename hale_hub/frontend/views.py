import pytz
from flask import current_app, Blueprint, render_template
from ..home_stats import get_home_stat_time_series
from ..constants import NUMBER_HOURS_ROOM_STAT_PLOT


frontend_blueprint = Blueprint('frontend_blueprint', __name__, template_folder='templates')


@frontend_blueprint.route('/hello_world')
def hello_world():
    return 'hello world'


@frontend_blueprint.route('/plot/<location>/<stat_name>')
def plot_home_stat(location, stat_name):
    home_stat_time_series = get_home_stat_time_series(location, stat_name, NUMBER_HOURS_ROOM_STAT_PLOT)

    if len(home_stat_time_series):
        units_string = home_stat_time_series[0].units
    else:
        units_string = ''

    time_points = list()
    stat_points = list()
    local_tz = pytz.timezone(current_app.config["INSTANCE_TIMEZONE"])
    for home_stat_time_slice in home_stat_time_series:
        local_datetime = home_stat_time_slice.date.replace(tzinfo=pytz.utc).astimezone(tz=local_tz).strftime('%H:%M')
        time_points.append(local_datetime)
        stat_points.append(home_stat_time_slice.value)

    return render_template('line_chart.html', title='{} {} {}'.format(location, stat_name, units_string),
                           max=24*4, labels=time_points, values=stat_points)
