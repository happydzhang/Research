# Brian Mann
# data.py
# 5/25/2016

import cherrypy, requests
import re, json
import webbrowser, urllib2, time, datetime

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

	CLIENT_ID = f.readline()
	CLIENT_SECRET = f.readline()
	# use current date to obtain version detail
	V_CODE = datetime.date.today().strftime("%Y%m%d")

	# custom search parameters
	location = data['location']
	srange = data['range']
	section = data['section']
	query = data['query']
	limit = data['limit']

	# setup the url
	if section != 'None':
		thisurl = "https://api.foursquare.com/v2/venues/explore?client_id="+CLIENT_ID+"&client_secret="+CLIENT_SECRET+"&v="+V_CODE+"&near="+location+"&section="+section+"&radius="+srange+"&limit="+limit
	elif query != '':
		thisurl = "https://api.foursquare.com/v2/venues/explore?client_id="+CLIENT_ID+"&client_secret="+CLIENT_SECRET+"&v="+V_CODE+"&near="+location+"&query="+query+"&radius="+srange+"&limit="+limit
		
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
