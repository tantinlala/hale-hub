from setuptools import setup

setup(
    name='HaleHub',
    version='0.1.0',
    packages=['hale_hub', 'hale_hub.monitors'],
    url='',
    license='',
    description='My home automation application',
    install_requires=[
        'pyserial',
        'pytz',
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
