// Brian Mann
// main.js
// 6/6/2016

var map;
var mymarkers = [];
var url = "http://0.0.0.0:8008/";

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
	for (var i = 0;i < mymarkers.length; i++){
		mymarkers[i].setMap(null)
	}
	mymarkers = [];
	thelocation = args[0].getValue();
	range = args[1].getValue();
	query = args[2].getValue();
	limit = args[3].getValue();
	var params = "{\"location\": \""+thelocation+"\", \"range\": \""+range+"\", \"query\": \""+query+"\", \"limit\": \""+limit+"\"}";	

	var html = new XMLHttpRequest();
	html.open("POST", url+'foursquare/', true);
	html.onload = function(e){
		var j = JSON.parse(html.responseText);

		var mylatlng = {lat: j['lat'], lng: j['lng']};
		var markers = j['markers'];
		var names = j['names'];
		var addresses = j['addresses'];
		var phones = j['phones'];
		var ratings = j['ratings'];
		var urls = j['urls'];
		map.setCenter(mylatlng);

		var obj = {};
		obj['urls'] = urls;
		var parameters = JSON.stringify(obj);
		var xml = new XMLHttpRequest();
		xml.open("POST", url+'twitter/', true);
		xml.onload = function(e){
			var l = JSON.parse(xml.responseText);
			var screennames = l['screennames'];
			var descriptions = l['descriptions'];
			var followers = l['followers'];
			for (var i = 0; i < markers.length; i++){
				var latlng = {lat: markers[i].lat, lng: markers[i].lng};
				var marker = new google.maps.Marker({
					map: map,
					position: latlng,
				});
				mymarkers.push(marker);

				if (urls[i]=='N/A'){
					marker.contentString = '<div id="tabs">'+
						'<ul>'+
						'<li><a href="#tab-1"><span>Foursquare</span></a></li>'+
						'<li><a href="#tab-2"><span>Twitter</span></a></li>'+
						'</ul>'+
						'<div id="tab-1">'+
						'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
						'<p>Address: '+addresses[i]+'</p>'+
						'<p>Phone: '+phones[i]+'</p>'+
						'<p>Rating: '+ratings[i]+'</p>'+
						'<p>URL: '+urls[i]+'</p>'+
						'</div>'+
						'<div id="tab-2">'+
						'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
						'<p>Screenname: '+screennames[i]+'</p>'+
						'<p>Description: '+descriptions[i]+'</p>'+
						'<p>Followers: '+followers[i]+'</p>'+
						'</div>'+
						'</div>';
				}else{
					marker.contentString = '<div id="tabs">'+
						'<ul>'+
						'<li><a href="#tab-1"><span>Foursquare</span></a></li>'+
						'<li><a href="#tab-2"><span>Twitter</span></a></li>'+
						'<div id="tab-1">'+
						'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
						'<p>Address: '+addresses[i]+'</p>'+
						'<p>Phone: '+phones[i]+'</p>'+
						'<p>Rating: '+ratings[i]+'</p>'+
						'<p>URL: <a href="'+urls[i]+'">'+urls[i]+'</a></p>'+
						'</div>'+
						'<div id="tab-2">'+
						'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
						'<p>Screenname: '+screennames[i]+'</p>'+
						'<p>Description: '+descriptions[i]+'</p>'+
						'<p>Followers: '+followers[i]+'</p>'+
						'</div>'+
						'</div>';
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

		infowindow = new google.maps.InfoWindow();

		for (var i = 0; i < markers.length; i++){
			var latlng = {lat: markers[i].lat, lng: markers[i].lng};
			var marker = new google.maps.Marker({
				map: map,
				position: latlng,
			});
			mymarkers.push(marker);

			if (urls[i]=='N/A'){
				marker.contentString = '<div id="tabs">'+
					'<ul>'+
					'<li><a href="#tab-1"><span>Foursquare</span></a></li>'+
					'<li><a href="#tab-2"><span>Twitter</span></a></li>'+
					'</ul>'+
					'<div id="tab-1">'+
					'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
					'<p>Address: '+addresses[i]+'</p>'+
					'<p>Phone: '+phones[i]+'</p>'+
					'<p>Rating: '+ratings[i]+'</p>'+
					'<p>URL: '+urls[i]+'</p>'+
					'</div>'+
					'<div id="tab-2">'+
					'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
					'<p>Screenname: Loading...</p>'+
					'<p>Description: Loading...</p>'+
					'<p>Followers: Loading...</p>'+
					'</div>'+
					'</div>';
			}else{
				marker.contentString = '<div id="tabs">'+
					'<ul>'+
					'<li><a href="#tab-1"><span>Foursquare</span></a></li>'+
					'<li><a href="#tab-2"><span>Twitter</span></a></li>'+
					'<div id="tab-1">'+
					'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
					'<p>Address: '+addresses[i]+'</p>'+
					'<p>Phone: '+phones[i]+'</p>'+
					'<p>Rating: '+ratings[i]+'</p>'+
					'<p>URL: <a href="'+urls[i]+'">'+urls[i]+'</a></p>'+
					'</div>'+
					'<div id="tab-2">'+
					'<h1 id="firstHeading" class="firstHeading">'+names[i]+'</h1>'+
					'<p>Screenname: Loading...</p>'+
					'<p>Description: Loading...</p>'+
					'<p>Followers: Loading...</p>'+
					'</div>'+
					'</div>';
			}

			google.maps.event.addListener(infowindow, 'domready', function(){
				$('#tabs').tabs();
			});

			google.maps.event.addListener(marker, 'click', function() {
				infowindow.setContent(this.contentString);
				infowindow.open(map, this);

			});
		}

		map.setZoom(13);
	}
	html.onerror = function(e) {console.log(html.statusText);}
	html.send(params);
}
