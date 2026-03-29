from hale_hub import create_hub
from hale_hub.task_scheduler import run_scheduler


def hale_hub_run():
    create_hub()
    run_scheduler()


def hale_hub_setup():
    print("No setup needed for the lights-only build.")
