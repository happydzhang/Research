# Brian Mann
# 2/3/2015

import time, datetime, json, requests

searches = 0

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
