from hale_hub.constants import FAST_TICK_PERIOD_SECS, FAST_TICK_MISFIRE_TIME
from hale_hub.extensions import scheduler
from hale_hub.automations import run_automations


@scheduler.task('interval', id='fast_tick_task_id',
                seconds=FAST_TICK_PERIOD_SECS, misfire_grace_time=FAST_TICK_MISFIRE_TIME)
def fast_tick_task():
    print('Fast tick task executed')
    with scheduler.app.app_context():
        run_automations()
