from setuptools import setup

setup(
    name='HaleHub',
    version='0.1.0',
    packages=['hale_hub', 'hale_hub.rest_api'],
    url='',
    license='',
    description='My home automation application',
    install_requires=[
        'MarkupSafe==2.0.0',
        'Flask<2.1.0; python_version < "3.9"',
        'tzlocal<4.0',
        'Flask-RESTful',
        'Flask-APScheduler',
        'pyserial',
        'suntime',
    ],
    entry_points={
        "console_scripts": [
            "hale_hub_run = hale_hub.entry_points:hale_hub_run",
            "hale_hub_setup = hale_hub.entry_points:hale_hub_setup"
        ]
    },
    extras_require={
        'testing': ['pytest', 'pytest-mock'],
    }
)
