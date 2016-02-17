# Brian Mann
# 2/3/2015

import webbrowser, urllib2, time, datetime, json, requests

def getMap(mydict):
	lat = mydict['response']['geocode']['center']['lat']
	lng = mydict['response']['geocode']['center']['lng']
	lst = mydict['response']['groups'][0]['items']
	lstlat = []
	lstlng = []
	markerstr = ""
	for lats in lst:
		lstlat.append(str(lats['venue']['location']['lat']))
	for lngs in lst:
		lstlng.append(str(lngs['venue']['location']['lng']))
	n = len(lstlat)
	for i in range(n):
		if i != n-1:
			markerstr += lstlat[i]+","+lstlng[i]+"|"
		else:
			markerstr += lstlat[i]+","+lstlng[i]
			
	url = "http://maps.google.com/maps/api/staticmap?center="+str(lat)+","+str(lng)+"&zoom=14&size=400x400&markers="+markerstr

	return url

# keys needed for access to url
CLIENT_ID = "X0JZOBTOXML0SUDIVYWAXZCIBCT4JPKGKSE4U0JZUAH2EOH5"
CLIENT_SECRET = "5YQWGTY5SMKA5GA40DFWHKSHHLJ1Y4BB1N4DZOQ2OVHK3UMY"
# use current date to obtain version detail
V_CODE = datetime.date.today().strftime("%Y%m%d")

# run in default mode or custom mode
mode = raw_input("Would you like to run on the default settings (y/n): ")

# default search
if mode == 'y':
	thisurl = "https://api.foursquare.com/v2/venues/explore?client_id="+CLIENT_ID+"&client_secret="+CLIENT_SECRET+"&v="+V_CODE+"&near=South Bend, IN&section=topPicks"
# custom search
elif mode == 'n':
# allow user to specify location, radius, etc.
	location = raw_input("Enter a city: ")
	radius = raw_input("Enter a range: ")
	section = raw_input("One of food, drinks, coffee, shops, arts, outdoors, sights, trending, or specials, nextVenues, or topPicks: ")

	# Obtain the data
	thisurl = "https://api.foursquare.com/v2/venues/explore?client_id="+CLIENT_ID+"&client_secret="+CLIENT_SECRET+"&v="+V_CODE+"&near="+location+"&section="+section+"&radius="+str(radius)
# wrong input
else:
	print "Incorrect input\n"
	exit()
r = requests.get(thisurl)

# store the json text
data = r.json()


mymap = getMap(data)
webbrowser.open(mymap)

# Write the data to a file
if r.status_code == 200:
	#use current time to name the file
	filename = datetime.datetime.now().strftime("%H%M%S%Y%m%d")
	datafile = open(filename+".json", "w")
	datafile.write(json.dumps(data, indent=4, sort_keys=True))
	datafile.close()
	print filename+".json created!"
else:
	print r
	print json.dumps(data, indent=4, sort_keys=True)
	exit()

