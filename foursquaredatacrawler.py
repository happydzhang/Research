#!/usr/local/python

# Brian Mann
# 6/1/2016

import webbrowser, urllib2, time, datetime, json, requests, tweepy
from bs4 import BeautifulSoup

class MyStreamListener(tweepy.StreamListener):

	def __init__(self, mydict, search, api=None):
		super(MyStreamListener, self).__init__()
		self.mydict = mydict
		self.search = search
		self.lst = mydict['response']['groups'][0]['items']
		self.numtweets = 0
		self.maxtweets = 25

	def on_status(self, status):
		self.numtweets += 1
		for i in self.lst:
			if i['venue']['name'].lower() in status.text.lower():
				print "Tweet #" + str(self.numtweets) + ": " + status.text
				break
			elif i['venue']['categories'][0]['shortName'].lower() in status.text.lower():
				print "Tweet #" + str(self.numtweets) + ": " + status.text
				break
			elif i['venue']['location']['city'].lower() in status.text.lower():	
				print "Tweet #" + str(self.numtweets) + ": " + status.text
				break
			elif self.search in status.text.lower():
				print "Tweet #" + str(self.numtweets) + ": " + status.text
				break
		if self.numtweets == self.maxtweets:
			return False
		return True

	def on_error(self, status_code):
		print 'Encountered error with status code: ', status_code
		if status_code == 420:
			return False
		return True

def makeHTML(mydict, api):
	f = open('my-map.html', 'w')

	lat = mydict['response']['geocode']['center']['lat']
	lng = mydict['response']['geocode']['center']['lng']
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
	for i in lst:
		tempgeo = {}
		tempgeo['lat'] = i['venue']['location']['lat']
		tempgeo['lng'] = i['venue']['location']['lng']
		tempnames.append(i['venue']['name'])
		tempaddresses.append(i['venue']['location']['formattedAddress'])
		try:
			tempphones.append(i['venue']['contact']['formattedPhone'])
		except:
			tempphones.append("N/A")
		try:
			tempratings.append(i['venue']['rating'])
		except:
			tempratings.append("N/A")
		try:
			tempurls.append(i['venue']['url'])
		except:
			tempurls.append("N/A")
		markers.append(tempgeo)

	names = json.dumps(tempnames)
	addresses = json.dumps(tempaddresses)
	phones = json.dumps(tempphones)
	ratings = json.dumps(tempratings)
	urls = json.dumps(tempurls)
	message = """
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <style>
      html, body, #map {
        margin: 0;
        padding: 0;
        width: 500px;
        height: 400px;
      }
    </style>
    <script src="https://maps.googleapis.com/maps/api/js?key="""+str(api)+""""></script>
    <script>
      var map;

      var markers = """+str(markers)+"""
      var names = """+str(names)+"""
      var addresses = """+str(addresses)+"""
      var phones = """+str(phones)+"""
      var ratings = """+str(ratings)+"""
      var urls = """+str(urls)+"""
      function initialize() {
        var myLatLng = {lat: """+str(lat)+""", lng: """+str(lng)+"""}
        var mapOptions = {
          zoom: 13,
          maxZoom: 17,
          center: myLatLng,
          mapTypeId: google.maps.MapTypeId.HYBRID
        };
        map = new google.maps.Map(document.getElementById('map'), mapOptions);

        infowindow = new google.maps.InfoWindow();

        for (var i = 0; i < markers.length; i++){
          var latlng = {lat: markers[i].lat, lng: markers[i].lng};
          var marker = new google.maps.Marker({
            map: map,
            position: latlng,
          });

          if (urls[i]=='N/A'){
            marker.contentString = '<div id="content">'+
              '<div id="siteNotice">'+
              '</div>'+
              '<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
              '<div id="bodyContent">'+
              '<p>'+addresses[i]+'</p>'+
              '<p>Phone: '+phones[i]+'</p>'+
              '<p>Rating: '+ratings[i]+'</p>'+
              '<p>URL: '+urls[i]+'</p>'+
              '</div>'+
              '</div>';
          }else{
            marker.contentString = '<div id="content">'+
              '<div id="siteNotice">'+
              '</div>'+
              '<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
              '<div id="bodyContent">'+
              '<p>'+addresses[i]+'</p>'+
              '<p>Phone:'+phones[i]+'</p>'+
              '<p>Rating: '+ratings[i]+'</p>'+
              '<p>URL: <a href="'+urls[i]+'">'+urls[i]+'</a></p>'+
              '</div>'+
              '</div>';
          }

          google.maps.event.addListener(marker, 'click', function() {
            infowindow.setContent(this.contentString);
            infowindow.open(map, this);
          });
        }
      }

      google.maps.event.addDomListener(window, 'load', initialize);

  </script>
  </head>
  <body>
    <div id="map"></div>
  </body>
</html>"""

	f.write(message)
	f.close()	

def makeTwitterStream(mydict, search, consumer_key, consumer_secret, access_token, access_token_secret):

	llng = mydict['response']['geocode']['geometry']['bounds']['sw']['lng']
	llat = mydict['response']['geocode']['geometry']['bounds']['sw']['lat']
	rlng = mydict['response']['geocode']['geometry']['bounds']['ne']['lng']
	rlat = mydict['response']['geocode']['geometry']['bounds']['ne']['lat']

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	apiT = tweepy.API(auth)

	myStream = tweepy.Stream(apiT.auth, MyStreamListener(mydict, search))
	myStream.filter(locations=[llng, llat, rlng, rlat], async=True)

def getTwitter(userid, consumer_key, consumer_secret, access_token, access_token_secret):


	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	user = api.get_user(userid)
	screenname = user.screen_name
	name = user.name
	location = user.location
	description = user.description
	followers = str(user.followers_count)
	friends = str(user.friends_count)
	statuses = str(user.statuses_count)
	if (user.url == None):
		url = 'N/A'
	else:
		url = user.url

	print "Screen Name: " + screenname
	print "User Name: " + name
	print "User Location: " + location
	print "User Description: " + description
	print "The Number of Followers: " + followers
	print "The Number of Friends: " + friends
	print "The Number of Statuses: " + statuses
	print "User URL: " + url + "\n"
	tweet = api.user_timeline(screenname)
	for status in tweet:
		print status.text

def webCrawl(mydict, ck, cs, at, ats):

	lst = mydict['response']['groups'][0]['items']
	userids = []

	for i in lst:
		checked = False
		try:
			response = requests.get(i['venue']['url'])
			print i['venue']['name']
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
						print userid
						getTwitter(userid, ck, cs, at, ats)
						print "\n"
						userids.append(userid)
		except Exception as e:
			#print str(e) + ": " + i['venue']['name']
			pass

# main script
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
	elif components[0] == 'iClient_ID':
		iCLIENT_ID = str(components[1])
	elif components[0] == 'iClient_Secret':
		iCLIENT_SECRET = str(components[1])
	elif components[0] == 'iAccess_Token':
		iaccess_token = str(components[1])

# use current date to obtain version detail
V_CODE = datetime.date.today().strftime("%Y%m%d")

# run in default mode or custom mode
mode = raw_input("Would you like to run on the default settings (y/n): ")

# default search
if mode == 'y':
	section = 'topPicks'
	query = section
	thisurl = "https://api.foursquare.com/v2/venues/explore?client_id="+fCLIENT_ID+"&client_secret="+fCLIENT_SECRET+"&v="+V_CODE+"&near=South Bend, IN&section="+section
# custom search
elif mode == 'n':
#allow user to specify location, radius, etc.
	location = raw_input("Enter a city: ")
	radius = raw_input("Enter a range: ")
	query = raw_input("What are you looking for: ")
	limit = raw_input("Maximum number of venues: ")

	# Obtain the data
	thisurl = "https://api.foursquare.com/v2/venues/explore?client_id="+fCLIENT_ID+"&client_secret="+fCLIENT_SECRET+"&v="+V_CODE+"&near="+location+"&query="+query+"&radius="+str(radius)+"&limit="+str(limit)
# wrong input
else:
	print "Incorrect input\n"
	exit()
r = requests.get(thisurl)

# store the json text
data = r.json()

# Write the data to a file
if r.status_code == 200:
	#use current time to name the file
	filename = datetime.datetime.now().strftime("%H%M%S%Y%m%d")
	datafile = open(filename+".json", "w")
	datafile.write(json.dumps(data, indent=4, sort_keys=True))
	datafile.close()
	print filename+".json created!"
	makeHTML(data, api)
	#webbrowser.open('my-map.html')
	webCrawl(data, consumer_key, consumer_secret, access_token, access_token_secret)
	#makeTwitterStream(data, query, consumer_key, consumer_secret, access_token, access_token_secret)
else:
	print r
	print json.dumps(data, indent=4, sort_keys=True)
	exit()

