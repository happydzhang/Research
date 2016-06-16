// Brian Mann
// main.js
// 6/14/2016

var map;
var service;
var mymarkers = [];
var url = "http://0.0.0.0:8008/";
var gratings = [];

// google map
function initialize() {
	var myLatLng = {lat: 39.8333333, lng: -98.585522};
	var mapOptions = {
		zoom: 3,
		maxZoom: 18,
		center: myLatLng,
		mapTypeId: google.maps.MapTypeId.HYBRID
	};
	map = new google.maps.Map(document.getElementById('map'), mapOptions);
}

google.maps.event.addDomListener(window, 'load', initialize);

// refresh button
var rbutton = new Button();
rbutton.createButton("Refresh", "therButton");
rbutton.addToDocument();

// location label
var llabel = new Label();
llabel.createLabel("Location", "thelLabel");
llabel.addToDocument();

// location box
var linput = new Input();
linput.createInput("South Bend", "thelInput");
linput.addToDocument();

// radius label
var rlabel = new Label();
rlabel.createLabel("Range (in meters)", "therLabel");
rlabel.addToDocument();

// radius box
var rinput = new Input();
rinput.createInput("250", "therInput");
rinput.addToDocument();

// query label
var qlabel = new Label();
qlabel.createLabel("What are you looking for?", "theqLabel");
qlabel.addToDocument();

// query box
var qinput = new Input();
qinput.createInput("", "theqInput");
qinput.addToDocument();

// limit label
var lilabel = new Label();
lilabel.createLabel("Limit", "theliLabel");
lilabel.addToDocument();

// limit box
var liinput = new Input();
liinput.createInput("10", "thelInput");
liinput.addToDocument();

args = [linput, rinput, qinput, liinput];
rbutton.addClickEventHandler(refresh, args);

function refresh(args){
	// clear the map of all markers
	for (var i = 0;i < mymarkers.length; i++){
		mymarkers[i].setMap(null)
	}
	// clear the array of markers
	mymarkers = [];
	// grab the parameters for the foursquare search
	thelocation = args[0].getValue();
	range = args[1].getValue();
	query = args[2].getValue();
	limit = args[3].getValue();
	// prepare as json
	var objs = {}
	objs['location'] = thelocation;
	objs['range'] = range;
	objs['query'] = query;
	objs['limit'] = limit;
	var params = JSON.stringify(objs);

	// new XML request
	var html = new XMLHttpRequest();
	html.open("POST", url+'foursquare/', true);
	html.onload = function(e){
		var j = JSON.parse(html.responseText);

		// assign from the response
		var mylatlng = {lat: j['lat'], lng: j['lng']};
		var markers = j['markers'];
		var names = j['names'];
		var addresses = j['addresses'];
		var phones = j['phones'];
		var ratings = j['ratings'];
		var urls = j['urls'];
		var here = j['here'];
		var tips = j['tips'];
		map.setCenter(mylatlng);

		// prepare the info window
		infowindow = new google.maps.InfoWindow();

		// loop through each venue
		for (var i = 0; i < markers.length; i++){
			// create a new marker at each venue's location
			var latlng = {lat: markers[i].lat, lng: markers[i].lng};
			var marker = new google.maps.Marker({
				map: map,
				position: latlng,
				icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
			});

			var request = {
				location: mylatlng,
				radius: range,
				query: names[i]
			};

			service = new google.maps.places.PlacesService(map);
			service.textSearch(request, callback_search);
			// add the markers to an array to allow for deletion
			mymarkers.push(marker);

			// generate the info window's text based on whether or not the venue has a url
			if (urls[i]=='N/A'){
				// does not have a url link
				marker.contentString = '<div id="tabs">'+
					'<ul>'+
					'<li><a href="#tab-1"><span>Info</span></a></li>'+
					'<li><a href="#tab-2"><span>Ratings</span></a></li>'+
					'<li><a href="#tab-3"><span>Comments and Reviews</span></a></li>'+
					'</ul>'+
					'<div id="tab-1">'+
					'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
					'<p>Address: '+addresses[i]+'</p>'+
					'<p>Phone: '+phones[i]+'</p>'+
					'<p>Currently here: '+here[i]+'</p>'+
					'</div>'+
					'<div id="tab-2">'+
					'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
					'<p>Foursquare Rating: '+ratings[i]+'/10</p>'+
					'<p>Google Rating: '+gratings[i]+'/5</p>'+
					'</div>'+
					'<div id="tab-3">'+
					'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
					'<p>User Comment: '+tips[i]+'</p>'+
					'</div>'+
					'</div>';
			}else{
				// does have a url link
				marker.contentString = '<div id="tabs">'+
					'<ul>'+
					'<li><a href="#tab-1"><span>Info</span></a></li>'+
					'<li><a href="#tab-2"><span>Ratings</span></a></li>'+
					'<li><a href="#tab-3"><span>Comments and Reviews</span></a></li>'+
					'<div id="tab-1">'+
					'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
					'<p>Address: '+addresses[i]+'</p>'+
					'<p>Phone: '+phones[i]+'</p>'+
					'<p>Currently here: '+here[i]+'</p>'+
					'<p>URL: <a href="'+urls[i]+'">'+urls[i]+'</a></p>'+
					'</div>'+
					'<div id="tab-2">'+
					'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
					'<p>Foursquare Rating: '+ratings[i]+'/10</p>'+
					'<p>Google Rating: '+gratings[i]+'/5</p>'+
					'</div>'+
					'<div id="tab-3">'+
					'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
					'<p>User Comment: '+tips[i]+'</p>'+
					'</div>'+
					'</div>';
			}

			// prepare jQuery tabs
			google.maps.event.addListener(infowindow, 'domready', function(){
				$('#tabs').tabs();
			});

			// add click function
			google.maps.event.addListener(marker, 'click', function() {
				infowindow.setContent(this.contentString);
				infowindow.open(map, this);

			});
		}

		// zoom to show a more general view of the search
		map.setZoom(13);

		// prepare the twitter request
		var obj = {};
		obj['urls'] = urls;
		var parameters = JSON.stringify(obj);
		// new XML request
		/*var http = new XMLHttpRequest();
		http.open("POST", url+'instagram/', true);
		http.onload = function(e){
			var l = JSON.parse(http.responseText);
		}
		http.onerror = function(e) {console.log(http.statusText);}
		http.send(parameters);*/

		// new XML request
		var xml = new XMLHttpRequest();
		xml.open("POST", url+'twitter/', true);
		xml.onload = function(e){
			var l = JSON.parse(xml.responseText);
			var screennames = l['screennames'];
			var descriptions = l['descriptions'];
			var followers = l['followers'];
			var tweets = l['tweets'];
			var utweet = [];
			for (var i = 0; i < tweets.length; i++){
				var tweet = '';
				for (var j = 0; j < tweets[i].length; j++){
					tweet += tweets[i][j]+"<br><br>";
				}
				utweet.push(tweet);
			}
			// the same as before with the foursquare data, but now with the additional twitter data
			for (var i = 0; i < markers.length; i++){
				var latlng = {lat: markers[i].lat, lng: markers[i].lng};
				var marker = new google.maps.Marker({
					map: map,
					position: latlng,
					icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
				});
				mymarkers.push(marker);

				if (urls[i]=='N/A'){
					// content string with no links
					marker.contentString = '<div id="tabs">'+
						'<ul>'+
						'<li><a href="#tab-1"><span>Info</span></a></li>'+
						'<li><a href="#tab-2"><span>Ratings</span></a></li>'+
						'<li><a href="#tab-3"><span>Comments and Reviews</span></a></li>'+
						'</ul>'+
						'<div id="tab-1">'+
						'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
						'<p>Address: '+addresses[i]+'</p>'+
						'<p>Phone: '+phones[i]+'</p>'+
						'<p>Currently here: '+here[i]+'</p>'+
						'</div>'+
						'<div id="tab-2">'+
						'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
						'<p>Foursquare Rating: '+ratings[i]+'/10</p>'+
						'<p>Google Rating: '+gratings[i]+'/5</p>'+
						'</div>'+
						'<div id="tab-3">'+
						'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
						'<p>User Comment: '+tips[i]+'</p>'+
						'</div>'+
						'</div>';
				}else{
					if (screennames[i] == 'N/A'){
						// content string with a link to the url
						marker.contentString = '<div id="tabs">'+
							'<ul>'+
							'<li><a href="#tab-1"><span>Info</span></a></li>'+
							'<li><a href="#tab-2"><span>Ratings</span></a></li>'+
							'<li><a href="#tab-3"><span>Comments and Reviews</span></a></li>'+
							'<div id="tab-1">'+
							'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
							'<p>Address: '+addresses[i]+'</p>'+
							'<p>Phone: '+phones[i]+'</p>'+
							'<p>Currently here: '+here[i]+'</p>'+
							'<p>URL: <a href="'+urls[i]+'">'+urls[i]+'</a></p>'+
							'</div>'+
							'<div id="tab-2">'+
							'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
							'<p>Foursquare Rating: '+ratings[i]+'/10</p>'+
							'<p>Google Rating: '+gratings[i]+'/5</p>'+
							'</div>'+
							'<div id="tab-3">'+
							'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
							'<p>User Comment: '+tips[i]+'</p>'+
							'</div>'+
							'</div>';
					}else{
						// content string with a link to the url and the twitter page
						marker.contentString = '<div id="tabs">'+
							'<ul>'+
							'<li><a href="#tab-1"><span>Info</span></a></li>'+
							'<li><a href="#tab-2"><span>Ratings</span></a></li>'+
							'<li><a href="#tab-3"><span>Comments and Reviews</span></a></li>'+
							'<div id="tab-1">'+
							'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
							'<p>Address: '+addresses[i]+'</p>'+
							'<p>Phone: '+phones[i]+'</p>'+
							'<p>Currently here: '+here[i]+'</p>'+
							'<p>URL: <a href="'+urls[i]+'">'+urls[i]+'</a></p>'+
							'<p>Screenname: <a href="https://twitter.com/'+screennames[i]+'">'+screennames[i]+'</a></p>'+
							'<p>Description: '+descriptions[i]+'</p>'+
							'<p>Followers: '+followers[i]+'</p>'+
							'</div>'+
							'<div id="tab-2">'+
							'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
							'<p>Foursquare Rating: '+ratings[i]+'/10</p>'+
							'<p>Google Rating: '+gratings[i]+'/5</p>'+
							'</div>'+
							'<div id="tab-3">'+
							'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
							'<p>User Comment: '+tips[i]+'</p>'+
							'<p>Recent Tweets: <br>'+utweet[i]+'</p>'+
							'</div>'+
							'</div>';
					}
				}

				google.maps.event.addListener(infowindow, 'domready', function(){
					$('#tabs').tabs();
				});

				google.maps.event.addListener(marker, 'click', function() {
					infowindow.setContent(this.contentString);
					infowindow.open(map, this);

				});
				if (screennames[i] != "N/A"){
					marker.setIcon('http://maps.google.com/mapfiles/ms/icons/blue-dot.png');
				}
			}
		}
		xml.onerror = function(e) {console.log(xml.statusText);}
		xml.send(parameters);
	}
	html.onerror = function(e) {console.log(html.statusText);}
	html.send(params);
}

function callback_search(results, status){
	if (status == 'OK'){
		if (typeof results[0]['rating'] !== 'undefined'){
			gratings.push(results[0]['rating']);
		}else{
			gratings.push(0);
		}
	}
}

