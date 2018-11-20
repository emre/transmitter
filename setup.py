from setuptools import setup, find_packages

setup(
    name='transmitter',
    version='0.1.1',
    packages=[
        'transmitter',
        'transmitter.pricefeed',
        'transmitter.pricefeed.adapters',
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
    install_requires=["beem==0.20.12", "requests"]
)