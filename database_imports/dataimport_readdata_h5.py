# Python script for filling database from csv file

import datetime, sys, os, random, pytz, h5py, time
import numpy as np
from dateutil.parser import parse

#dates_datetime = [pytz.utc.localize(base - datetime.timedelta(seconds = x)) for x in range(0, nbEntries)]
#dates = [np.string_(date.isoformat()) for date in dates_datetime]

#open_price = np.array([random.random()*100 for _ in range(0, nbEntries)])


time1 = time.time()

h5f = h5py.File('data.h5','r')
#datestrings = np.ndarray.tolist(h5f['dates'][:])
#dates = [parse(date) for date in datestrings]
dates = np.ndarray.tolist(h5f['dates'][:])
#dates = [datetime.datetime.fromtimestamp(date) for date in datestamp]
data = np.ndarray.tolist(h5f['data'][:])
h5f.close()

'''with h5py.File('data.h5','r') as hf:
    dates = hf.get('dates')
    data = hf.get('data')
data = data[...]'''
print(dates[0])
time2 = time.time()
print(time2-time1)
