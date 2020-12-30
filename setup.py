from setuptools import setup

from transmitter import __version__

setup(
    name='transmitter',
    version=__version__,
    packages=[
        'transmitter',
        'transmitter.pricefeed',
        'transmitter.pricefeed.adapters',
    ],
    url='http://github.com/emre/transmitter',
    license='MIT',
    author='emre yilmaz',
    author_email='mail@emreyilmaz.me',
    description='HIVE Witness updates made easy.',
    entry_points={
        'console_scripts': [
            'transmitter = transmitter.main:main',
        ],
    },
    install_requires=["beem==0.24.19", "requests", "numpy"]
)
