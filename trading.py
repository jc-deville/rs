
import robin_stocks.robinhood as rs
import math as m
import time
import logging
import functions as f
import importlib
import csv

#setup log file
logging.basicConfig(filename='./logs/trading_20220126.log',format='%(asctime)s,%(message)s', datefmt='%m/%d/%Y,%I:%M:%S %p', level=logging.INFO)

#logging.info('

f.loginUser()
startinfo = f.accSts()
sts = startinfo['sts']
#logging.info('sts:')
#logging.info(sts)

delta = 0.0005
price15s = []
realrsi = []
realDelta = []
macd15s = []
price1m = []
avg1rsi = []
avg1Delta = []
price5m = []
avg5rsi = []
macd5m = []
avg5Delta = []
roll5m = []
roll5rsi = []
macd5mroll = []
roll5Delta = []
sma5x5 = []
smaTrend = []
tradenum = 1
tradeid = 'trade'+str(tradenum)
tradePrice = ['tradePrice']
currVal = startinfo['accountVal']
currQuant = startinfo['quant']
tradeActive = startinfo['tradeActive']
tradeTest = False
ticker = startinfo['ticker']
ATH = 0
ATL = 0

timeC = 1


crypInfo = rs.get_crypto_info(ticker)

minPriceInc = crypInfo['min_order_price_increment']
minPrice = float(minPriceInc)
minQuantInc = crypInfo['min_order_quantity_increment']
minQuant = float(minQuantInc)

fpath = '/etc/trading/rs/data/' + ticker + 'log.csv'

try:
    with open(fpath,'r') as fprice:
        reader = csv.DictReader(fprice)
        k = 1
        for row in reader:
            mark_price = float(row['mark'])
            bid_price = float(row['bid'])
            ask_price = float(row['ask'])
            if ATL == 0:
                ATL = mark_price
            if ATH == 0:
                ATH = mark_price

            price15s.append(mark_price)
            if len(price15s) > 100:
                del price15s[0]

            if(len(price15s) > 1):
                realDelta.append(price15s[-1] - price15s[-2])
                if len(realDelta) > 100: del realDelta[0]
                if len(price15s) > 60:
                    rsin =f.rsi(price15s,60)
                    realrsi.append(rsin)
#                if len(price15s) > 40:
                macdnow = f.macd(price15s,12,26,9)
                macd15s = macdnow['macd']
                if len(realrsi) > 15: del realrsi[0]
                rsin = 0
            if (len(price15s) > 4) & (k%10 == 0):
                price1m.append(f.avgCalc(price15s,4))
                if len(price1m) > 14:
                    rsin = f.rsi(price1m,14)
                    avg1rsi.append(rsin)
                if len(avg1rsi) > 15: del avg1rsi[0]
                rsin = 0
            if (len(price1m) > 1) & (k%10 == 0):
                avg1Delta.append(price1m[-1] - price1m[-2])
            if (len(price1m) > 4) & (k%50 == 0):
                price5m.append(f.avgCalc(price1m,5))
                if len(price5m) > 50: del price5m[0]
                if len(price5m) > 14:
                    rsin = f.rsi(price5m,14)
                    avg5rsi.append(rsin)
#                if len(price5m) > 40:
                macdnow5m = f.macd(price5m,12,26,9)
                macd5m = macdnow5m['macd']
                if len(avg5rsi) > 15: del avg5rsi[0]
                rsin = 0
            if (len(price5m) > 1) & (k%50 == 0):
                avg5Delta.append(price5m[-1] - price5m[-2])
                if len(avg5Delta) > 10: del avg5Delta[0]
            if (len(price1m) > 4) & (k%10 == 0):
                roll5m.append(f.avgCalc(price1m,5))
                if len(roll5m) > 50: del roll5m[0]
                if len(roll5m) > 14:
                    rsin = f.rsi(roll5m,14)
                    roll5rsi.append(rsin)
                macdroll5m = f.macd(roll5m,12,26,9)
                if len(roll5rsi) > 15: del roll5rsi[0]
                rsin = 0
            if (len(roll5m) > 1) & (k%10 == 0):
                roll5Delta.append(roll5m[-1] - roll5m[-2])
                if len(roll5Delta) > 10: del roll5Delta[0]
            if (len(price5m) > 4) & (k%50 == 0):
                sma5x5.append(f.avgCalc(price5m,5))
                if len(sma5x5) > 10: del sma5x5[0]
            if (len(sma5x5) > 1) & (k%50 == 0):
                smaTrend.append(sma5x5[-1] - sma5x5[-2])
                if len(smaTrend) > 10: del smaTrend[0]

            if price15s[-1] > ATH: ATH = price15s[-1]
            if price15s[-1] < ATL: ATL = price15s[-1]

            k += 1
        logging.info("complete backlog")

except  Exception as e:
    logging.info(e)

try:
#    logging.info('inside try')
    while sts:
#        logging.info('inside while')
        min1 = timeC%4
        min5 = timeC%20
        rsin = 0

        quote = rs.get_crypto_quote(ticker)
        mark_price = float(quote['mark_price'])
        bid_price = float(quote['bid_price'])
        ask_price = float(quote['ask_price'])

        if ATL == 0:
            ATL = mark_price
#            logging.info('ATL : ' + str(ATL))
        if ATH == 0:
            ATH = mark_price
#            logging.info('ATH : ' + str(ATH))

        logOut = 'ATL,' + str(ATL) + ',ATH,' + str(ATH) + ','

        price15s.append(mark_price)
        if len(price15s) > 50:
            del price15s[0]
#        logging.info('Current Price: ' + str(price15s[-1]))
        logOut = logOut + 'Current Price ,' + str(price15s[-1]) + ','

        if(len(price15s) > 1):
            realDelta.append(price15s[-1] - price15s[-2])
            if len(realDelta) > 50: del realDelta[0]
            if len(price15s) > 20:
                rsin =f.rsi(price15s,20)
                realrsi.append(rsin)
#            if len(price15s) > 40:
            macdnow = f.macd(price15s,12,26,9)
            macd15s = macdnow['macd']
            if len(realrsi) > 15: del realrsi[0]
#            rsin = rsi(price15s,20)
#            logging.info('Real Delta : ' + str(realDelta[-1]))
            logOut = logOut + 'Current Delta ,' + str(realDelta[-1]) + ','
            logOut = logOut + 'RSI(20) ,' + str(rsin) + ','
            logOut = logOut + 'MACD15s(12,26,9),' + str(macd15s[-1]) + ','
            rsin = 0
        if (len(price15s) > 4) & (min1 == 0):
            price1m.append(f.avgCalc(price15s,4))
            if len(price1m) > 14:
                rsin = f.rsi(price1m,14)
                avg1rsi.append(rsin)
            if len(avg1rsi) > 15: del avg1rsi[0]
            logOut = logOut + 'RSI(14),' + str(rsin) + ','
            logOut =  logOut + '1Min Avg,' + str(price1m[-1]) + ','
            rsin = 0
        if (len(price1m) > 1) & (min1 == 0):
            avg1Delta.append(price1m[-1] - price1m[-2])
            logOut = logOut + '1Min Delta,' + str(avg1Delta[-1]) + ','
        if (len(price1m) > 4) & (min5 == 0):
            price5m.append(f.avgCalc(price1m,5))
            if len(price5m) > 50: del price5m[0]
            if len(price5m) > 14:
                rsin = f.rsi(price5m,14)
                avg5rsi.append(rsin)
#            if len(price5m) > 40:
            macdnow5m = f.macd(price5m,12,26,9)
            macd5m = macdnow5m['macd']
            if len(avg5rsi) > 15: del avg5rsi[0]
#            logging.info('5Min Avg : ' + str(price5m[-1]))
            logOut = logOut + 'RSI5m(14),' + str(rsin) + ','
            logOut = logOut + '5Min Avg,' + str(price5m[-1]) + ','
            logOut = logOut + 'MACD(5m,12,26,9),' + str(macd5m[-1]) + ','
            rsin = 0
        if (len(price5m) > 1) & (min5 == 0):
            avg5Delta.append(price5m[-1] - price5m[-2])
            if len(avg5Delta) > 10: del avg5Delta[0]
            logOut = logOut + '5Min Delta,' + str(avg5Delta[-1]) + ','
        if (len(price1m) > 4) & (min1 == 0):
            roll5m.append(f.avgCalc(price1m,5))
            if len(roll5m) > 50: del roll5m[0]
            if len(roll5m) > 14:
                rsin = f.rsi(roll5m,14)
                roll5rsi.append(rsin)
            macdroll5m = f.macd(roll5m,12,26,9)
            macd5mroll = macdroll5m['macd']
            if len(roll5rsi) > 15: del roll5rsi[0]
            logOut = logOut + '5Min Roll,' + str(roll5m[-1]) + ','
            logOut = logOut + 'RSI5mRoll(14),' + str(rsin) + ','
            logOut = logOut + 'macd(5mRoll,12,26,9),' + str(macd5mroll[-1]) + ','
            rsin = 0
        if (len(roll5m) > 1) & (min1 == 0):
            roll5Delta.append(roll5m[-1] - roll5m[-2])
            if len(roll5Delta) > 10: del roll5Delta[0]
            logOut = logOut + '5MinRoll Delta,' + str(roll5Delta[-1]) + ','
        if (len(price5m) > 4) & (min5 == 0):
            sma5x5.append(f.avgCalc(price5m,5))
            if len(sma5x5) > 10: del sma5x5[0]
#            logging.info('SMA Last : ' + str(sma5x5[-1]))
            logOut = logOut + 'SMA,' + str(sma5x5[-1]) + ','
        if (len(sma5x5) > 1) & (min5 == 0):
            smaTrend.append(sma5x5[-1] - sma5x5[-2])
            if len(smaTrend) > 10: del smaTrend[0]
#            logging.info('SMA Delta : ' + str(smaTrend[-1]))
            logOut = logOut + 'SMA Delta,' + str(smaTrend[-1]) + ','

#        logging.info('ATH : ' + str(ATH))
#        logging.info('ATL : ' + str(ATL))

        logging.info(logOut)

        if price15s[-1] > ATH: ATH = price15s[-1]
        if price15s[-1] < ATL: ATL = price15s[-1]

        if  (min1 == 0):
            if tradeActive:
#                if price15s[-1] > ATH:
#                    ATH = price15s[-1]
#                    logging.info('ATH : ' + str(ATH))
#                if price15s[-1] < ATL: ATL = price15s[-1]

#                decisionData = {
#                    'side':'sell',
#                    'delta':delta,
#                    'tradePrice':tradePrice,
#                    'ATL':ATL,
#                    'ATH':ATH,
#                    'realTime':price15s,
#                    'realDelta':realDelta,
#                    'realrsi':realrsi,
#                    'avg1':price1m,
#                    'avg1Delta':avg1Delta,
#                    'avg1rsi':avg1rsi,
#                    'avg5':price5m,
#                    'avg5Delta':avg5Delta,
#                    'avg5rsi':avg5rsi,
#                    'roll5m':roll5m,
#                    'roll5rsi':roll5rsi,
#                    'roll5Delta':roll5Delta,
#                    'macd5mroll':macd5mroll,
#                    'sma':sma5x5,
#                    'smaDelta':smaTrend,
#                    'min1':min1,
#                    'min5':min5
#                    }

                decision = f.tradeDecision('sell',delta,tradePrice,ATL,ATH,price15s,realDelta,realrsi,price1m,avg1Delta,avg1rsi,price5m,avg5Delta,avg5rsi,roll5m,roll5rsi,roll5Delta,macd5mroll,sma5x5,smaTrend,min1,min5)
                logging.info('Trade Decision : ' + str(decision[0]) + ' @ limit : ' + str(decision[1]))
                decider = decision[0]
                if decider:
                    trade=rs.order_sell_crypto_by_quantity(ticker,currQuant)
                    limit = trade['price']
                    limit = float(limit)
                    logging.info('Sell ' + str(currQuant) + ' of ' + ticker + ' at $' + str(limit))
                    logging.info(trade)
                    tradeinfo = f.checkTrade(trade)
                    currVal = currVal + currQuant * limit
                    currVal = f.truncate(currVal,2)
                    tradeActive = False
                    logging.info(tradeinfo)
                    logging.info('Current Portfolio Value: ' + str(currVal))
                    ATL = limit
            else:

#                decisionData = {
#                    'side':'buy',
#                    'delta':delta,
#                    'tradePrice':0,
#                    'ATL':ATL,
#                    'ATH':ATH,
#                    'realTime':price15s,
#                    'realDelta':realDelta,
#                    'realrsi':realrsi,
#                    'avg1':price1m,
#                    'avg1Delta':avg1Delta,
#                    'avg1rsi':avg1rsi,
#                    'avg5':price5m,
#                    'avg5Delta':avg5Delta,
#                    'avg5rsi':avg5rsi,
#                    'roll5m':roll5m,
#                    'roll5rsi':roll5rsi,
#                    'roll5Delta':roll5Delta,
#                    'macd5mroll':macd5mroll,
#                    'sma':sma5x5,
#                    'smaDelta':smaTrend,
#                    'min1':min1,
#                    'min5':min5
#                    }

                decision = f.tradeDecision('buy',delta,0,ATL,ATH,price15s,realDelta,realrsi,price1m,avg1Delta,avg1rsi,price5m,avg5Delta,avg5rsi,roll5m,roll5rsi,roll5Delta,macd5mroll,sma5x5,smaTrend,min1,min5)
                logging.info('Trade Decision : ' + str(decision[0]) + ' @ limit : ' + str(decision[1]))
                decider = decision[0]
                if decider:
#                    priceDev = (avg1Delta[-1] + avg1Delta[-2]) / 2
#                    limit = decision[1]
#                    limit = ask_price + priceDev
#                    limit = minLimit(limit,minPrice)
#                    limit = truncate(limit,2)
                    limit = ask_price
                    currQuant = currVal / limit
#                    currQuant = f.truncate(currQuant,2)
                    currQuant = f.minLimit(currQuant,minQuant)
                    currQuant = f.truncate(currQuant,6)
                    trade=rs.order_buy_crypto_by_quantity(ticker,currQuant)
                    tradeinfo = f.checkTrade(trade)
                    tradeID = trade['id']
                    tradeData = rs.get_crypto_order_info(tradeID)
                    currQuant = trade['quantity']
                    currQuant = float(currQuant)
                    limit = tradeData['average_price']
                    limit = float(limit)
                    logging.info('min limit : ' + str(minPrice) + ' @ min quant : ' + str(minQuant))
                    logging.info('limit : ' + str(limit) + ' @ quantity : ' + str(currQuant))
#                    trade=rs.order_buy_crypto_by_price(ticker,currVal)
                    logging.info('Buy ' + str(currQuant) + ' of ' + ticker + ' at $' + str(limit))
                    currVal = currVal - currQuant*limit
                    currVal = f.truncate(currVal,2)
                    tradePrice = limit
                    tradeActive = True
                    logging.info(tradeinfo)
                    logging.info('Current Portfolio Value: ' + str(currVal))
                    ATH = limit
                    ATL = price15s[-1]

        time.sleep(15)

        importlib.reload(f)

        startinfo=f.accSts()
        sts = startinfo['sts']

        if timeC == 5760:
            f.loginUser()
            timeC = 0

        timeC = timeC + 1

except  Exception as e:
    logging.info(e)

#logging.info(price1m)
logging.info("end")

