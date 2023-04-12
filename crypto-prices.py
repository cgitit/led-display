#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys
import os
import time

#Grab each price and overwrite the text file for each crypto

def bitcoinSettings():
	bfile = '/home/pi/static/crypto/Bitcoin'
	cur_price = str(float(requests.get("https://api.pro.coinbase.com/products/BTC-USD/ticker").json()["price"]))
	with open(bfile, "w") as f:
		f.write(cur_price)
		f.close()

def ethSettings():
	bfile = '/home/pi/static/crypto/ETH'
	cur_price = str(float(requests.get("https://api.pro.coinbase.com/products/ETH-USD/ticker").json()["price"]))
	with open(bfile, "w") as f:
		f.write(cur_price)
		f.close()

def ltcSettings():
	bfile = '/home/pi/static/crypto/LTC'
	cur_price = str(float(requests.get("https://api.pro.coinbase.com/products/LTC-USD/ticker").json()["price"]))
	with open(bfile, "w") as f:
		f.write(cur_price)
		f.close()
