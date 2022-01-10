from hale_hub import create_app
from hale_hub.extensions import db


def hale_hub_run():
    app = create_app()
    app.run(host='0.0.0.0')


def hale_hub_setup():
    app = create_app()
    with app.app_context():
        db.init_app(app)
        db.create_all()
