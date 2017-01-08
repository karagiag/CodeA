# Calculate Capitalization of specific Stock
# Markus Werner
# 03.10.2016
##################################################################################################

def fundamentals(compyNumber, today, price):

    # Header
    #from yahoo_finance import Share
    from pprint import pprint
    import time
    try:
        import Fundamentals_Value
        import Sector
    except:
        from modules.FinApp import Fundamentals_Value
        from modules.FinApp import Sector

    #ticker = 'TSLA'
    #today = str("2013-10-03")
    # Import Fundamentals of the current date
    Fundamentals = Fundamentals_Value.analyze(compyNumber, today)

    # Market Capitalization
    try:
        shares = float(Fundamentals['Shares Outstanding'])  # Shares Outstanding
        capitalization = shares * price # Market Capitalization
    except:
        shares = float('NaN')
        capitalization = float('NaN')

    ## Share Price KPIs

    # price / cash flow ratio, Kurs Cashflow Verhätlnis (KCF)
    try:
        PCF = price / float(Fundamentals['Free Cash Flow Per Share'])
    except:
        PCF = float('NaN')

    # ~price sales ratio, Kurs Umsatz Verhätlnis (KRF / KUV)
    try:
        PSR = price / float(Fundamentals['Total Revenue'])
    except:
        PSR = float('NaN')

    # P/B ratio, Kurs Buchwert Verhältnis
    try:
        PB = price / float(Fundamentals['Total Assets Per Share'])
    except:
        PB = float('NaN')

    # EPS (Earnings Per Share)- Net Income - Diluted
    try:
        EPSD = float(Fundamentals['EPS - Net Income - Diluted'])
    except:
        EPSD = float('NaN')

    # Quick Ratio (indicator of company's short term liquidity)
    try:
        quick = float(Fundamentals['Quick Ratio'])
    except:
        quick = float('NaN')

    # Current ratio (a liquidity ratio measuring a company's ability to pay short-term and long-term obligations)
    try:
        current = float(Fundamentals['Current Ratio'])
    except:
        current = float('NaN')

    #sector = Sector.SectorIndustry(ticker)

    # Sector and Industry
    #print('\nSector: '+ sector[0] +'  Industry: '+ sector[1])

    #return Fundamentals
    return shares, capitalization, PCF, PSR, PB, EPSD, quick, current
