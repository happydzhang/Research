# Brian Mann
# data.py
# 5/25/2016

import cherrypy, requests
import re, json
import webbrowser, urllib2, time, datetime, tweepy
from bs4 import BeautifulSoup

class DataController(object):
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
		result = makeHTML(thedata, consumer_key, consumer_secret, access_token, access_token_secret)
	else:
		result = "Error"
	return result

def makeHTML(mydict, ck, cs, at, ats):
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
	result['twitters'] = webCrawl(lst, ck, cs, at, ats)
	return result

def webCrawl(lst, ck, cs, at, ats):

	userids = []
	output = []
	placeholder = {}
	placeholder['screenname'] = 'N/A'
	placeholder['name'] = 'N/A'
	placeholder['location'] = 'N/A'
	placeholder['description'] = 'N/A'
	placeholder['followers'] = 'N/A'
	placeholder['friends'] = 'N/A'
	placeholder['statuses'] = 'N/A'
	placeholder['url'] = 'N/A'
	k = 0
	for i in lst:
		element = None
		checked = False
		try:
			response = requests.get(i['venue']['url'])
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
					for j in range(0, len(userids)):
						if userid == userids[j]:
							checked = True
					if not checked:
						element = getTwitter(userid, ck, cs, at, ats)
						userids.append(userid)
		except:
			pass
		if element != None:
			output.append(element)
		else:
			output.append(placeholder)
	return output

def getTwitter(userid, ck, cs, at, ats):

	output = {}
	tweets = []

	auth = tweepy.OAuthHandler(ck, cs)
	auth.set_access_token(at, ats)

	api = tweepy.API(auth)

	user = api.get_user(userid)
	output['screenname'] = user.screen_name
	output['name'] = user.name
	output['location'] = user.location
	output['description'] = user.description
	output['followers'] = str(user.followers_count)
	output['friends'] = str(user.friends_count)
	output['statuses'] = str(user.statuses_count)
	if (user.url == None):
		output['url'] = 'N/A'
	else:
		output['url'] = user.url

	tweet = api.user_timeline(user.screen_name)
	#for status in tweet:
	#	tweets.append(status.text)
	#output['tweets'] = tweets
	return output
