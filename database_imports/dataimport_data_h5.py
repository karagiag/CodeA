# Python script for filling database from csv file

import datetime, sys, os, Quandl, random, pytz, h5py
import numpy as np

# Full path to django project directory
djangoproject_home="/home/oliver/Repositories/CodeA/codea/"
# Full path to python FinApp directory

sys.path.append(djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codea.settings")

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
from django.utils import timezone
from django.conf import settings
from django.core.files import File
stockplot = get_wsgi_application()
from stockplot.models import Stock, StockDataFile
from modules.FinApp.stockQuandl import StockQuandl
today = datetime.datetime.now().strftime("%Y-%m-%d")

# get Quandl token from settings
token = getattr(settings, "QUANDL_TOKEN", 'NO')

# Get available stocks from database:
stock = Stock.objects.get(name__iexact = 'Random')
print(stock.name)
base = datetime.datetime.today()
nbEntries = 10000000
dates_datetime = [pytz.utc.localize(base - datetime.timedelta(seconds = x)) for x in range(0, nbEntries)]
#timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
#dates = [np.string_(date.isoformat()) for date in dates_datetime]
dates = [date.timestamp() for date in dates_datetime]
# change pytz utc. local is not utc!

open_price = np.array([random.random()*100 for _ in range(0, nbEntries)])

#### UPDATE #### separate data into months and save into database...

print("begin")
with h5py.File('data.h5', 'w') as hf:
    hf.create_dataset('dates', data=dates)
    hf.create_dataset('data', data=open_price)
print("end")

stockdatafile = StockDataFile()
stockdatafile.stock = stock
stockdatafile.stockid = stock.id
stockdatafile.fromDate = dates[0]
stockdatafile.toDate = dates[len(dates)-1]

djangofile = File(open('data.h5', 'rb'))

##### UPDATE ##### give a good name to each file...
stockdatafile.stockdata.save(stock.name, djangofile)
djangofile.close()

stockdatafile.save()
