# Research
My Undergraduate Research with Professor Dong Wang

Notes for 5/26/2016
- (4:57) For tomorrow:
	- Determine a photo's filename
	- If photo was just taken, write the lat and long to the photo's EXIF data
- (4:27) EXIF Info that every image is stored with will be the best approach. App will allow the user to select a picture already taken, or to take a new one. It should then check for geolocation information in the EXIF Info, and, if there, should accept the photo; otherwise, the app should reject the user's photo.
- (4:12) Standard Camera App's geotagging ability cannot be programmatically enabled. This means that simply using an Intent in Android Studio will not suffice. Must completely explore the Android Camera API
- (12:36) Spent the morning reworking the Camera application. Application now operates very basically, allowing the user to either select a picture already on the phone, or to take a new one. The next step is to enforce the user to enable location services for the camera application

Notes for 5/25/2016
- (4:46) Found a lengthy tutorial on uploading photos to a server. Will explore in more detail tomorrow
- (4:39) Standard Camera App on Android devices can already enable location embedding, as it turns out. Previous work on BasicCameraApp is unnecessary, and a new project will be started, which will simply utilize the already existing camera application to take the photos, but send them to an online directory, instead of saving them locally.
- (3:30) Resumed work on the mobile application
- *(1:52) Next steps: GPS based search, and move towards data diversification*
- (1:41) Resolved minor bug of markers not clearing.
- (12:33) Python server successfully runs the script and sends the desired information to the client. Small issue remains where old markers need to be deleted upon starting a new search. Should be a simple fix
- (10:17) Web page successfully interacts with the Python server. Next step is adding data crawler script to the server

Notes for 5/24/2016
- (5:20) Prior data crawler remains untouched (besides minor quality of life update this morning)
- (5:15) Began turning Python script into server. Tomorrow will entail continuing that effort by finishing the server's ability to process requests and then send the results back, which the JS will then use to generate the proper map.
- (12:10) Basic webpage has been setup. Next step is changing the Python script to JavaScript
- (9:33) Planning on moving from simple Python script to interactive webpage; Python script might need to be turned into JS
- Removed URL from venues that do not have one

Notes for 4/20/2016
- Added venues' phone numbers to the infowindow
- Images provided by Foursquare seem to be bad links
- Hours of operation are also unreliable on Foursquare
- Explore Twitter API, Flickr, and Facebook for additional data
- Add GPS search
- GPS Photo-App

Notes for 4/18/2016
- Fell behind in consistently working on the application as I became bogged down by assignments in other courses
- Successfully added venues' websites to the infowindow, including making them a hyperlink
- Also began to refine the search process by adding try-except blocks
- Next step is to continue to improve the range of the search function by revisiting the features of the Foursquare API
- Also, explore the JSON datasets to determine other pertinent information to go into the infowindows.
- Long-term, use the Foursquare data to jump to other social media sites for extra data

Notes for 4/6/2016
- Moved API keys into a text file to prevent access to them on Github
- Ran into a minor issue getting information about a location, such as likes, because not all venues contain those indices
- Added information like steet address to info box. Next step would be links to websites, as well as Facebook and Twitter pages
- Added the venue's rating to the info window

Notes for 3/30/2016
- Markers' info box now correctly displays venues Name
- Must implement method to include important information regarding venue in the body of the info box
- Explore how to use gitignore to store things like API Keys

Notes for 3/23/2016
- Markers are displayed with an info box
- Markers' locations determined by dataset
- Info box does not contain info regarding the dataset

Notes for 3/15/2016
- Successfully have the data crawler also write the html file
- Currently working on getting the dataset to be written to the html file

Notes for 3/2/2016
- Must develop function to loop through all elements of array of dataset
- Must find way to get dataset created from Python script into an html object



