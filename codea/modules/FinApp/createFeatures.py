from math import sqrt

def createFeatures(df):

    data = df['Price'].values

    # price change features
    netchange = [0]
    netchange += [data[i]-data[i-1] for i in range(1, len(data))]
    percentchange = [netchange[i]/data[i] * 100 for i in range(0, len(data))]

    # volatility based on price change
    sqrt254 = sqrt(254) # square root of yearly trading days
    volatility10 = [0] * 10
    volatility20 = [0] * 20
    volatility30 = [0] * 30
    volatility10 += [sqrt254 * np.std(percentchange[i-10:i]) for i in range(10, len(data))]
    volatility20 += [sqrt254 * np.std(percentchange[i-20:i]) for i in range(20, len(data))]
    volatility30 += [sqrt254 * np.std(percentchange[i-30:i]) for i in range(30, len(data))]

    # add features to dataframe
    df['featPPO'] = df['PPO']
    df['featMFI'] = df['MFI']
    df['Netchange'] = netchange
    df['Percentage Change'] = percentchange
    df['10 day volatility'] = volatility10
    df['20 day volatility'] = volatility20
    df['30 day volatility'] = volatility30

    # check if shorter EMA crosses a longer one
    df['EMA 15 / 30 posx'], df['EMA 15 / 30 negx'], df['EMA 15 / 30 higher'] = crossing(df['EMA 15'].values, df['EMA 30'].values)

    df['EMA 15 / 50 posx'], df['EMA 15 / 50 negx'], df['EMA 15 / 50 higher'] = crossing(df['EMA 15'].values, df['EMA 50'].values)

    df['EMA 15 / 100 posx'], df['EMA 15 / 100 negx'], df['EMA 15 / 100 higher'] = crossing(df['EMA 15'].values, df['EMA 100'].values)

    df['EMA 15 / 200 posx'], df['EMA 15 / 200 negx'], df['EMA 15 / 200 higher'] = crossing(df['EMA 15'].values, df['EMA 200'].values)

    df['EMA 30 / 50 posx'], df['EMA 30 / 50 negx'], df['EMA 30 / 50 higher'] = crossing(df['EMA 30'].values, df['EMA 50'].values)

    df['EMA 30 / 100 posx'], df['EMA 30 / 100 negxx'], df['EMA 30 / 100 higher'] = crossing(df['EMA 30'].values, df['EMA 100'].values)

    df['EMA 30 / 200 posx'], df['EMA 30 / 200 negx'], df['EMA 30 / 200 higher'] = crossing(df['EMA 30'].values, df['EMA 200'].values)

    df['EMA 50 / 100 posx'], df['EMA 50 / 100 negx'], df['EMA 50 / 100 higher'] = crossing(df['EMA 50'].values, df['EMA 100'].values)

    df['EMA 50 / 200 posx'], df['EMA 50 / 200 negx'], df['EMA 50 / 200 higher'] = crossing(df['EMA 50'].values, df['EMA 200'].values)

    df['EMA 100 / 200 pox'], df['EMA 100 / 200 negx'],df['EMA 100 / 200 higher'] = crossing(df['EMA 100'].values, df['EMA 200'].values)


    # check if price crosses an EMA

    df['Price / EMA 15 posx'], df['Price / EMA 15 negx'], df['Price / EMA 15 higher'] = crossing(df['Price'].values, df['EMA 15'].values)

    df['Price / EMA 30 posx'], df['Price / EMA 30 negx'], df['Price / EMA 30 higher'] = crossing(df['Price'].values, df['EMA 30'].values)

    df['Price / EMA 50 posx'], df['Price / EMA 50 negx'], df['Price / EMA 50 higher'] = crossing(df['Price'].values, df['EMA 50'].values)

    df['Price / EMA 100 posx'], df['Price / EMA 100 negx'], df['Price / EMA 100 higher'] = crossing(df['Price'].values, df['EMA 100'].values)

    df['Price / EMA 200 posx'], df['Price / EMA 200 negx'], df['Price / EMA 200 higher'] = crossing(df['Price'].values, df['EMA 200'].values)

    # check if EMA of MACD crosses MACD
    df['MACD posx'], df['MACD negx'], df['MACD higher'] = crossing(df['MACD EMA'].values, df['MACD'].values)

    # check if EMA of PPO crosses PPO
    df['PPO posx'] , df['PPO negx'],  df['PPO higher'] = crossing(df['PPO EMA'].values, df['PPO'].values)



    # create features for bollinger
    higheraverage = [] # price higher than average bollinger band
    higherhigh = [] # price higher than upper bollinger band
    lowerlow = [] # price lower than lower bollinger band

    bollinger = df['Bollinger'].values
    bollingerhigh = df['Bollinger high'].values
    bollingerlow = df['Bollinger low'].values
    for i in range (0, len(data)):
            # check if price is higher than Bollinger
            if data[i] > bollinger[i]:
                higheraverage.append(1)
            else:
                higheraverage.append(0)

            if data[i] > bollingerhigh[i]:
                higherhigh.append(1)
            else:
                higherhigh.append(0)

            if data[i] < bollingerlow[i]:
                lowerlow.append(1)
            else:
                lowerlow.append(0)

    df['Bollinger higher'] = higheraverage
    df['Bollinger higher high'] = higherhigh
    df['Bollinger lower low'] = lowerlow

    # create features for Money Flow Index:
    strongoverbought = overbought = oversold = strongoversold = [0] * len(df)
    MFI = df['MFI'].values
    for i in range(0, len(df)):
        if MFI[i] > 90:
            strongoverbought[i] = 1
            overbought[i] = 1
        if MFI[i] > 80:
            overbought[i] = 1
        elif MFI[i] < 10:
            oversold[i] = 1
            strongoversold[i] = 1
        elif MFI[i] < 20:
            oversold[i] = 1

    df['MFI strong overbought'] = strongoverbought
    df['MFI overbought'] = overbought
    df['MFI oversold'] = oversold
    df['MFI strong oversold'] = strongoversold


    return df
