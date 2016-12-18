import time, csv #, company

def analyze(ticker, today):

    ## INPUTS
    lookfor_ticker = ticker
    #today = str("2014-08-03")
    today = time.strptime(today, "%Y-%m-%d")

    ## Unternehmen finden
    path = "/home/oliver/Repositories/CodeA/codea/modules/Fundamentals/"
    filename_company = "Companies.csv"
    file_company = path + filename_company

    def company_search (lookfor_ticker,file_company):
        print('Looking for Compynumber %s')
        headers = None
        content = {}
        reader=csv.reader(open(file_company), delimiter=';')
        for row in reader:
            if reader.line_num == 1:
                headers = row[0:] # Header für Dictionary Keys
            else:
                content[row[8]] = dict(zip(headers, row[0:])) # Einträge den Keys zuordnen
        Compnumber =  (content[lookfor_ticker]["compnumber"]) # Compnumber für gesuchten Ticker
        filename = Compnumber + ".csv"
        file = path + filename
        return file


    ## Einlesen der Fundamentaldaten
    try:
        file_fundamental = company_search(lookfor_ticker, file_company)
        reader = csv.reader(open(file_fundamental))
    except:
        print('Ticker not Found')
        exit()

    # Bewertungszeitraum in Datei finden (Datum)
    def reporting_date (lookfor_date):
        try:
            flag_date = 0
            for row in reader:
                if flag_date == 1:
                    date_row = row[5]
                    rowtime_python = time.strptime(date_row, "%Y-%m-%d")
                    if rowtime_python <= lookfor_date:
                        last_date = date_row
                    else:
                        break
                else:
                    flag_date = 1
            return last_date
        except:
            print('\nDate before Fundamental Data Recording')
            exit()


    ## Dictionary anlegen fuer alle Kennzahlen des aktuellen Bewertungszeitraums
    report_date = reporting_date(today) # YYY-MM-DD
    print('\nReporting Period: ' + report_date)

    headers = None
    content = {}
    reader=csv.reader(open(file_fundamental))
    for row in reader:
        if reader.line_num == 1:
            headers = row[0:] # Header für Dictionary Keys
        else:
            if row[5] == report_date: # Einträge den Keys zuordnen
                content[row[31]] = dict(zip(headers, row[0:]))

    Fundamentals = {'Cash From Operations' : float(content['Cash From Operations']['amount']), \
            #'Cash End of Year' : float(content['Cash, End of Year']['amount']),\
            'Free Cash Flow Per Share' : float(content['Free Cash Flow Per Share']['amount']),\
            'Net Income' : float(content['Net Income']['amount']), \
            'Net Margin' : float(content['Net Margin']['amount']), \
            #'Return on Assets' : float(content['Return on Assets']['amount']), \
            #'Return on Equity' : float(content['Return on Equity']['amount']), \
            #'Revenue Per Share' : float(content['Revenue Per Share']['amount']), \
            #'Revenue to Assets' : float(content['Revenue to Assets']['amount']), \
            'Shares Outstanding' : float(content['Shares Outstanding']['amount']), \
            #'Total Assets' : float(content['Total Assets']['amount']), \
            'Total Assets Per Share' : float(content['Total Assets Per Share']['amount']), \
            #'Total Debt to Equity' : float(content['Total Debt to Equity']['amount']), \
            #'Total Liabilities' : float(content['Total Liabilities']['amount']), \
            'Total Revenue' : float(content['Total Revenue']['amount']), \
            'EPS - Net Income - Diluted' : float(content['EPS - Net Income - Diluted']['amount']),\
            'Quick Ratio' : float(content['Quick Ratio']['amount']),\
            'Current Ratio' : float(content['Current Ratio']['amount']),\
            }

    return Fundamentals
