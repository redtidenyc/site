try {
	if(typeof(MochiKit.Base) == 'undefined' || 
	typeof(MochiKit.DOM) == 'undefined' || 
	typeof(MochiKit.Logging) == 'undefined' ) { throw ""; }
} catch(e) {
	throw "MochiKit.Redtide-ext depends on MochiKit.Base, MochiKit.DOM and MochiKit.Logging";
}

if(typeof(MochiKit.Redtide_ext) == 'undefined') {
	MochiKit.Redtide_ext = {};
}

MochiKit.Redtide_ext.NAME = "MochiKit.Redtide-ext";
MochiKit.Redtide_ext.VERSION = "0.1";

MochiKit.Redtide_ext.__repr__ = function () {
	return "[" + this.NAME + " " + this.VERSION + "]";
};

MochiKit.Redtide_ext.GetPageSize = function() {
    var xScroll, yScroll;
	
    if (window.innerHeight && window.scrollMaxY) {	
        xScroll = document.body.scrollWidth;
	yScroll = window.innerHeight + window.scrollMaxY;
    } else if (document.body.scrollHeight > document.body.offsetHeight){ // all but Explorer Mac
        xScroll = document.body.scrollWidth;
	yScroll = document.body.scrollHeight;
    } else { // Explorer Mac...would also work in Explorer 6 Strict, Mozilla and Safari
	xScroll = document.body.offsetWidth;
	yScroll = document.body.offsetHeight;
    }
	
    var windowWidth, windowHeight;
    if (self.innerHeight) {	// all except Explorer
        windowWidth = self.innerWidth;
        windowHeight = self.innerHeight;
    } else if (document.documentElement && document.documentElement.clientHeight) { // Explorer 6 Strict Mode
        windowWidth = document.documentElement.clientWidth;
        windowHeight = document.documentElement.clientHeight;
    } else if (document.body) { // other Explorers
	windowWidth = document.body.clientWidth;
        windowHeight = document.body.clientHeight;
    }	
	
    // for small pages with total height less then height of the viewport
    if(yScroll < windowHeight){
        pageHeight = windowHeight;
    } else { 
	pageHeight = yScroll;
    }

	// for small pages with total width less then width of the viewport
    if(xScroll < windowWidth){	
        pageWidth = windowWidth;
    } else {
        pageWidth = xScroll;
    }


    arrayPageSize = new Array(pageWidth,pageHeight,windowWidth,windowHeight) 
    return arrayPageSize;
}

MochiKit.Redtide_ext.GetPageScroll = function() {
    var yScroll;

    if (self.pageYOffset) {
        yScroll = self.pageYOffset;
    } else if (document.documentElement && document.documentElement.scrollTop){	 // Explorer 6 Strict
	yScroll = document.documentElement.scrollTop;
    } else if (document.body) {// all other Explorers
	yScroll = document.body.scrollTop;
    }

    arrayPageScroll = new Array('',yScroll) 
    return arrayPageScroll;
}

MochiKit.Redtide_ext.swapFromHttp = function(myId, xmlhttp) {
	/*
	  Use this in contexts like:
	  def = doSimpleXMLHttpRequest('myfile.xhtml');
	  def.addCallback(swapFromHttp, 'myId');
	  where $('myId') is the DOM that you want replaced with content
	  with the same id="myId" DOM element in the xml request
	  caveats:
	     IE 6 needs the Content-type: text/xml
	     Firefox wants
	     IE and Safari don't handle named entities like &nbsp; well in this
	context
	       and should be numeric (e.g. &#160;)
	*/	
	var resXML=xmlhttp.responseXML;
	var curr=$(myId);
	var scrollPos=curr.scrollTop; //save scroll position
	var newDOM = null;
	try {
		if (typeof(resXML.getElementById) == 'undefined') {
			//IE HACK
			//IE doesn't work because XML DOM isn't as rich as HTML DOM
			var findID = function(node) {
				if (newDOM) {return null;} //don't waste time after we've found it
				if (node.nodeType != 1) {
					//document node gets us going
					return (node.nodeType == 9) ? node.childNodes : null;
				}
				if (node.getAttribute('id') == myId) {
					newDOM = node;
					return null;
				}
				return node.childNodes;
			};
			MochiKit.Base.nodeWalk(resXML, findID); //walk the html tag
			curr.outerHTML=newDOM.xml;
		} else {
			newDOM=resXML.getElementById(myId);
			if (newDOM.outerHTML) {
				//SAFARI HACK
				//SAFARI fails because XML dom node can't be added into a replaceChild HTML function
				curr.innerHTML=newDOM.innerHTML;
			} else {
				//probably Firefox
				MochiKit.DOM.swapDOM(curr,newDOM);
			}
		}
		$(myId).scrollTop = scrollPos;
	} catch(err) {
		//we might be catching an XML parsing error
		MochiKit.Logging.logError(err);
		MochiKit.Logging.logError(err.message);
		if (resXML.parseError) {
			MochiKit.Logging.logDebug('xml error:', resXML.parseError.errorCode);
			MochiKit.Logging.logDebug(resXML.parseError.reason);
			MochiKit.Logging.logDebug(resXML.parseError.line);
		}
	}
};

MochiKit.Redtide_ext.__new__ = function() {
	var m = MochiKit.Base;
	m.nameFunctions(this);
	this.EXPORT_TAGS = {
		":common":this.EXPORT,
		":all": m.concat(this.EXPORT, this.EXPORT_OK)
	};
};

MochiKit.Redtide_ext.EXPORT = [
    "swapFromHttp",
    "GetPageScroll",
    "GetPageSize",
];

MochiKit.Redtide_ext.EXPORT_OK = [
	"Base",
	"PAIRS"
];

MochiKit.Redtide_ext.__new__();
MochiKit.Base._exportSymbols(this, MochiKit.Redtide_ext);
