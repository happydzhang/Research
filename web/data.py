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
			if result != 200:
				output['result'] = 'error'
				output['message'] = result
			else:

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
thisurl = "https://api.foursquare.com/v2/venues/explore?client_id="+CLIENT_ID+"&client_secret="+CLIENT_SECRET+"&v="+V_CODE+"&near="+location+"&section="+section+"&query="+query+"&radius="+srange+"&limit="+limit
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
        makeHTML(thedata)
else
	result = r.status_code
	return result

def makeHTML(mydict):
	# obtain center of search
	lat = mydict['response']['geocode']['center']['lat']
        lng = mydict['response']['geocode']['center']['lng']
	# obtain list of venues
        lst = mydict['response']['groups'][0]['items']
        markers = []
        names = []
        tempnames = []
        addresses = []
        tempaddresses = []
        ratings = []
        tempratings = []
        urls = []
        tempurls = []
        phones = []
        tempphones = []
	# loop through each venue
        for i in lst:
		# obtain geolocation of venue
                tempgeo = {}
                tempgeo['lat'] = i['venue']['location']['lat']
                tempgeo['lng'] = i['venue']['location']['lng']
		# obtain name of venue
                tempnames.append(i['venue']['name'])
		# obtain address of venue
                tempaddresses.append(i['venue']['location']['formattedAddress'])
		# obtain phone number of venue
                try:
                        tempphones.append(i['venue']['contact']['formattedPhone'])
                except:
                        tempphones.append("N/A")
		# obtain rating of venue
                try:
                        tempratings.append(i['venue']['rating'])
                except:
			tempratings.append("N/A")
		# obtain url of venue
                try:
                        tempurls.append(i['venue']['url'])
                except:
                        tempurls.append("N/A")
                markers.append(tempgeo)

	# clean up the data
	names = json.dumps(tempnames)
        addresses = json.dumps(tempaddresses)
        phones = json.dumps(tempphones)
        ratings = json.dumps(tempratings)
        urls = json.dumps(tempurls)
