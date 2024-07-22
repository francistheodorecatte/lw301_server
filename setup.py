#!/usr/bin/python3
from setuptools import setup, find_packages

setup(
    name='lw301-server',
    version='0.0.2',
    install_requires=['tornado>=5.1, <6.0', 'paho-mqtt'],
    tests_require=['nose', 'pycodestyle'],
    test_suite='nose.collector',
    scripts=['lw301_server'],
    packages=find_packages(exclude=['lw301_server_tests']),
    description='Emulate servers for Oregon Scientific LW301',
    author='Francis T. Catte',
    author_email='perturbed.old.cat@gmail.com',
    license='Apache 2.0',
    url='https://github.com/francistheodorecatte/lw301_server',
)
