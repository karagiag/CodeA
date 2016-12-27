# Calculate Capitalization of specific Stock
# Markus Werner
# 03.10.2016
##################################################################################################

def fundamentals(compyNumber, today, price):

    # Header
    #from yahoo_finance import Share
    from pprint import pprint
    import time, Fundamentals_Value, Sector

    #ticker = 'TSLA'
    #today = str("2013-10-03")
    # Import Fundamentals of the corrent date
    Fundamentals = Fundamentals_Value.analyze(compyNumber, today)

    # Market Capitalization
    shares = float(Fundamentals['Shares Outstanding'])  # Shares Outstanding
    #yahoo = Share(ticker)
    #price = float(yahoo.get_historical(today, today)[0]['Close'])   # Price per Share

    capitalization = shares * price # Market Capitalization
    #print ('\nReturn Market Capitalization for Reporting Date: $' + str(capitalization/1000000000) + 'Mrd')

    # Share Price KPI
    #KCF = price / float(Fundamentals['Free Cash Flow Per Share'])   # Kurs-Cash-Flow-Verhältnis (KCV oder KCF)
    #print('\nKurs-Cash-Flow-Verhältnis: ' + str(KCF))

    #KRF = price / float(Fundamentals['Total Revenue'])  # Kurs-Umsatz-Verhältnis (KUV oder KRF)
    #print('\nKurs-Umsatz-Verhältnis: ' + str(KRF))

    #PB = price / float(Fundamentals['Total Assets Per Share'])  # Kurs-Buchwert-Verhältnis (KBV; engl. P/B ratio oder P/BV)
    #print('\nKurs-Buchwert-Verhältnis:: ' + str(PB))

    #EPSD = float(Fundamentals['EPS - Net Income - Diluted'])
    #print('\nEPS: ' + str(EPSD))

    #Quick = float(Fundamentals['Quick Ratio'])
    #print('\nQuick Ratio: ' + str(Quick))

    #Current = float(Fundamentals['Current Ratio'])
    #print('\nCurrent Ratio: ' + str(Current))

    #sector = Sector.SectorIndustry(ticker)

    # Sector and Industry
    #print('\nSector: '+ sector[0] +'  Industry: '+ sector[1])

    #return Fundamentals
    return Fundamentals
