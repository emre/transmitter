from setuptools import setup

setup(
    name='transmitter',
    version='0.2.6',
    packages=[
        'transmitter',
        'transmitter.pricefeed',
        'transmitter.pricefeed.adapters',
    ],
    url='http://github.com/emre/transmitter',
    license='MIT',
    author='emre yilmaz',
    author_email='mail@emreyilmaz.me',
    description='STEEM Witness updates made easy.',
    entry_points={
        'console_scripts': [
            'transmitter = transmitter.main:main',
        ],
    },
    install_requires=["beem==0.23.9", "requests", "numpy"]
)
