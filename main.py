import requests
import time
import json
from unidecode import unidecode
from discord_hooks import Webhook
import sys
import subprocess
from flask import Flask, request, jsonify, render_template, redirect
import logging
import _thread
from datetime import datetime
import webbrowser

variantID = 7319611637818

#param | variantID | variant ID of item we want to generate hash for
#return | object | object containing checkouthash and first auth token
def getCheckoutHash(s, variantID):
	addHeaders = {
		"Accept":"application/json, text/plain, */*",
		"Accept-Encoding":"gzip, deflate, br",
		"Accept-Language":"en-US,en;q=0.9",
		"Content-Type":"application/json;charset=UTF-8",
		"Host":"yeezysupply.com",
		"Origin":"https://yeezysupply.com",
		"Referer":"https://yeezysupply.com/products/002/?back=%2Fcollections%2Fseason-4",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
	}
	addPayload = {
		"quantity":1,
		"id":variantID,
		"properties":{}
	}
	print(str(time.clock()) + ": Adding variant to cart")
	addRes = s.post("https://yeezysupply.com/cart/add.js", headers = addHeaders, json = addPayload)
	print(str(time.clock()) + ": Added to cart!")
	cookies = requests.utils.dict_from_cookiejar(addRes.cookies)
	cookieString = ""
	for cookie in list(cookies.keys()):
		cookieString += (cookie+"="+cookies[cookie]+"; ")
	if(addRes.status_code == 200):
		checkoutHeaders = {
			"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			"Accept-Language":"en-US,en;q=0.9",
			"Cookie": cookieString,
			"Content-Type":"application/x-www-form-urlencoded",
			"Host":"yeezysupply.com",
			"Origin":"https://yeezysupply.com",
			"Referer":"https://yeezysupply.com/cart",
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
		}
		checkoutData = {
			"updates[]":1,
			"checkout":"CHECK OUT",
			"note": ""
		}
		print(str(time.clock()) + ": Getting checkout hash")
		checkoutRes = s.post("https://yeezysupply.com/cart", headers = checkoutHeaders, data = checkoutData)
		print(str(time.clock()) + ": Finished getting checkout hash")
		checkoutHashCookie = checkoutRes.headers["Set-Cookie"]
		checkoutHash = checkoutHashCookie[checkoutHashCookie.find("path=/17655971/checkouts/") + 25:]
		checkoutHash = checkoutHash[:checkoutHash.find(";")]
		authToken = getAuthToken(checkoutRes.text)
		sitekey = "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-" #getSitekey(checkoutRes.text)
		ret = {
			"checkoutHash": checkoutHash,
			"authToken": authToken,
			"cookieString": cookieString,
			"sitekey": sitekey
		}
		return ret

#Hardcoded variantID
def generateBlankCOLinks(goodVariant):
	s = requests.Session()
	addHeaders = {
		"Accept":"application/json, text/plain, */*",
		"Accept-Encoding":"gzip, deflate, br",
		"Accept-Language":"en-US,en;q=0.9",
		"Content-Type":"application/json;charset=UTF-8",
		"Host":"yeezysupply.com",
		"Origin":"https://yeezysupply.com",
		"Referer":"https://yeezysupply.com/products/002/?back=%2Fcollections%2Fseason-4",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
	}
	addPayload = {
		"quantity":1,
		"id":43714953555,
		"properties":{}
	}
	print(str(time.clock()) + ": Adding variant to cart")
	addRes = s.post("https://yeezysupply.com/cart/add.js", headers = addHeaders, json = addPayload)
	print(str(time.clock()) + ": Added to cart!")
	cookies = requests.utils.dict_from_cookiejar(addRes.cookies)
	cookieString = ""
	for cookie in list(cookies.keys()):
		cookieString += (cookie+"="+cookies[cookie]+"; ")
	if(addRes.status_code == 200):
		checkoutHeaders = {
			"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			"Accept-Language":"en-US,en;q=0.9",
			"Cookie": cookieString,
			"Content-Type":"application/x-www-form-urlencoded",
			"Host":"yeezysupply.com",
			"Origin":"https://yeezysupply.com",
			"Referer":"https://yeezysupply.com/cart",
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
		}
		checkoutData = {
			"updates[]":1,
			"checkout":"CHECK OUT",
			"note": ""
		}
		print(str(time.clock()) + ": Getting checkout hash")
		checkoutRes = s.post("https://yeezysupply.com/cart", headers = checkoutHeaders, data = checkoutData)
		cookies = requests.utils.dict_from_cookiejar(checkoutRes.cookies)
		for cookie in list(cookies.keys()):
			cookieString += (cookie+"="+cookies[cookie]+"; ")
		print(str(time.clock()) + ": Finished getting checkout hash")
		checkoutHashCookie = checkoutRes.headers["Set-Cookie"]
		checkoutHash = checkoutHashCookie[checkoutHashCookie.find("path=/17655971/checkouts/") + 25:]
		checkoutHash = checkoutHash[:checkoutHash.find(";")]
		checkoutHeaders = {
			"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			"Accept-Language":"en-US,en;q=0.9",
			"Cookie": cookieString,
			"Content-Type":"application/x-www-form-urlencoded",
			"Host":"yeezysupply.com",
			"Origin":"https://yeezysupply.com",
			"Referer":"https://yeezysupply.com/cart",
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
		}
		print(str(time.clock()) + ": Clearing cart")
		clearCartRes = s.get("https://yeezysupply.com/cart/change?line=1&quantity=0", headers = checkoutHeaders)
		print(str(time.clock()) + ": Finished clearing cart")
		cookies = requests.utils.dict_from_cookiejar(clearCartRes.cookies)
		for cookie in list(cookies.keys()):
			cookieString += (cookie+"="+cookies[cookie]+"; ")
		print("https://yeezysupply.com/17655971/checkouts/" + checkoutHash)
		s = open("blankhashes.json", "r")
		hashes = json.load(s)
		ret = {
			"checkoutHash": checkoutHash,
			"cookieString": cookieString
		}
		hashes.append(ret)
		with open('blankhashes.json', 'w') as outfile:
			json.dump(hashes, outfile)

		
def checkOut(s, authToken, cookieString, checkoutHash, ccProfileID, profileJSON):
	checkoutHeaders = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.9",
		"Host": "yeezysupply.com",
		"Referer": "https://yeezysupply.com/17655971/checkouts/"+checkoutHash,
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
	}
	shippingPayload = {
		"utf8": "✓",
		"_method": "patch",
		"authenticity_token": authToken,
		"previous_step": "contact_information",
		"step": "shipping_method",
		"checkout[email]": profileJSON["email"],
		"checkout[buyer_accepts_marketing]": 0,
		"checkout[buyer_accepts_marketing]": 1,
		"checkout[shipping_address][first_name]": "",
		"checkout[shipping_address][last_name]": "",
		"checkout[shipping_address][address1]": "",
		"checkout[shipping_address][address2]": "",
		"checkout[shipping_address][city]": "",
		"checkout[shipping_address][country]": "",
		"checkout[shipping_address][province]": "",
		"checkout[shipping_address][zip]": "",
		"checkout[shipping_address][phone]": "",
		"checkout[shipping_address][first_name]": profileJSON["firstName"],
		"checkout[shipping_address][last_name]": profileJSON["lastName"],
		"checkout[shipping_address][address1]": profileJSON["address"],
		"checkout[shipping_address][address2]": profileJSON["address2"],
		"checkout[shipping_address][city]": profileJSON["city"],
		"checkout[shipping_address][country]": profileJSON["country"],
		"checkout[shipping_address][province]": profileJSON["state"],
		"checkout[shipping_address][zip]": profileJSON["zip"],
		"checkout[shipping_address][phone]": profileJSON["phone"],
		"checkout[remember_me]": "",
		"checkout[remember_me]": 0,
		"button": "",
		"checkout[client_details][browser_width]": 1920,
		"checkout[client_details][browser_height]": 949,
		"checkout[client_details][javascript_enabled]": 1
	}

	shippingHeaders = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.9",
		"Content-Type": "application/x-www-form-urlencoded",
		"Cookie": cookieString,
		"Host": "yeezysupply.com",
		"Origin": "https://yeezysupply.com",
		"Referer": "https://yeezysupply.com/17655971/checkouts/" + checkoutHash,
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
	}
	print("Cookie string 1 :" + cookieString)
	print(str(time.clock()) + ": Setting shipping information")
	shippingRes = s.post("https://yeezysupply.com/17655971/checkouts/" + checkoutHash, headers = shippingHeaders, data = shippingPayload)
	print(str(time.clock()) + ": Shipping information submitted")
	authToken2 = getAuthToken(shippingRes.text)
	cookies = requests.utils.dict_from_cookiejar(shippingRes.cookies)
	for cookie in list(cookies.keys()):
		cookieString += (cookie+"="+cookies[cookie]+"; ")

	shippingMethodHeaders = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.9",
		"Content-Type": "application/x-www-form-urlencoded",
		"Cookie": cookieString,
		"Host": "yeezysupply.com",
		"Origin": "https://yeezysupply.com",
		"Referer": "https://yeezysupply.com/17655971/checkouts/" + checkoutHash,
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
	}
	shippingMethodPayload = {
		"utf8": "✓",
		"_method": "patch",
		"authenticity_token": authToken2,
		"previous_step": "shipping_method",
		"step": "payment_method",
		"checkout[shipping_rate][id]": "shopify-STANDARD%20GROUND%20SHIPPING-20.00",
		"button": "",
		"checkout[client_details][browser_width]": 1920,
		"checkout[client_details][browser_height]": 949,
		"checkout[client_details][javascript_enabled]": 1
	}
	print(str(time.clock()) + ": Setting shipping method to default")
	print("Cookie string 2 :" + cookieString)
	shippingMethodRes = s.post("https://yeezysupply.com/17655971/checkouts/" + checkoutHash, headers = shippingMethodHeaders, data = shippingMethodPayload)
	print(str(time.clock()) + ": Shipping method successfully set!")
	authToken3 = getAuthToken(shippingMethodRes.text)
	cookies = requests.utils.dict_from_cookiejar(shippingMethodRes.cookies)
	for cookie in list(cookies.keys()):
		cookieString += (cookie+"="+cookies[cookie]+"; ")

	completeOrderHeaders = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.9",
		"Content-Type": "application/x-www-form-urlencoded",
		"Cookie": cookieString,
		"Host": "yeezysupply.com",
		"Origin": "https://yeezysupply.com",
		"Referer": "https://yeezysupply.com/17655971/checkouts/" + checkoutHash +"?previous_step=shipping_method&step=payment_method",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
	}

	completeOrderPayload = {
		"utf8": "✓",
		"_method": "patch",
		"authenticity_token": authToken3,
		"previous_step": "payment_method",
		"step": "",
		"s": ccProfileID,
		"checkout[payment_gateway]": 117647559,
		"checkout[credit_card][vault]": "false",
		"checkout[different_billing_address]": "false",
		"checkout[total_price]": 67000,
		"complete": 1,
		"checkout[client_details][browser_width]": 1920,
		"checkout[client_details][browser_height]": 949,
		"checkout[client_details][javascript_enabled]": 1
	}
	print(str(time.clock()) + ": Submitting order")
	completeOrderRes = s.post("https://yeezysupply.com/17655971/checkouts/" + checkoutHash, headers = completeOrderHeaders, data = completeOrderPayload)
	print(str(time.clock()) + ": Order submitted")
	return (time.clock())

def generateProfileJSON(profileName):
	with open("./profiles/" + profileName + ".json") as profile:
		profileJSON = json.load(profile)
		return profileJSON

def getAuthToken(htmltext):
	findAuthToken = unidecode(htmltext)
	findAuthToken = findAuthToken[findAuthToken.index('"authenticity_token"') + 20:]
	findAuthToken = findAuthToken[findAuthToken.index('"authenticity_token"') + 20:]
	findAuthToken = findAuthToken[findAuthToken.index('"authenticity_token"') + 20:]
	authToken = findAuthToken[8:findAuthToken.index('" />')]
	return authToken

##UNUSED##
def getATCCookies(s, variantID):
	addHeaders = {
		"Accept":"application/json, text/plain, */*",
		"Accept-Encoding":"gzip, deflate, br",
		"Accept-Language":"en-US,en;q=0.9",
		"Content-Type":"application/json;charset=UTF-8",
		"Host":"yeezysupply.com",
		"Origin":"https://yeezysupply.com",
		"Referer":"https://yeezysupply.com/products/002/?back=%2Fcollections%2Fseason-4",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
	}
	addPayload = {
		"quantity":1,
		"id":variantID,
		"properties":{}
	}
	print(str(time.clock()) + ": Started getting ATC cookies")
	addRes = s.post("https://yeezysupply.com/cart/add.js", headers = addHeaders, json = addPayload)
	print(str(time.clock()) + ": Finished getting ATC cookies")
	cookies = requests.utils.dict_from_cookiejar(addRes.cookies)
	cookieString = ""
	for cookie in list(cookies.keys()):
		cookieString += (cookie+"="+cookies[cookie]+"; ")
	return cookieString

def generateCheckoutProfile(profileJSON, checkoutHash):
	ccHeaders = {
		"Accept": "application/json",
		"Accept-Language": "en-US,en;q=0.9",
		"Content-Type": "application/json",
		"Host": "elb.deposit.shopifycs.com",
		"Origin": "https://checkout.shopifycs.com",
		"Referer": "https://checkout.shopifycs.com/number?identifier=" + checkoutHash + "&location=https%3A%2F%2Fyeezysupply.com%2F17655971%2Fcheckouts%2F" + checkoutHash + "%3Fprevious_step%3Dshipping_method%26step%3Dpayment_method",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
	}

	ccPayload = {
		"credit_card":{
			"number":profileJSON["ccNumber"],
			"name":profileJSON["firstName"] + " " + profileJSON["lastName"],
			"month":profileJSON["ccMonth"],
			"year":profileJSON["ccYear"],
			"verification_value":profileJSON["ccVerification"]
		}
	}

	print(str(time.clock()) + ": Generating checkout profile")
	ccRes = requests.post("https://elb.deposit.shopifycs.com/sessions", headers = ccHeaders, json = ccPayload)
	print(str(time.clock()) + ": Finished generating checkout profile")
	ccProfileJSON = json.loads(ccRes.text)
	ccProfileID = ccProfileJSON["id"]
	print(ccProfileID)
	return ccProfileID

def sendWebhook(checkoutUrl, totaltime, method, productName, pictureurl, webhook):
	embed = Webhook(webhook, color=123123)
	embed.set_author(name='Checkout/Queue Bypass Link', url = checkoutUrl)
	embed.add_field(name='Product Name',value=productName)
	embed.add_field(name='Total Time', value=totaltime)
	embed.add_field(name='Created by', value="rycao18#3998")
	embed.add_field(name='Method', value=method)
	embed.set_thumbnail(pictureurl)
	embed.set_footer(text='RyZySply Bot - '+str(time.strftime("%H:%M:%S")),icon='https://i.imgur.com/fG3Gu2Y.jpg',ts=True)
	embed.post()

def getProductInfo(url):
	r = requests.get(url)
	rtext = r.text[r.text.index('featured_image') + 17:]
	rtext = rtext[:rtext.index(',') - 1]
	rtext = rtext.replace("\/", "/")
	rtext2 = r.text[r.text.index('PI__title js-unorphan') + 39:]
	rtext2 = rtext2[:rtext2.index('</div>')]
	print(rtext2)
	ret = {
		"picUrl": "https:" + rtext,
		"productName": rtext2
	}
	return ret

def getProductInfoFromCheckoutLink(checkoutLink):
	r = requests.get(checkoutLink)
	rtext = r.text[r.text.index('product__description__name order-summary__emphasis'):]
	print(rtext)

def getSitekey(html):
	sitekey1 = html[html.index('data-sitekey="') + 14:]
	sitekey = sitekey1[:sitekey1.index('"')]
	w = open("sitekey.txt", "w")
	w.write(sitekey)
	w.close()

tokens = eval(open("tokens.txt", "r").read())

def manageTokens():
	while True:
		for token in tokens:
			if token['expiry'] < datetime.now().timestamp():
				tokens.remove(token)
				print("Token expired and deleted.")
		time.sleep(5)

def startHarvester():
	app = Flask(__name__)

	@app.route('/')
	def home():
		return render_template('index.html', sitekey=config['sitekey'], domain=config['domain'])

	@app.route('/submit', methods=['POST'])
	def submit():
		token = request.form['g-recaptcha-response']
		expiry = datetime.now().timestamp() + 115
		tokenDict = {
			'token': token,
			'expiry': expiry
		}
		tokens.append(tokenDict)
		w = open("tokens.txt", "w")
		w.write(str(tokens))
		w.close()
		print("Token harvested and stored.")
		return redirect('/')

	@app.route('/count')
	def count():
		count = len(tokens)
		return jsonify(count=count)

	@app.route('/token')
	def fetch_token():
		try:
			token = tokens.pop(0)
			print("Token requested and returned to user.")
			return token['token']
		except:
			print("Token requested but none available.")
			return "ERROR"

	_thread.start_new_thread(manageTokens, ())
	with open('config.json') as file:
		config = json.load(file)
		file.close()
	print("Server running at ryzysply.{}:5000".format(config['domain']))
	webbrowser.open('http://ryzysply.{}:5000/'.format(config['domain']))
	app.run()



##########RUNNING STUFF##########


generateBlankCOLinks(43714670675)
_thread.start_new_thread(startHarvester, ())
# param | productURL | string of the url of the product
# param | sizeIndex | index of the array that the size is
# param | profile | string of the name of the profile that we checkout with
# param | discord | boolean of whether or not to post to discord
def completelyNewCheckout(productURL, sizeIndex, profile, discord, discordwebhook):
	s = requests.session()
	variantIDs = getVariants(productURL)
	selectedVariant = variantIDs[sizeIndex]
	checkoutHashOBJ = getCheckoutHash(s, selectedVariant)
	checkoutHash = checkoutHashOBJ["checkoutHash"]
	authToken = checkoutHashOBJ["authToken"]
	cookieString = checkoutHashOBJ["cookieString"]
	sitekey = checkoutHashOBJ["sitekey"]
	#captchaToken = getToken(sitekey)
	#print("TOKEN : " + captchaToken)
	profileJSON = generateProfileJSON(profile)
	ccProfileID = generateCheckoutProfile(profileJSON, checkoutHash)
	stopTime = checkOut(s, authToken, cookieString, checkoutHash, ccProfileID, profileJSON)
	if discord:
		productOBJ = getProductInfo(productURL)
		sendWebhook("https://yeezysupply.com/17655971/checkouts/" + checkoutHash, str(stopTime)[:7] + " seconds", "Full Checkout", productOBJ["productName"], productOBJ["picUrl"], discordwebhook)

productURL = "https://yeezysupply.com/products/sherpa-lined-hooded-coaches-coat-bat/?back=%2Fcollections%2Fseason-4"
#completelyNewCheckout(productURL, 0, "profile", True, "https://discordapp.com/api/webhooks/430085575010156544/6C5IxlbGY4HC-235eg83tUmJo3Ow3xscGa5wGGq7vnp3uIWoJoFZ4qJMdgue16gpZ3s1")

def checkoutWithProfileID(productURL, sizeIndex, ccProfileID, profile, discord, discordwebhook):
	startTime = time.clock()
	s = requests.session()
	variantIDs = getVariants(productURL)
	selectedVariant = variantIDs[sizeIndex]
	checkoutHashOBJ = getCheckoutHash(s, selectedVariant)
	checkoutHash = checkoutHashOBJ["checkoutHash"]
	authToken = checkoutHashOBJ["authToken"]
	cookieString = checkoutHashOBJ["cookieString"]
	sitekey = checkoutHashOBJ["sitekey"]
	profileJSON = generateProfileJSON(profile)
	stopTime = checkOut(s, authToken, cookieString, checkoutHash, ccProfileID, profileJSON)
	if discord:
		productOBJ = getProductInfo(productURL)
		sendWebhook("https://yeezysupply.com/17655971/checkouts/" + checkoutHash, str(stopTime-startTime)[:7] + " seconds", "Checkout With Premade Profile", productOBJ["productName"], productOBJ["picUrl"], discordwebhook)

productURL = "https://yeezysupply.com/products/sherpa-lined-hooded-coaches-coat-bat/?back=%2Fcollections%2Fseason-4"
#checkoutWithProfileID(productURL, 0, "east-261e5ad2737cd283a9d5a758e8d9fd46", "profile", True, "https://discordapp.com/api/webhooks/430085575010156544/6C5IxlbGY4HC-235eg83tUmJo3Ow3xscGa5wGGq7vnp3uIWoJoFZ4qJMdgue16gpZ3s1")

def checkoutWithCheckoutLink(productURL, sizeIndex, checkoutLink, profile, discord, discordwebhook):
	startTime = time.clock()
	if "?" in checkoutLink:
		checkoutLink = checkoutLink[:checkoutLink.index("?")]
	if "stock_problems" in checkoutLink:
		checkoutLink = checkoutLink[:checkoutLink.index("/stock_problems")]
	s = requests.session()
	s.get(checkoutLink+"?no_cookies_from_redirect=1")
	r = s.get(checkoutLink+"?cookies_blocked=1&no_cookies_from_redirect=1")
	checkoutHashCookie = r.headers["Set-Cookie"]
	checkoutHash = checkoutHashCookie[checkoutHashCookie.find("path=/17655971/checkouts/") + 25:]
	checkoutHash = checkoutHash[:checkoutHash.find(";")]
	cookieString = ""
	variantIDs = getVariants(productURL)
	selectedVariant = variantIDs[sizeIndex]
	authToken = getAuthToken(r.text)
	profileJSON = generateProfileJSON(profile)
	ccProfileID = generateCheckoutProfile(profileJSON, checkoutHash)
	stopTime = checkOut(s, authToken, cookieString, checkoutHash, ccProfileID, profileJSON)
	if discord:
		#productOBJ = getProductInfo(productURL)
		sendWebhook("https://yeezysupply.com/17655971/checkouts/" + checkoutHash, str(stopTime-startTime)[:7] + " seconds", "Checkout With Checkout Link", "Hi", "https://i.imgur.com/fG3Gu2Y.jpg", discordwebhook)

productURL = "https://yeezysupply.com/17655971/checkouts/8b32c815b54b2e7a64f13f01c38ae559"
#checkoutWithCheckoutLink("https://yeezysupply.com/products/002/?back=%2Fcollections%2Fseason-4", 0, productURL, "profile", True, "https://discordapp.com/api/webhooks/430085575010156544/6C5IxlbGY4HC-235eg83tUmJo3Ow3xscGa5wGGq7vnp3uIWoJoFZ4qJMdgue16gpZ3s1")


