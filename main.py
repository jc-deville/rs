#!/usr/bin/env python3

import robin_stocks.robinhood as rs
import math as m
import functions as f
import importlib
import csv
import os
import pathlib
import logging
from datetime import datetime
import time

logging.basicConfig(filename='/etc/trading/rs/data/priceLog.log',format='%(asctime)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

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



while sts == True:

    now = datetime.now()
    datenow = now.strftime("%m/%d/%Y")
    timenow = now.strftime("%H:%M:%S")
    secnow = now.strftime("%S")
    secnow = int(secnow)

    if secnow%5 == 0:
        try:
            quote = rs.get_crypto_quote(ticker)

            writedict = {'date':datenow,'time':timenow,'ticker':ticker,'mark':quote['mark_price'],'bid':quote['bid_price'],'ask':quote['ask_price']}

            with open(pricelog,'a',newline='') as f:

                writer = csv.DictWriter(f,fieldnames = pricelogHeader)

                writer.writerow(writedict)

            logging.info(str(writedict))

        except Exception as e:
            logging.info(e)

    time.sleep(1)

#    startinfo = f.accSts()
#    sts = startinfo['sts']

