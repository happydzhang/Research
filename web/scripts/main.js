// Brian Mann
// main.js
// 6/6/2016

var map;
var mymarkers = [];
var url = "http://0.0.0.0:8008/";

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
	var params = "{\"location\": \""+thelocation+"\", \"range\": \""+range+"\", \"query\": \""+query+"\", \"limit\": \""+limit+"\"}";	

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
			});
			// add the markers to an array to allow for deletion
			mymarkers.push(marker);

			// generate the info window's text based on whether or not the venue has a url
			if (urls[i]=='N/A'){
				// does not have a url link
				marker.contentString = '<div id="tabs">'+
					'<ul>'+
					'<li><a href="#tab-1"><span>Foursquare</span></a></li>'+
					'<li><a href="#tab-2"><span>Twitter</span></a></li>'+
					'<li><a href="#tab-3"><span>Instagram</span></a></li>'+
					'</ul>'+
					'<div id="tab-1">'+
					'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
					'<p>Address: '+addresses[i]+'</p>'+
					'<p>Phone: '+phones[i]+'</p>'+
					'<p>Rating: '+ratings[i]+'</p>'+
					'<p>Currently here: '+here[i]+'</p>'+
					'<p>URL: '+urls[i]+'</p>'+
					'<p>User Comment: '+tips[i]+'</p>'+
					'</div>'+
					'<div id="tab-2">'+
					'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
					'<p>Screenname: Loading...</p>'+
					'<p>Description: Loading...</p>'+
					'<p>Followers: Loading...</p>'+
					'<div id="tab-3">'+
					'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
					'</div>'+
					'</div>';
			}else{
				// does have a url link
				marker.contentString = '<div id="tabs">'+
					'<ul>'+
					'<li><a href="#tab-1"><span>Foursquare</span></a></li>'+
					'<li><a href="#tab-2"><span>Twitter</span></a></li>'+
					'<li><a href="#tab-3"><span>Instagram</span></a></li>'+
					'<div id="tab-1">'+
					'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
					'<p>Address: '+addresses[i]+'</p>'+
					'<p>Phone: '+phones[i]+'</p>'+
					'<p>Rating: '+ratings[i]+'</p>'+
					'<p>Currently here: '+here[i]+'</p>'+
					'<p>URL: <a href="'+urls[i]+'">'+urls[i]+'</a></p>'+
					'<p>User Comment: '+tips[i]+'</p>'+
					'</div>'+
					'<div id="tab-2">'+
					'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
					'<p>Screenname: Loading...</p>'+
					'<p>Description: Loading...</p>'+
					'<p>Followers: Loading...</p>'+
					'<div id="tab-3">'+
					'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
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
		var http = new XMLHttpRequest();
		http.open("POST", url+'instagram/', true);
		http.onload = function(e){
			var l = JSON.parse(http.responseText);
		}
		http.onerror = function(e) {console.log(http.statusText);}
		http.send(parameters);
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
				});
				mymarkers.push(marker);

				if (urls[i]=='N/A'){
					// content string with no links
					marker.contentString = '<div id="tabs">'+
						'<ul>'+
						'<li><a href="#tab-1"><span>Foursquare</span></a></li>'+
						'<li><a href="#tab-2"><span>Twitter</span></a></li>'+
						'<li><a href="#tab-3"><span>Instagram</span></a></li>'+
						'</ul>'+
						'<div id="tab-1">'+
						'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
						'<p>Address: '+addresses[i]+'</p>'+
						'<p>Phone: '+phones[i]+'</p>'+
						'<p>Rating: '+ratings[i]+'</p>'+
						'<p>Currently here: '+here[i]+'</p>'+
						'<p>URL: '+urls[i]+'</p>'+
						'<p>User Comment: '+tips[i]+'</p>'+
						'</div>'+
						'<div id="tab-2">'+
						'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
						'<p>Screenname: '+screennames[i]+'</p>'+
						'<p>Description: '+descriptions[i]+'</p>'+
						'<p>Followers: '+followers[i]+'</p>'+
						'<div id="tab-3">'+
						'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
						'</div>'+
						'</div>';
				}else{
					if (screennames[i] == 'N/A'){
						// content string with a link to the url
						marker.contentString = '<div id="tabs">'+
							'<ul>'+
							'<li><a href="#tab-1"><span>Foursquare</span></a></li>'+
							'<li><a href="#tab-2"><span>Twitter</span></a></li>'+
							'<li><a href="#tab-3"><span>Instagram</span></a></li>'+
							'<div id="tab-1">'+
							'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
							'<p>Address: '+addresses[i]+'</p>'+
							'<p>Phone: '+phones[i]+'</p>'+
							'<p>Rating: '+ratings[i]+'</p>'+
							'<p>Currently here: '+here[i]+'</p>'+
							'<p>URL: <a href="'+urls[i]+'">'+urls[i]+'</a></p>'+
							'<p>User Comment: '+tips[i]+'</p>'+
							'</div>'+
							'<div id="tab-2">'+
							'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
							'<p>Screenname: '+screennames[i]+'</p>'+
							'<p>Description: '+descriptions[i]+'</p>'+
							'<p>Followers: '+followers[i]+'</p>'+
							'<div id="tab-3">'+
							'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
							'</div>'+
							'</div>';
					}else{
						// content string with a link to the url and the twitter page
						marker.contentString = '<div id="tabs">'+
							'<ul>'+
							'<li><a href="#tab-1"><span>Foursquare</span></a></li>'+
							'<li><a href="#tab-2"><span>Twitter</span></a></li>'+
							'<li><a href="#tab-3"><span>Instagram</span></a></li>'+
							'<div id="tab-1">'+
							'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
							'<p>Address: '+addresses[i]+'</p>'+
							'<p>Phone: '+phones[i]+'</p>'+
							'<p>Rating: '+ratings[i]+'</p>'+
							'<p>Currently here: '+here[i]+'</p>'+
							'<p>URL: <a href="'+urls[i]+'">'+urls[i]+'</a></p>'+
							'<p>User Comment: '+tips[i]+'</p>'+
							'</div>'+
							'<div id="tab-2">'+
							'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
							'<p>Screenname: <a href="https://twitter.com/'+screennames[i]+'">'+screennames[i]+'</a></p>'+
							'<p>Description: '+descriptions[i]+'</p>'+
							'<p>Followers: '+followers[i]+'</p>'+
							'<p>Recent Tweets: <br>'+utweet[i]+'</p>'+
							'<div id="tab-3">'+
							'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
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
			}
		}
		xml.onerror = function(e) {console.log(xml.statusText);}
		xml.send(parameters);
	}
	html.onerror = function(e) {console.log(html.statusText);}
	html.send(params);
}
