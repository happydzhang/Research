// Brian Mann
// objects.js
// 5/24/2016

var Item = {
	addToDocument: function(){
		document.body.appendChild(this.item);
	}
}

function Label() {
	this.createLabel = function(text, id){
		this.item = document.createElement("p");
		this.item.setAttribute("id", id);
		labeltext = document.createTextNode(text);
		this.item.appendChild(labeltext);
	}
	this.setText = function(text){
		this.item.innerHTML = text;
	}
}

function Button() {
	this.createButton = function(text, id){
		this.item = document.createElement("button");
		this.item.setAttribute("id", id);
		btntxt = document.createTextNode(text);
		this.item.appendChild(btntxt);	
	}
	this.addClickEventHandler = function(handler, args){
		this.item.onmouseup = function() {
			handler(args);
		};
	}
}

function Input(){
	this.createInput = function(text, id){
		this.item = document.createElement("input");
		this.item.setAttribute("id", id);
		this.item.value = text;
	}
	this.getValue = function(){
		return this.item.value;
	}
}

Label.prototype = Item;
Button.prototype = Item;
Input.prototype = Item;
