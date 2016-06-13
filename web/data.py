# Brian Mann
# data.py
# 6/6/2016

import cherrypy, requests
import re, json
import webbrowser, urllib2, time, datetime, tweepy
from bs4 import BeautifulSoup

class FoursquareController(object):
	def __init__(self):
		pass

	def POST(self):
		output = {'result':'success'}
		try:
			# grab the parameters sent by the web page
			params = cherrypy.request.body.read()
			# put the data into a string
			data = json.loads(params)
			# run the foursquare data crawl
			result = datacrawl(data)
			# check if foursquare data crawl failed
			if result == "Error":
				output['result'] = 'error'
				output['message'] = "Could not process request"
			else:
				output = result
				output['result'] = 'success'
		except Exception as ex:
			# send any exceptions to the web page
			output['result'] = 'error'
			output['message'] = str(ex)
		return json.dumps(output, encoding='latin-1')

class TwitterController(object):
	def __init__(self):
		pass

	def POST(self):
		output = {'result':'success'}
		try:
			# read the list of urls
			params = cherrypy.request.body.read()
			# convert it to a string
			data = json.loads(params)
			# run the twitter data crawl
			result = twitterCrawl(data)
			output = result
			output['result'] = 'success'
		except Exception as ex:
			# send any exceptions to the web page
			output['result'] = 'error'
			output['message'] = str(ex)
		return json.dumps(output, encoding='latin-1')

class InstagramController(object):
	def __init__(self):
		pass

	def POST(self):
		output = {'result':'success'}
		try:
			# read the list of urls
			params = cherrypy.request.body.read()
			# convert it to a string
			data = json.loads(params)
			# run the twitter data crawl
			result = instaCrawl(data)
			output = result
			output['result'] = 'success'
		except Exception as ex:
			# send any exceptions to the web page
			output['result'] = 'error'
			output['message'] = str(ex)
		return json.dumps(output, encoding='latin-1')

def datacrawl(data):
	# keys needed for access to url
	f = open('keys.txt', 'r')

	for line in f:
		line = line.rstrip()
		components = line.split("::")
		if components[0] == 'fClient_ID':
			fCLIENT_ID = str(components[1])
		elif components[0] == 'fClient_Secret':
			fCLIENT_SECRET = str(components[1])
		elif components[0] == 'gAPI':
			api = str(components[1])
		elif components[0] == 'tConsumer_Key':
			consumer_key = str(components[1])
		elif components[0] == 'tConsumer_Secret':
			consumer_secret = str(components[1])
		elif components[0] == 'tAccess_Token':
			access_token = str(components[1])
		elif components[0] == 'tAccess_Token_Secret':
			access_token_secret = str(components[1])

	# use current date to obtain version detail
	V_CODE = datetime.date.today().strftime("%Y%m%d")

	# custom search parameters
	location = data['location']
	srange = data['range']
	query = data['query']
	limit = data['limit']

	# setup the url
	if query != '':
		thisurl = "https://api.foursquare.com/v2/venues/explore?client_id="+fCLIENT_ID+"&client_secret="+fCLIENT_SECRET+"&v="+V_CODE+"&near="+location+"&query="+query+"&radius="+srange+"&limit="+limit
	else:
		thisurl = "https://api.foursquare.com/v2/venues/explore?client_id="+fCLIENT_ID+"&client_secret="+fCLIENT_SECRET+"&v="+V_CODE+"&near="+location+"&section=topPicks&radius="+srange+"&limit="+limit
	# ping the foursquare api
	r = requests.get(thisurl)

	# store the json
	thedata = r.json()

	# get the values for the markers
	if r.status_code == 200:
		#use current time to name the file
		result = makeHTML(thedata)
	else:
		result = "Error"
	return result

def makeHTML(mydict):
	result = {}
	# obtain center of search
	lat = mydict['response']['geocode']['center']['lat']
	lng = mydict['response']['geocode']['center']['lng']
	# obtain list of venues
	lst = mydict['response']['groups'][0]['items']
	markers = []
	names = []
	addresses = []
	ratings = []
	urls = []
	phones = []
	here = []
	tips = []
	# loop through each venue
	for i in lst:
		# obtain geolocation of venue
		tempgeo = {}
		tempgeo['lat'] = i['venue']['location']['lat']
		tempgeo['lng'] = i['venue']['location']['lng']
		# obtain name of venue
		names.append(i['venue']['name'])
		# obtain address of venue
		addresses.append(i['venue']['location']['formattedAddress'])
		# obtain phone number of venue
		try:
			phones.append(i['venue']['contact']['formattedPhone'])
		except:
			phones.append("N/A")
		# obtain rating of venue
		try:
			ratings.append(i['venue']['rating'])
		except:
			ratings.append("N/A")
		# obtain url of venue
		try:
			urls.append(i['venue']['url'])
		except:
			urls.append("N/A")
		here.append(i['venue']['hereNow']['count'])
		try:
			tips.append(i['tips'][0]['text'])
		except:
			tips.append("N/A")
		markers.append(tempgeo)

	# setup return structure
	result['lat'] = lat
	result['lng'] = lng
	result['markers'] = markers
	result['names'] = names
	result['addresses'] = addresses
	result['phones'] = phones
	result['ratings'] = ratings
	result['urls'] = urls
	result['here'] = here
	result['tips'] = tips
	return result

def twitterCrawl(data):

	#localtime = time.asctime(time.localtime(time.time()))
	#print localtime
	# keys needed for access to url
	f = open('keys.txt', 'r')

	for line in f:
		line = line.rstrip()
		components = line.split("::")
		if components[0] == 'fClient_ID':
			fCLIENT_ID = str(components[1])
		elif components[0] == 'fClient_Secret':
			fCLIENT_SECRET = str(components[1])
		elif components[0] == 'gAPI':
			api = str(components[1])
		elif components[0] == 'tConsumer_Key':
			consumer_key = str(components[1])
		elif components[0] == 'tConsumer_Secret':
			consumer_secret = str(components[1])
		elif components[0] == 'tAccess_Token':
			access_token = str(components[1])
		elif components[0] == 'tAccess_Token_Secret':
			access_token_secret = str(components[1])

	# standard tweepy steps
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)
	# prepare list of urls
	lst = data['urls']
	result = {}
	screennames = []
	descriptions = []
	followers = []
	tweets = []

	# loop through each url and attempt to do a get request
	for i in lst:
		utweets = []
		try:
			checked = False
			# simply skip any urls that are not provided
			if i == 'N/A':
				screennames.append('N/A')
				descriptions.append('N/A')
				followers.append('N/A')
			# the following are all bad urls
			elif '7-eleven' in i:
				screennames.append('N/A')
				descriptions.append('N/A')
				followers.append('N/A')
			elif 'brunospizza' in i:
				screennames.append('N/A')
				descriptions.append('N/A')
				followers.append('N/A')
			elif 'suxinghouse' in i:
				screennames.append('N/A')
				descriptions.append('N/A')
				followers.append('N/A')
			# good urls
			else:
				response = requests.get(i)
				# parse html
				page = BeautifulSoup(response.content, "html.parser")
				# loop through all of the links on a page
				for link in page.find_all('a'):
					# if a twitter link
					if 'twitter' in link.get('href'):
						url = link.get('href')
						# break down the string to grab the screenname
						line = url.rstrip()
						components = line.split("/")
						userid = components[-1]
						# found on one example that the screenname had garbage characters after it starting with a '?'
						if '?' in userid:
							components = userid.split("?")
						user = api.get_user(userid)
						statuses = api.user_timeline(screen_name = userid, count = 10)
						screennames.append(user.screen_name)
						descriptions.append(user.description)
						followers.append(user.followers_count)
						for tweet in statuses:
							utweets.append(tweet.text)
						tweets.append(utweets)
						checked = True
						break
				if checked == False:
					screennames.append('N/A')
					descriptions.append('N/A')
					followers.append('N/A')
					tweets.append(utweets)
		except Exception as ex:
			screennames.append('N/A')
			descriptions.append('N/A')
			followers.append('N/A')
			tweets.append(utweets)
	result['screennames'] = screennames
	result['descriptions'] = descriptions
	result['followers'] = followers
	result['tweets'] = tweets
	return result

def instaCrawl(data):

	#localtime = time.asctime(time.localtime(time.time()))
	#print localtime
	# keys needed for access to url
	f = open('keys.txt', 'r')

	for line in f:
		line = line.rstrip()
		components = line.split("::")
		if components[0] == 'fClient_ID':
			fCLIENT_ID = str(components[1])
		elif components[0] == 'fClient_Secret':
			fCLIENT_SECRET = str(components[1])
		elif components[0] == 'gAPI':
			api = str(components[1])
		elif components[0] == 'tConsumer_Key':
			consumer_key = str(components[1])
		elif components[0] == 'tConsumer_Secret':
			consumer_secret = str(components[1])
		elif components[0] == 'tAccess_Token':
			access_token = str(components[1])
		elif components[0] == 'tAccess_Token_Secret':
			access_token_secret = str(components[1])

	# prepare list of urls
	lst = data['urls']
	result = {}

	# loop through each url and attempt to do a get request
	for i in lst:
		try:
			checked = False
			# simply skip any urls that are not provided
			if i == 'N/A':
				pass
			# the following are all bad urls
			elif '7-eleven' in i:
				pass
			elif 'brunospizza' in i:
				pass
			elif 'suxinghouse' in i:
				pass
			# good urls
			else:
				response = requests.get(i)
				# parse html
				page = BeautifulSoup(response.content, "html.parser")
				# loop through all of the links on a page
				for link in page.find_all('a'):
					# if an instagram link
					if 'instagram.com' in link.get('href'):
						url = link.get('href')
						print url
						# break down the string to grab the userid
						line = url.rstrip()
						components = line.split("/")
						username = components[-1]
						checked = True
						break
				if checked == False:
					pass
		except Exception as ex:
			pass
	return result
