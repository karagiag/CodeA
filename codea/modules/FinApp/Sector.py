
from urllib.request import urlopen
from lxml.html import parse


def SectorIndustry(name):
    try:
        tree = parse(urlopen('http://www.google.com/finance?&q='+name))
        return tree.xpath("//a[@id='sector']")[0].text, tree.xpath("//a[@id='sector']")[0].getnext().text
    except:
        print('Sector: Ticker not Found')
        exit()


