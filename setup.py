from setuptools import setup, find_packages

setup(
    name='transmitter',
    version='0.0.3',
    packages=find_packages(),
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
    install_requires=["beem", "requests"]
)