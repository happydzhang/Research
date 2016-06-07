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
			params = cherrypy.request.body.read()
			data = json.loads(params)
			result = datacrawl(data)
			if result == "Error":
				output['result'] = 'error'
				output['message'] = "Could not process request"
			else:
				output = result
				output['result'] = 'success'
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
		return json.dumps(output, encoding='latin-1')

class TwitterController(object):
	def __init__(self):
		pass

	def POST(self):
		output = {'result':'success'}
		try:
			params = cherrypy.request.body.read()
			data = json.loads(params)
			result = webCrawl(data)
			output = result
			output['result'] = 'success'
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
		return json.dumps(output, encoding='latin-1')

def datacrawl(data):
	# keys needed for access to url
	f = open('keys.txt', 'r')

	for line in f:
		line = line.rstrip()
		components = line.split("::")
		if components[0] == 'Client_ID':
			CLIENT_ID = str(components[1])
		elif components[0] == 'Client_Secret':
			CLIENT_SECRET = str(components[1])
		elif components[0] == 'API':
			api = str(components[1])
		elif components[0] == 'Consumer_Key':
			consumer_key = str(components[1])
		elif components[0] == 'Consumer_Secret':
			consumer_secret = str(components[1])
		elif components[0] == 'Access_Token':
			access_token = str(components[1])
		elif components[0] == 'Access_Token_Secret':
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
		thisurl = "https://api.foursquare.com/v2/venues/explore?client_id="+CLIENT_ID+"&client_secret="+CLIENT_SECRET+"&v="+V_CODE+"&near="+location+"&query="+query+"&radius="+srange+"&limit="+limit
	else:
		thisurl = "https://api.foursquare.com/v2/venues/explore?client_id="+CLIENT_ID+"&client_secret="+CLIENT_SECRET+"&v="+V_CODE+"&near="+location+"&section=topPicks&radius="+srange+"&limit="+limit
	r = requests.get(thisurl)

	# store the json
	thedata = r.json()

	# get the values for the markers
	if r.status_code == 200:
		#use current time to name the file
		#filename = datetime.datetime.now().strftime("%m%d%Y%H%M%S")
		#datafile = open("datasets/"+filename+".json", "w")
		#datafile.write(json.dumps(thedata, indent=4, sort_keys=True))
		#datafile.close()
		#print filename+".json created!"
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
	return result

def webCrawl(data):
	# keys needed for access to url
	f = open('keys.txt', 'r')

	for line in f:
		line = line.rstrip()
		components = line.split("::")
		if components[0] == 'Client_ID':
			CLIENT_ID = str(components[1])
		elif components[0] == 'Client_Secret':
			CLIENT_SECRET = str(components[1])
		elif components[0] == 'API':
			api = str(components[1])
		elif components[0] == 'Consumer_Key':
			consumer_key = str(components[1])
		elif components[0] == 'Consumer_Secret':
			consumer_secret = str(components[1])
		elif components[0] == 'Access_Token':
			access_token = str(components[1])
		elif components[0] == 'Access_Token_Secret':
			access_token_secret = str(components[1])

	lst = data['urls']
	userids = []
	result = {}
	for i in lst:
		try:
			checked = False
			if i == 'N/A':
				userids.append('N/A')
			else:
				response = requests.get(i)
				# parse html
				page = BeautifulSoup(response.content, "html.parser")
				for link in page.find_all('a'):
					if 'twitter' in link.get('href'):
						url = link.get('href')
						line = url.rstrip()
						components = line.split("/")
						userid = components[-1]
						if '?' in userid:
							components = userid.split("?")
							userid = components[0]
						if not checked:
							userids.append(userid)
							checked = True
				if not checked:
					userids.append('N/A')
		except Exception as ex:
			userids.append('N/A')
	result = getTwitter(userids, consumer_key, consumer_secret, access_token, access_token_secret)
	return result


def getTwitter(userids, ck, cs, at, ats):

	result = {}
	screennames = []
	descriptions = []
	followers = []

	auth = tweepy.OAuthHandler(ck, cs)
	auth.set_access_token(at, ats)

	api = tweepy.API(auth)

	for userid in userids:
		try:
			user = api.get_user(userid)
			screennames.append(user.screen_name)
			descriptions.append(user.description)
			followers.append(user.followers_count)
		except:
			screennames.append('N/A')
			descriptions.append('N/A')
			followers.append('N/A')
			
	result['screennames'] = screennames
	result['descriptions'] = descriptions
	result['followers'] = followers
	return result
