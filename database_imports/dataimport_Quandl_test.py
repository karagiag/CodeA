# Python script for filling database from csv file

import datetime, sys, os, random, pytz, h5py, time, Quandl
import numpy as np

from django.utils import timezone

today = datetime.datetime.now().strftime("%Y-%m-%d")
history = Quandl.get('FSE/AIR_X', trim_start='2015-01-01', trim_end=today)

for index, row in history.iterrows():
    date = index.timestamp()
    print(type(date))
