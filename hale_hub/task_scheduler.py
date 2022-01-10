from hale_hub.constants import FAST_TICK_PERIOD_SECS, FAST_TICK_MISFIRE_TIME
from hale_hub.extensions import scheduler
from hale_hub.home_stats import commit_newest_home_stats, health_check_room_stats
from hale_hub.automations import run_automations


@scheduler.task('cron', id='slow_tick_task_id', hour='*')
def slow_tick_task():
    print('Slow tick task executed')
    with scheduler.app.app_context():
        commit_newest_home_stats()


@scheduler.task('interval', id='fast_tick_task_id',
                seconds=FAST_TICK_PERIOD_SECS, misfire_grace_time=FAST_TICK_MISFIRE_TIME)
def fast_tick_task():
    print('Fast tick task executed')
    with scheduler.app.app_context():
        health_check_room_stats()
        run_automations()
