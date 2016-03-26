# Python script for filling database from csv file

import sys, os, csv

# Full path and name to csv file
csv_filepathname="/home/oliver/Repositories/CodeA/docs/FSE-datasets-codes.csv"
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

dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
for row in dataReader:
    #if row[0] != 'ZIPCODE': # Ignore the header row, import everything else
    stock = Stock()
    stock.name = row[0]
    stock.symbol = row[1]
    stock.stockExchange = row[2]
    stock.QuandlName = row[3]
    stock.QuandlSymbol = row[4]
    print("Saving " + stock.name)
    stock.save()

print("Done.")
