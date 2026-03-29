from time import sleep

from hale_hub.constants import FAST_TICK_PERIOD_SECS
from hale_hub.automations import run_automations


def run_scheduler(tick_period_secs=FAST_TICK_PERIOD_SECS):
    while True:
        run_automations()
        sleep(tick_period_secs)
