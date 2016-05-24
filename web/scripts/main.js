// Brian Mann
// main.js
// 5/24/2016

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

// dummy label
var dlabel = new Label();
dlabel.createLabel("", "thedLabel");
dlabel.addToDocument();

args = [linput, rinput, sdropdown, qinput, liinput, dlabel];
rbutton.addClickEventHandler(display, args);

function display(args){
	thelocation = args[0].getValue();
	range = args[1].getValue();
	section = args[2].getSelected();
	if(section == "None"){
		query = args[3].getValue();
	}else{
		query = "";
	}
	limit = args[4].getValue();
	args[5].setText(thelocation+" "+range+" "+section+" "+query+" "+limit);
}
