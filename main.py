#!/usr/bin/env python3

import robin_stocks.robinhood as rs
import math as m
import functions as f
import importlib
import csv
import os
import pathlib
import logging
from datetime import datetime as dt
import time

logging.basicConfig(filename='./data/priceLog.log',format='%(asctime)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

startinfo = f.accSts()
sts = startinfo['sts']
ticker = startinfo['ticker']
pricelog = './data/' + ticker + 'log.csv'
pricelogHeader = ['date','time','ticker','mark','bid','ask']
file = pathlib.Path(pricelog)

if file.exists():
    #file exist
    True
else:
    with open(pricelog,'w+',newline='') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames = pricelogHeader)
        writer.writeheader()


f.loginUser()

is_crypto = f.secType(ticker)

if is_crypto:
    market = True
else:
    market = f.marketopen()

while (sts == True) & (market == True):

    if secnow%5 == 0:
        try:
            if is_crypto:
                quote = rs.get_crypto_quote(ticker)
            else:
                quote = rs.get_quotes(ticker)

            writedict = {'date':datenow,'time':timenow,'ticker':ticker,'mark':quote['mark_price'],'bid':quote['bid_price'],'ask':quote['ask_price']}

            with open(pricelog,'a',newline='') as f:

                writer = csv.DictWriter(f,fieldnames = pricelogHeader)

                writer.writerow(writedict)

            logging.info(str(writedict))

        except Exception as e:
            logging.info(e)
    
    if is_crypto:
        market = True
    else:
        market = f.marketopen()

    time.sleep(1)

#    startinfo = f.accSts()
#    sts = startinfo['sts']

