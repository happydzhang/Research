// Brian Mann
// main.js
// 5/24/2016

var map;
var url = "0.0.0.0"

function initialize() {
	var myLatLng = {lat: 41.68338, lng: -86.25001}
	var mapOptions = {
		zoom: 13,
		maxZoom: 17,
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

// section label
var slabel = new Label();
slabel.createLabel("Section", "thesLabel");
slabel.addToDocument();

// section dropdown
var sdropdown = new Dropdown();
dict = ["None", "food", "drinks", "coffee", "shops", "arts", "outdoors", "sights", "trending", "specials", "nextVenues", "topPicks"];
sdropdown.createDropdown(dict, "thesDropdown", 0);
sdropdown.addToDocument();

// query label
var qlabel = new Label();
qlabel.createLabel("Query", "theqLabel");
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

args = [linput, rinput, sdropdown, qinput, liinput];
rbutton.addClickEventHandler(refresh, args);

function refresh(args){
	thelocation = args[0].getValue();
	range = args[1].getValue();
	section = args[2].getSelected();
	if(section == "None"){
		query = args[3].getValue();
	}else{
		query = "";
	}
	limit = args[4].getValue();
	var params = "{\"location\": \""+thelocation+"\", \"range\": \""+range+"\", \"section\": \""+section+"\", \"query\": \""+query+"\", \"limit\": \""+limit+"\"}";	

	var marker = new google.maps.Marker({
		map: map,
		position: {lat: 41.68338, lng: -86.25001},
	});
	google.maps.event.addDomListener(window, 'load', initialize);

	var html = new XMLHttpRequest();
	html.open("POST", url, true);
	html.onload = function(e){
		var j = JSON.parse(html.responseText);
		
	}
	html.onerror = function(e) {console.log(html.statusText);}
	html.send(params);
}
