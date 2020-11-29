import requests
from bs4 import BeautifulSoup
import smtplib
import time
import numpy as np
import operator
import secrets

mediamarkt = '';
coolblue = '';
bol = '';
bestprice = float;
bestprices = {};
bestPriceS = [];
bestPriceP = [];

def Mediamarkt():
	global bestprices
	global mediamarkt
	url = 'https://www.mediamarkt.nl/nl/product/_logitech-mx-master-3-graphite-1636206.html'
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.11 Safari/537.36'}
	page = requests.get(url, headers = headers)
	soup = BeautifulSoup(page.content, 'html.parser')

	mediamarkt = soup.find('div', {'class': 'price'}).get_text()
	mediamarkt = float(mediamarkt.replace(",", "."))
	bestprices["Mediamarkt"] = mediamarkt

def Coolblue():
	global bestprices
	global coolblue
	url = 'https://www.coolblue.nl/product/838633/logitech-mx-master-3-draadloze-muis-zwart.html'
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.11 Safari/537.36'}
	page = requests.get(url, headers = headers)
	soup = BeautifulSoup(page.content, 'html.parser')

	coolblue = soup.find('span', {'class': 'sales-price js-sales-price'}).get_text()
	coolblue = float(coolblue.replace(",", "."))
	bestprices["Coolblue"] = coolblue

def Bol():
	global bestprices
	global bol
	url = 'https://www.bol.com/nl/p/logitech-mx-master-3-draadloze-muis-zwart/9200000118467975/?s2a=#productTitle'
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.11 Safari/537.36'}
	page = requests.get(url, headers = headers)
	soup = BeautifulSoup(page.content, 'html.parser')

	bol = soup.find('span', {'class': 'promo-price'}).get_text()

	decimalpart = bol[-3:]	
	intpart = bol[0:3]
	decimalpart = int(decimalpart)
	intpart = int(intpart)
	bol = "%s,%s" % (intpart,decimalpart)
	bol = float(bol.replace(",", "."))
	bestprices["Bol"] = bol

def Prices():
	Mediamarkt()
	Coolblue()
	Bol()

def BestPrice():
	global bestPriceS
	global bestPriceP
	global bestprices
	pricesSorted = sorted(bestprices.items(), key=operator.itemgetter(1))
	bestPrice = pricesSorted[0]
	bestPriceS = bestPrice[0]
	bestPriceP = bestPrice[1]

def AllPrices():
	global bestprices
	print(bestprices)

def SendMail():
	global bestPriceS
	global bestPriceP
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()

	server.login(secrets.sender, secrets.password)

	subject = f"Beste prijs is {bestPriceP} bij {bestPriceS}"
	body = f"""
	Mediamarkt: {mediamarkt}
	https://www.mediamarkt.nl/nl/product/_logitech-mx-master-3-graphite-1636206.html

	Coolblue: {coolblue}
	https://www.coolblue.nl/product/838633/logitech-mx-master-3-draadloze-muis-zwart.html

	Bol: {bol}
	https://www.bol.com/nl/p/logitech-mx-master-3-draadloze-muis-zwart/9200000118467975/?s2a=#productTitle
	"""
	msg = f"Subject: {subject}\n\n{body}"

	server.sendmail(
		secrets.sender,
		secrets.receiver,
		msg
	)

	print('send')
	server.quit()

def interval():
	Prices()
	BestPrice()
	# SendMail()
	AllPrices()
	print(f'Ff wachten pik, nog {time_wait} minuten')

def threshold():
	priceWanted = 90
	Prices()
	BestPrice()
	while bestPriceP <= priceWanted:
		print(f'Check op prijs onder {priceWanted}')
		print(f'Er is er één onder {priceWanted}!!!')
		SendMail()
	else:
		print(f'Geen prijs gevonden onder {priceWanted}')
		print(f'Probeer het weer over {time_wait} minuten.')


if __name__ == '__main__':
	while True:
		time_wait = 60
		interval()
		time.sleep(time_wait * 60)

