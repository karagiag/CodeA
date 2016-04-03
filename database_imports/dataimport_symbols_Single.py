# Python script for filling database from csv file

import sys, os, csv

# Full path and name to csv file
csv_filepathname="FSE-datasets-codes.csv"
# Full path to your django project directory
your_djangoproject_home="/home/oliver/Repositories/CodeA/codea/"

sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codea.settings")

# This is so my local_settings.py gets loaded.
#os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
stockplot = get_wsgi_application()

from stockplot.models import Stock

stock = Stock()
stock.name = 'Fandom'
stock.symbol = 'FAN.DOM'
stock.stockExchange = 'Frankfurt'
stock.source = 'Fandom'
stock.sourceName = 'Fandom'
stock.sourceSymbol = 'FAN.DOM'
print("Saving " + stock.name)
stock.save()

print("Done.")
