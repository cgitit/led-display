#!/bin/env/python3

#Command line communications
import os

#time(sleep)
import time

#random numbers
import random

#Creates a shell to run program in parallel with python
import subprocess

#Used for sys.exit()
import sys

from threading import Timer

#Signal checks on the running program
import signal

#Crypto Prices crypto-prices.py
import crypto-prices
import urllib

image = ""
quote = ""
lyric = ""

#Loads a random image file in the paths location
def imgSettings():
	path = '/home/pi/static/images/'
	files = os.listdir(path)
	choice = random.choice(files)
	return path + choice

#Loads a random quote from a random file in paths location
def quoteSettings():
	path = '/home/pi/static/quotes/'
	files = os.listdir(path)
	choice = random.choice(files)
	with open(path + choice) as f:
		lines = f.readlines()
		quote = random.choice(lines)
		return quote

def redditSettings():
	path = '/home/pi/static/reddit/'
	files = os.listdir(path)
	choice = random.choice(files)
	with open(path + choice) as f:
		lines = f.readlines()
		reddit = random.choice(lines)
		return reddit

#Loads all the lyrics from a file in the paths location
def lyricSettings():
	path = '/home/pi/static/lyrics/'
	files = os.listdir(path)
	choice = random.choice(files)
	print(choice)
	with open(os.path.join(path, choice), 'r', encoding='utf-8') as f:
        	lines = (line.strip() for line in f)
        	lyric = ' - '.join(lines)
        	lyric = lyric.replace("'", '').replace('(', '[').replace(')', ']')
        	return lyric

#Connection test for getPrice() and reddit()
def connect(host="https://www.google.com"):
	try:
		urllib.request.urlopen(host)
		return True
	except:
		return False

#check if connected, then print prices for a random choice
def cryptoSettings():
	path = '/home/pi/static/crypto/'
	files = os.listdir(path)
	choice = random.choice(files)
	connected = connect()
	if connected == True:
		if choice == "Bitcoin":
			bitcoinPrices.bitcoinSettings()
		elif choice == "ETH":
			bitcoinPrices.ethSettings()
		elif choice == "LTC":
			bitcoinPrices.ltcSettings()
		with open(path + choice, "r") as f:
			price1 = f.readlines()
			price = choice + " Price: \$" + random.choice(price1)
			return price
	else:
		fontSet = fontSettings()
		setColor = ran_color()
		os.system("sudo ./scrolling-text-example --led-cols=64 -s 5 -y 8 -l 1 -f " + fontSet + " -C " + setColor + "Disconnected from the internet.")

#return path and random gif or movie
def movieSettings():
	path = '/home/pi/static/movies/'
	files = os.listdir(path)
	choice = random.choice(files)
	return path + choice

#choose a random font file to use
def fontSettings():
	path = '/home/pi/display32x64/rpi-rgb-led-matrix/fonts/'
	files = os.listdir(path)
	bdfFiles = []
	for file in files:
		if file.endswith(".bdf"):
			bdfFiles.append(file)
	choice = random.choice(bdfFiles)
	return path + choice

#What could this be?
colors = ["red", "green", "blue", "yellow", "orange", "purple", "indigo", "white"]


#add a space after the color
colors_id = {
	"red" : "255,0,0 ",
	"green" : "128,255,0 ",
	"blue" : "0,0,255 ",
	"yellow" : "255,255,0 ",
	"orange" : "255,128,0 ",
	"purple" : "127,0,255 ",
	"indigo" : "0,255,255 ",
	"white" : "255,255,255 "
	}

#Change to folder
def apiFolder():
	os.chdir("/home/pi/display32x64/rpi-rgb-led-matrix/examples-api-use/")

#Change to folder
def utilFolder():
	os.chdir("/home/pi/display32x64/rpi-rgb-led-matrix/utils/")

#Pick a random color
def ran_color():
	choice = random.choice(colors)
	chosen = colors_id[choice]
	return chosen

#Pick a random image
def images():
	image = imgSettings()
	return image

#Pick a random quote
def quotes():
	apiFolder()
	setColor = ran_color()
	quote = str(quoteSettings())
	fontSet = fontSettings()
	os.system("sudo ./scrolling-text-example --led-cols=64 -s 5 -y 8 -l 1 -f " + fontSet + " -C " + setColor + quote)

#check if connected, and display the headlines from /r/news. 
#Updated/controlled by supervisorctl reddit_headline.conf in /etc/sup.../conf.d/
def reddit():
	connected = connect()
	if connected == True:
		apiFolder()
		setColor = ran_color()
		reddit = str(redditSettings())
		fontSet = fontSettings()
		os.system("sudo ./scrolling-text-example --led-cols=64 -s 5 -y 8 -l 1 -f " + fontSet + " -C " + setColor + reddit)


#Pick random lyrics
def lyrics():
	apiFolder()
	setColor = ran_color()
	lyric = str(lyricSettings())
	fontSet = fontSettings()
	os.system("sudo ./scrolling-text-example --led-cols=64 -s 5 -y 8 -l 1 -f " + fontSet + " -C " + setColor + lyric)

#runs and kills a subprocess after timeout so that it doesnt run forever
def playImage():
	image = images()
	#ranImgScroll = ['normal', 'forward','backward']
	ranImgScroll = ['normal']
	ranImgScrollChoice = random.choice(ranImgScroll)
	try:
		if ranImgScrollChoice == 'normal':
			utilFolder()
			img = "sudo ./led-image-viewer --led-cols=64 " + image
			proc = subprocess.run(img, timeout=10, shell=True)
		#PPM FILES ONLY not PNG
		#elif ranImgScrollChoice == 'forward':
		#	apiFolder()
		#	img = "sudo ./demo -D 1 " + image + " --led-cols=64 "
		#	proc = subprocess.run(img, timeout=5, shell=True)
		#elif ranImgScrollChoice == 'backward':
		#	apiFolder()
		#	img = "sudo ./demo -D 2 " + image + " --led-cols=64 "
		#	proc = subprocess.run(img, timeout=5, shell=True)
		else:
			img = "sudo ./led-image-viewer --led-cols=64 " + image
			proc = subprocess.run(img, timeout=5, shell=True)
	except subprocess.TimeoutExpired:
		pgid = os.getpgid(os.getpid())
		if pgid == 1:
			os.kill(os.getpid(), signal.CTRL_C_EVENT)
			randomize(cycleLimit, btcLimit)
		else:
			os.killpg(os.getpgid(os.getpid()), signal.SIGINT)
			randomize(cycleLimit, btcLimit)
	finally:
		return None

#Select which demo and settings to run
def demo():
	apiFolder()
	demos = ['0','4','6','7','8','9','10','11']
	chosen = random.choice(demos)
	cmd = "sudo ./demo -D " + chosen + " --led-cols=64 "
	try:
		if chosen == '0':
			proc = subprocess.run(cmd, timeout=60, shell=True)
		elif chosen == '4':
			cmd = cmd + "--led-brightness=50 "
			proc = subprocess.run(cmd, timeout=20, shell=True)
		elif chosen == '6':
			cmd = cmd + "--led-brightness=70 "
			proc = subprocess.run(cmd, timeout=180, shell=True)
		elif chosen == "7":
			cmd = cmd + "--led-brightness=70 -m 500 "
			proc = subprocess.run(cmd, timeout=150, shell=True)
		elif chosen == "8":
			cmd = cmd + "--led-brightness=70 "
			proc = subprocess.run(cmd, timeout=120, shell=True)
		elif chosen == "9":
			cmd = cmd + "--led-brightness=70 "
			proc = subprocess.run(cmd, timeout=15, shell=True)
		elif chosen == "10":
			cmd = cmd + "--led-brightness=70 -m 250 "
			proc = subprocess.run(cmd, timeout=10, shell=True)
		elif chosen == "11":
			proc = subprocess.run(cmd, timeout=10, shell=True)
		else:
			proc = subprocess.run(cmd, timeout=10, shell=True)
	except subprocess.TimeoutExpired:
		pgid = os.getpgid(os.getpid())
		if pgid == 1:
			os.kill(os.getpid(), signal.CTRL_C_EVENT)
			randomize(cycleLimit, btcLimit)
		else:
			os.killpg(os.getpgid(os.getpid()), signal.SIGINT)
			randomize(cycleLimit, btcLimit)
	finally:
		return None

def playMovie():
	movie = movieSettings()
	utilFolder()
	cmd = "sudo ./video-viewer --led-cols=64 -V15 -f " + movie
	try:
		proc = subprocess.run(cmd, timeout=45, shell=True)
	except subprocess.TimeoutExpired:
		pgid = os.getpgid(os.getpid())
		if pgid == 1:
			os.kill(os.getpid(), signal.CTRL_C_EVENT)
			randomize(cycleLimit, btcLimit)
		else:
			os.killpg(os.getpgid(os.getpid()), signal.SIGINT)
			randomize(cycleLimit, btcLimit)
	finally:
		return None

def getPrice():
	price = str(cryptoSettings())
	setColor = ran_color()
	apiFolder()
	fontSet = fontSettings()
	cmd = "sudo ./scrolling-text-example --led-cols=64 -s 12 -y 8 -l 2 -f " + fontSet + " -C " + setColor + price
	try:
		proc = subprocess.run(cmd, timeout=15, shell=True)
	except subprocess.TimeoutExpired:
		pgid = os.getpgid(os.getpid())
		if pgid == 1:
			os.kill(os.getpid(), signal.CTRL_C_EVENT)
			randomize(cycleLimit, btcLimit)
		else:
			os.killpg(os.getpgid(os.getpid()), signal.SIGINT)
			randomize(cycleLimit, btcLimit)
	finally:
		return None


def displayTime():
	connected = connect()
	if connected == True:
		setColor = ran_color()
		setColor2 = ran_color()
		while setColor == setColor2:
			setColor2 = ran_color()
		if setColor == "255,255,0 " and setColor2 == "255,255,255 ":
			setColor = ran_color()
			setColor2 = ran_color()
		if setColor == "255,255,255 " and setColor2 == "255,255,0 ":
			setColor = ran_color()
			setColor2 = ran_color()
		if setColor == "255,255,0 " and setColor2 == "255,128,0 ":
			setColor = ran_color()
			setColor2 = ran_color()
		if setColor == "255,128,0 " and setColor2 == "255,255,0 ":
			setColor = ran_color()
			setColor2 = ran_color()
		apiFolder()
		cmd = "sudo ./clock --led-cols=64 -f ../fonts/6x12.bdf -x 8 -d %I:%M:%S -d %A -O " + setColor + " -C " + setColor2
		try:
			proc = subprocess.run(cmd, timeout=15, shell=True)
		except subprocess.TimeoutExpired:
			pgid = os.getpgid(os.getpid())
			if pgid == 1:
				os.kill(os.getpid(), signal.CTRL_C_EVENT)
				randomize(cycleLimit, btcLimit)
			else:
				os.killpg(os.getpgid(os.getpid()), signal.SIGINT)
				randomize(cycleLimit, btcLimit)
		finally:
			return None
	else:
		fontSet = fontSettings()
		setColor = ran_color()
		os.system("sudo ./scrolling-text-example --led-cols=64 -s 11 -y 8 -l 1 -f " + fontSet + " -C " + setColor + "Disconnected from the internet.")


def playRPlace():
	cmd = "sudo /home/pi/rplace.py"
	os.system(cmd)

#ToDO
#movieQuotes
#def news()
#def customMovies()/Animations

def randomize(cycleLimit, btcLimit):
	# DONT DELETE BELOW LINE cmd Pick which types of media will run. Used to isolate and troubleshoot.
	#cmd = ['displayTime()']
	cmd = ['playRPlace()', 'reddit()', 'demo()', 'playImage()', 'quotes()', 'lyrics()', 'getPrice()', 'playMovie()', 'displayTime()']
	# this is a count loop to restrict how many times the API was called to avoid banning. I was originally using
	# crontab to control the whole program but have since moved on to supervisor. 
	# With the supervisor configuration controlling when the prices are checked, the below code can be removed
	# and rewritten or left to help control how many times the price is shown in the rotation.
	if cycleLimit > 0:
		choice = random.choice(cmd)
		cycleLimit -= 1
		if choice == 'getPrice()':
			if btcLimit <= 5:
				eval(choice)
				btcLimit += 1
				randomize(cycleLimit, btcLimit)
			else:
				randomize(cycleLimit, btcLimit)
		else:
			eval(choice)
			randomize(cycleLimit, btcLimit)
	else:
		cycleLimit = 30
		btcLimit = 0
		randomize(cycleLimit, btcLimit)

#Main program should run always, on boot.
def main():
	try:
		while True:
			#values for crypto
			cycleLimit = 30
			btcLimit = 0
			randomize(cycleLimit, btcLimit)
	except:
		randomize(cycleLimit, btcLimit)
		#sys.exit()
		main()

if __name__ == "__main__":
	main()
