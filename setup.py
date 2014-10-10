#!/usr/bin/env python2

from distutils.core import setup

setup(name='wpschema',
      version='1.0',
      description='Schema for the WavePlot server database',
      author='Ben Ockmore',
      author_email='ben.sput@gmail.com',
      url='https://github.com/waveplot/schema',
      packages=['wpschema'],
      requires=['sqlalchemy (>=0.9.7)', 'psycopg2 (>=2.5.4)'],
      provides=['wpschema'],
)
