import robin_stocks.robinhood as rs
import math as m
import time
import logging
import pyotp
import csv
from datetime import datetime as dt

#setup log file
logging.basicConfig(filename='./logs/trading_20220126.log',format='%(asctime)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

def loginUser():
    login=rh_login()
# Delete third argument of rs.login function below if you do not use a OTP to login to RH.
    rs.login(username=login[0],
        password=login[1],
        mfa_code=login[2])

def rh_login():

    results=[]
    config = accSts()
    results.append(config['user'])
    results.append(config['pass'])
# Comment out below row if you do not use a OTP to login to RH.
    results.append(pyotp.TOTP(config['totp']).now())

    return(results)

def accSts():
    configpath = './config.csv'
    with open(configpath,'r') as config:
        reader = csv.DictReader(config)
        for row in reader:
            user = row['user']
            password = row['pass']
            totp = row['totp']
            sts = row['runSys']
            tradeAct = row['tradeActive']
            accVal =  row['accountVal']
            tradePrice = row['tradePrice']
            currQuant = row['currQuant']
            ticker = row['ticker']
            testing = row['test']

    if sts == 'True':
        sts = True
    else:
        sts = False
    if tradeAct == 'True':
        tradeAct = True
    else:
        tradeAct = False
    results= {
        'user':user,
        'pass':password,
        'totp':totp,
        'sts':sts,
        'tradeActive':tradeAct,
        'accountVal':accVal,
        'quant':currQuant,
        'tradePrice':tradePrice,
        'ticker':ticker,
        'test':testing
        }
    return results

def marketopen():

    dtstr=dt.now().strftime("%Y-%m-%d")
    market=rs.get_market_hours('XNYS',dtstr)
    mksts=market['is_open']
    mkopen=market['opens_at']
    mkclose=market['closes_at']
    mkopen=mkopen.replace("T"," ").replace("Z","")
    mkclose=mkclose.replace("T"," ").replace("Z","")
    currtm=dt.utcnow().isoformat(sep=' ')
    currtm=currtm[:len(currtm)-7]
    if (currtm >= mkopen) & (currtm <= mkclose) & mksts:
        marketopen=True
    else:
        marketopen=False

    return marketupen

def secType(ticker):
    pairs = rs.get_currency_pairs()
    list=[]
    for item in pairs:
        list.append(item['asset_currency']['code'])
    is_crypto = ticker in list

    return is_crypto

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return m.trunc(stepper * number) / stepper

def avgCalc(num, dig, start = 1):
    sum = 0
#    dig = 5

    div = dig
    dig += start

    while start < dig:
#        pos = (-1)*i
        sum += num[-start]
        start += 1
    avg = sum / div
    return avg

def checkTrade(trade,crypto):
    j = 1
    emptyCheck = False
    tradeID = trade['id']
    if crypto:
        tradeInfo = rs.get_crypto_order_info(tradeID)
    else:
        tradeInfo = rs.get_stock_order_info(tradeID)
    tradeState = tradeInfo['state']
    while emptyCheck == False:
        if tradeState == 'filled':
            emptyCheck = True
#        logging.info('tradeid : ' + str(tradeID) + 'execution time: ' + str(j) + ' seconds')
        j += 1
        if crypto:
            tradeDate = rs.get_crypto_order_info(tradeID)
        else:
            tradeData = rs.get_stock_order_info(tradeID)
        tradeState = tradeDate['state']
        time.sleep(1)
    return 'Trade ' + tradeID + ' executed in ' + str(j) + ' seconds'

def minLimit(limit, min_increment):
    testLimit = limit / min_increment
    testLimit = int(testLimit)
    testLimit = testLimit * min_increment
    return testLimit

def avgDelta(range,num, start):
    sum = 0
    deltas = []
    pos = []
    i = start-num

    while i < start + num:
        pos.append(i)
        i += 1

    if len(range) < start + num + 1:
        returnVal = 0
    else:
        for j in pos:
            if j < start + num:
                delta = range[j+1]-range[j]
                deltas.append(delta)
                sum += delta
            j += 1
        returnVal = sum / (num-1)
    return returnVal

def rsi(data,pd):

    pos = []
    neg = []
    i = 1

    if len(data) <= pd: pd = len(data)

    while i < pd:
        if (data[-i] - data[-(i+1)]) < 0:
            neg.append(-(data[-i] - data[-(i+1)]))
        else:
            pos.append(data[-i] - data[-(i+1)])
        i += 1

    if len(pos) > 0: avgPos = avgCalc(pos,len(pos))
    else: avgPos = 0
    if len(neg) > 0: avgNeg = avgCalc(neg,len(neg))
    else: avgNeg = 0

    if avgNeg == 0: rsi = 100
    else:
        rsi = 100 - (100 / (1 + (avgPos / avgNeg)))

    return rsi

def tradeDecision(side, delta, tradeprice, ATL, ATH, realTime, realDelta, realrsi, avg1, avg1Delta, avg1rsi, avg5, avg5Delta, avg5rsi, roll5m, roll5rsi, roll5Delta, macd5mroll, sma, smaDelta,min1 = 0,min5 = 0):

#    side=decisionData['side']
#    delta=decisionData['delta']
#    tradeprice=decisionData['tradeprice']
#    ATL=decisionData['ATL']
#    ATH=decisionData['ATH']
#    realTime=decisionData['realTime']
#    realDelta=decisionData['realDelta']
#    realrsi=decisionData['realrsi']
#    avg1=decisionData['avg1']
#    avg1Delta=decisionData['avgDelta']
#    avg1rsi=decisionData['avg1rsi']
#    avg5=decisionData['avg5']
#    avg5Delta=decisionData['avg5Delta']
#    avg5rsi=decisionData['avg5rsi']
#    roll5m=decisionData['roll5m']
#    roll5rsi=decisionData['roll5rsi']
#    roll5Delta=decisionData['roll5Delta']
#    macd5mroll=decisionData['macd5mroll']
#    sma=decisionData['sma']
#    smaDelta=decisionData['smaDelta']
#    min1=decisionData['min1']
#    min5=decisionData['min5']


    limit = 0
    decision = [False,limit] #true/false decision with a reccomended limit price [true,limit]

#    logging.info(',avg5 length: ' + str(len(avg5)))
#    logging.info(',roll5 length: ' + str(len(roll5m)))

    macd15s = macd(realTime,12,26,9)
    macd1m = macd(avg1,12,26,9)
    macd5m = macd(avg5,12,26,9)
    macdDelta = macd1m['emaDelta']
    macdReal = macd15s['macd']
    macd1 = macd1m['macd']
    macd5 = macd5m['macd']

#    logging.info(',macd1m : ' + str(macd1[-1]))

#    logging.info(macd5mroll)

    if side == 'sell':

        logging.info('inside sell')

#        gainDelta = tradeprice + (0.8*(ATH - tradeprice))
#        if (realTime[-1] < gainDelta) & (avg1Delta[-1] < 0):
#            decision = [True,limit]
        if (len(avg1rsi) > 2):
            if ((avg1rsi[-1] - avg1rsi[-2]) < -10):
                limit = ((avg1Delta[-1] + avg1Delta[-2]) / 2) + realTime[-1]
#                decision = [True,limit]
#                logging.info('1m RSI Delta > -8')
            if len(roll5rsi) > 1:
                if (avg1rsi[-2] < avg1rsi[-3]) & (avg1rsi[-1] < avg1rsi[-2]) & (roll5rsi[-1] < roll5rsi[-2]) & (avg1Delta[-1] < 0):
                    limit = ((avg1Delta[-1] + avg1Delta[-2]) / 2) + realTime[-1]
#                    decision = [True,limit]
#                    logging.info('1m RSI and 5m RSI and 1m Delta trending down')
        if (len(macd5mroll) > 1):
            if (macd5mroll[-1] < 0) & ((roll5rsi[-1] < 70) & (roll5rsi[-2] < 70)):
                limit = ((avg1Delta[-1] + avg1Delta[-2]) / 2) + realTime[-1]
                decision = [True,limit]
                logging.info('macd5[-1] < 0')

    if side == 'buy':

        if (len(macd5) > 1) & (min5 == 0):
            if (macd5[-1] > 0) & (macd5mroll[-1] > 0):
                limit = ((avg1Delta[-1] + avg1Delta[-2]) / 2) + realTime[-1]
                decision = [True,limit]
        if (len(macd5mroll) > 2):
            if (macd5mroll[-1] > 0) & (macd5mroll[-2] > 0):
                limit = ((avg1Delta[-1] + avg1Delta[-2]) / 2) + realTime[-1]
                decision = [True,limit]
                logging.info('roll5macd trend up')
        if len(roll5rsi) > 3:
            if (roll5rsi[-2] > 60) & (roll5rsi[-1] > 60):
                if (roll5rsi[-1] > roll5rsi[-2]) & (roll5rsi[-2] > roll5rsi[-3]) & (roll5rsi[-3] > roll5rsi[-4]):
                    if (roll5Delta[-1] > 0) & (roll5Delta[-2] > 0):
                        limit = ((avg1Delta[-1] + avg1Delta[-2]) / 2) + realTime[-1]
                        decision = [True,limit]
                        logging.info('roll5RSI increase')
        else:
            decision = [False,0]
#            if macd1[-1] > 0:
#                limit = ((avg1Delta[-1] + avg1Delta[-2]) / 2) + realTime[-1]
#                decision = [True,limit]

#    decision = [False,limit]

    return decision

def ema(data,term,ema=None):
    if (ema is None) or (len(ema) < 1):
        ema = []
        if len(data) < (term + 1):
            ema[0] = 0
            return ema
        else:
            for i in range(0,len(data)-1):
                if i == term:
                    dig = len(data) - term - 1
                    ema.append(avgCalc(data,term,dig))
                if i > term:
                    ema.append((data[i]*(2/(term+1))) + (ema[-1]*(1-(2/(term+1)))))
    else:
        ema.append((data[-1]*(2/(term+1))) + (ema[-1]*(1-(2/(term+1)))))
    return ema

def macd(data,fast,slow,sig):

    rng = slow + sig + 5


    if len(data) <= rng:
        emafast = [0]
        emaslow = [0]
        emasig = [0]
        macd = [0]
        macdsig = [0]
    else:
        emafast = []
        emaslow = []
        emasig = []
        macd = []
        macdsig = []

        emafast = ema(data,fast,emafast)
        emaslow = ema(data,slow,emaslow)
        deltaemas = len(emafast) - len(emaslow)
        for i in range(0,len(emaslow)):
            macd.append(emafast[i + deltaemas] - emaslow[i])
        emasig = ema(macd,sig,emasig)
        deltamacd = len(macd) - len(emasig)
        for j in range(0,len(emasig)):
            macdsig.append(macd[j + deltamacd] - emasig[-j])
#        macdcurr = macd[-1] - emasig[-1]
    return {'emafast': emafast,'emaslow': emaslow,'emaDelta': macd,'emasig': emasig,'macd': macdsig}

def candles(data,intime,outtime):

    if intime[-1] == 's':
        itime = int(intime[:-1])
    if intime[-1] == 'm':
        itime = intime[:-1]
        itime = int(itime) * 60
    if intime[-1] == 'h':
        itime = intime[:-1]
        itime = int(itime) * 3600
    if outtime[-1] == 's':
        otime = int(outtime[:-1])
    if outtime[-1] == 'm':
        otime = outtime[:-1]
        otime = int(otime) * 60
    if outtime[-1] == 'h':
        otime = outtime[:-1]
        otime = int(otime) * 3600

    mult = otime / itime
    mult = int(mult)
    size = len(data)
    quant = size / mult
    quant = int(quant)

    #for item in data:


    return 0
