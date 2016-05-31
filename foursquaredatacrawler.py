#!/usr/local/python

# Brian Mann
# 5/30/2016

import webbrowser, urllib2, time, datetime, json, requests, tweepy

class MyStreamListener(tweepy.StreamListener):

	def __init__(self, api=None):
		super(MyStreamListener, self).__init__()
		self.numtweets = 0
		self.maxtweets = 100

	def on_status(self, status):
		self.numtweets += 1
		print status.text
		if self.numtweets > self.maxtweets:
			print self.numtweets
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

def makeTwitterStream(mydict, consumer_key, consumer_secret, access_token, access_token_secret):

	llng = mydict['response']['geocode']['geometry']['bounds']['sw']['lng']
	llat = mydict['response']['geocode']['geometry']['bounds']['sw']['lat']
	rlng = mydict['response']['geocode']['geometry']['bounds']['ne']['lng']
	rlat = mydict['response']['geocode']['geometry']['bounds']['ne']['lat']

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	apiT = tweepy.API(auth)

	myStream = tweepy.Stream(apiT.auth, MyStreamListener())
	myStream.filter(locations=[llng, llat, rlng, rlat], async=True)

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

# run in default mode or custom mode
mode = raw_input("Would you like to run on the default settings (y/n): ")

# default search
if mode == 'y':
	thisurl = "https://api.foursquare.com/v2/venues/explore?client_id="+CLIENT_ID+"&client_secret="+CLIENT_SECRET+"&v="+V_CODE+"&near=South Bend, IN&section=topPicks"
# custom search
elif mode == 'n':
#allow user to specify location, radius, etc.
	location = raw_input("Enter a city: ")
	radius = raw_input("Enter a range: ")
	section = raw_input("One of food, drinks, coffee, shops, arts, outdoors, sights, trending, or specials, nextVenues, or topPicks: ")
	if section == "":
		query = raw_input("Kind of food place: ")
	limit = raw_input("Maximum number of venues: ")

	# Obtain the data
	thisurl = "https://api.foursquare.com/v2/venues/explore?client_id="+CLIENT_ID+"&client_secret="+CLIENT_SECRET+"&v="+V_CODE+"&near="+location+"&section="+section+"&query="+query+"&radius="+str(radius)+"&limit="+str(limit)
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
	#datafile = open(filename+".json", "w")
	#datafile.write(json.dumps(data, indent=4, sort_keys=True))
	#datafile.close()
	#print filename+".json created!"
	makeHTML(data, api)
	#webbrowser.open('my-map.html')
	makeTwitterStream(data, consumer_key, consumer_secret, access_token, access_token_secret)
else:
	print r
	print json.dumps(data, indent=4, sort_keys=True)
	exit()

