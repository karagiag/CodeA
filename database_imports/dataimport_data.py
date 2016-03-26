# Python script for filling database from csv file

import datetime, sys, os
import numpy as np
from sqlalchemy import create_engine

# Full path to django project directory
djangoproject_home="/home/oliver/Repositories/CodeA/codea/"
# Full path to python FinApp directory

sys.path.append(djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codea.settings")

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
from django.utils import timezone
stockplot = get_wsgi_application()
from stockplot.models import Stock, StockData
from stockplot.FinApp.stockQuandl import StockQuandl
today = datetime.datetime.now().strftime("%Y-%m-%d")


'''# connect to database:
from django.conf import settings

user = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']
database_name = settings.DATABASES['default']['NAME']

database_url = 'postgresql://{user}:{password}@localhost/{database_name}'.format(
    user=user,
    password=password,
    database_name=database_name,
)

engine = create_engine(database_url, echo=False)
result = engine.execute("select * from stockplot_stock where symbol=%s", ('KCO.F') )
row.to_sql('stockplot_stock', engine,if_exists='append',index=True)
'''

# Get available stocks from database:
stocks = Stock.objects.all()
#stock = Stock.objects.get(symbol='KCO.F')
#stock = stocks[0];
for stock in Stock.objects.all():
    print(stock.name)
    stockobj = StockQuandl(stock.QuandlSymbol)
    history = stockobj.getStockHistory('1900-01-01', today)
    for index, row in history.iterrows():
        index = timezone.make_aware(index, timezone.get_current_timezone())
        data = stock.stockdata_set.get_or_create(date = index,
            open_price = float(row['Open']), high = float(row['High']),
            low = float(row['Low']), close = float(row['Close']),
            change = float(row['Change']), traded_volume = float(row['Traded Volume']),
            turnover = float(row['Turnover']),
            last_price_of_the_day = float(row['Last Price of the Day']),
            daily_traded_units = float(row['Daily Traded Units']),
            daily_turnover = float(row['Daily Turnover']))
