from hale_hub import create_app


def hale_hub_run():
    app = create_app()
    app.run(host='0.0.0.0')


def hale_hub_setup():
    # No setup is required for the lights-only runtime.
    return
