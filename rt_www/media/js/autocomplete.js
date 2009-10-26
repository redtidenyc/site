/*
 *  This is a port of the scriptaculous autocomplete widget to MochiKit.
 *
 *
 *
 */


/*
 * The constructor takes the id of the text field, the id of the div to populate
 */

var KEY_BACKSPACE = 8;
var KEY_TAB =       9;
var KEY_RETURN =   13;
var KEY_ESC =      27;
var KEY_LEFT =     37;
var KEY_UP =       38;
var KEY_RIGHT =    39;
var KEY_DOWN =     40;
var KEY_DELETE =   46;

AutoComplete = function() {
	bindMethods(this);
}

AutoComplete.prototype.base_initialize = function(element, update, options) {
        /* load our css */
        var css_dom = createDOM('link', {'rel':'stylesheet', 'type':'text/css', 'href':options.css});
        var head = getFirstElementByTagAndClassName('head');
        appendChildNodes(head, css_dom);
	if(typeof(element) == 'string') {
		this.text_element = $(element);
	} else {
		this.text_element = element;
	}

        if(this.text_element == null) {
            //then we shutdown
            return;
        }

        /* This first thing we do is check that the incoming element is a input type=text element
        If not we replace it with one */
        var new_id = this.text_element.id;
        var orig_value = this.text_element.value;
        var value = orig_value;
        if(this.text_element.localName == 'SELECT') {
            value = this.text_element.options[this.text_element.selectedIndex].text;
        }
        var widget = INPUT({"type":"text", "name":new_id, "class":options.input_class, "value":value, "id":new_id});
        swapDOM(this.text_element, widget);
        this.text_element = widget;
	this.element = new_id;
        /* We stick this above the */
	var id = new_id;
	var hidden_id = this.text_element.id.replace(/^id_/, ''); 
	this.hidden_input = $(hidden_id);
        if(this.hidden_input == null) {
            this.hidden_input = INPUT({'id':hidden_id, 'name':hidden_id, 'type':'hidden', 'value':orig_value});
            insertSiblingNodesAfter(this.text_element, this.hidden_input);
        }
	
	if(typeof(update) == 'string') {
		this.update = $(update);
	} else {
		this.update = update;
	}

        if(this.update == null && typeof(update) == 'string' ) {
            this.update = DIV({'id':update, 'class':'autocomplete'});
            var body = getFirstElementByTagAndClassName('body'); 
            appendChildNodes(body, this.update);
        }

	this.changed     = false; 
	this.active      = false; 
	this.index       = 0;     
	this.entryCount  = 0;

	if(this.setOptions) {
		this.SetOptions(options);
	} else {
		this.options = options || {};
	}
	var _this = this;
	this.options.paramName    = this.options.paramName || this.element.name;
	this.options.tokens       = this.options.tokens || [];
	this.options.frequency    = this.options.frequency || 0.4;
	this.options.minChars     = this.options.minChars || 1;
	this.options.onShow       = this.options.onShow || 
		function(element, update){ 
			if(!update.style.position || update.style.position=='absolute') {
				update.style.position = 'absolute';
				_this.ClonePosition(element, update);
			}
        		appear(update,{duration:0.15});
		};
	this.options.onHide = this.options.onHide ||
		function(element, update) {
			fade(update, { duration:0.15});
		};
	if(typeof(this.options.tokens) == 'string') {
      		this.options.tokens = new Array(this.options.tokens);
	}

	this.observer = null;

	this.text_element.setAttribute('autocomplete','off');
	hideElement(this.update);
	connect(this.text_element, 'onblur', this, 'OnBlur');
	connect(this.text_element, 'onkeypress', this, 'OnKeyPress');
}

AutoComplete.prototype.CumulativeOffset = function(element) {
	var valueT = element.offsetHeight, valueL = 0;
	do {
		valueT += element.offsetTop || 0 ;
                valueL += element.offsetLeft || 0;
		element = element.offsetParent;
	} while (element);

	return [valueL, valueT];
}

AutoComplete.prototype.ClonePosition = function(source, target) {
	var source = $(source);
	var target = $(target);
	var offsets = this.CumulativeOffset(source);
	target.style.top    = offsets[1] + 'px';
	target.style.left   = offsets[0] + 'px';
	target.style.width  = source.offsetWidth + 'px';
}

AutoComplete.prototype.OnBlur = function(e) {
	// needed to make click events working
	setTimeout(bind(this.Hide, this), 250);
	this.hasFocus = false;
	this.active = false;
}

AutoComplete.prototype.OnKeyPress = function(e) {
	
	var key = 0;
	if(e.event() == null) {
		key = window.event.keyCode;
	} else {
		key = e.event().keyCode;
	}
	if(this.active) {
		switch(key) {
			case KEY_TAB: 
			case KEY_RETURN:
				this.SelectEntry();
				e.stop();
			case KEY_ESC:
				this.Hide();
				this.active = false;
				e.stop();
				return;
			case KEY_LEFT:
			case KEY_RIGHT:
				return;
			case KEY_UP:
				this.MarkPrevious();
				this.Render();
				if(navigator.appVersion.indexOf('AppleWebKit')>0)
					e.stop();
				return;
			case KEY_DOWN:
				this.MarkNext();
				this.Render();
				if(navigator.appVersion.indexOf('AppleWebKit')>0)
					e.stop();
				return;
		}
	} else {
		if(key == KEY_TAB || key == KEY_RETURN) 
			return;
	}
	this.changed = true;
	this.hasFocus = true;
	if(this.observer) {
		clearTimeout(this.observer);
	}
	this.observer =  setTimeout(bind(this.OnObserverEvent, this), this.options.frequency*1000);
	
}

AutoComplete.prototype.OnObserverEvent = function() {
	this.changed = false;   
	if(this.GetToken().length>=this.options.minChars) {
		this.StartIndicator();
		this.GetUpdatedChoices(); //This needs to be inheirated 
	} else {
		this.active = false;
		this.Hide();
	}
}

AutoComplete.prototype.GetToken = function() {
	var tokenPos = this.FindLastToken();
	if (tokenPos != -1) {
		var ret = this.text_element.value.substr(tokenPos + 1).replace(/^\s+/,'').replace(/\s+$/,'');
	} else {
		var ret = this.text_element.value;
	}

	return /\n/.test(ret) ? '' : ret;
}

AutoComplete.prototype.FindLastToken = function() {
	var lastTokenPos = -1;
	for (var i=0; i<this.options.tokens.length; i++) {
		var thisTokenPos = this.element.value.lastIndexOf(this.options.tokens[i]);
		if (thisTokenPos > lastTokenPos) {
			lastTokenPos = thisTokenPos;
		}    
	}
	return lastTokenPos;
}

AutoComplete.prototype.MarkPrevious = function() {
	if(this.index > 0) {
		this.index--;
	} else {
		this.index = this.entryCount-1;
	}

	this.GetEntry(this.index);
}

AutoComplete.prototype.MarkNext = function() {
	if(this.index < this.entryCount-1) {
		this.index++;
	} else {
		this.index = 0;
	}

	this.GetEntry(this.index);
}

AutoComplete.prototype.Render = function() {
	if(this.entryCount > 0) {
		for (var i = 0; i < this.entryCount; i++)
			this.index == i ? addElementClass(this.GetEntry(i), 'selected') : 
				removeElementClass(this.GetEntry(i), 'selected');
        
		if(this.hasFocus) { 
			this.Show();
			this.active = true;
		}
	} else {
		this.active = false;
		this.Hide();
    	}
}

AutoComplete.prototype.Show = function() {
	if(getStyle(this.update, 'display') == 'none'){
		this.options.onShow(this.text_element, this.update);
	}
	if(!this.iefix && (navigator.appVersion.indexOf('MSIE')>0) && (navigator.userAgent.indexOf('Opera')<0) && 
		(getStyle(this.update, 'position') == 'absolute')) {
		var iedom = createDOM('iframe', {
			'id':this.update.id + '_iefix', 
			'style':'display:none;position:absolute;filter:progid:DXImageTransform.Microsoft.Alpha(opacity=0);', 
			'scrolling':'no', 'src':'javascript:false', 'frameborder':'0'});
		appendChildNodes(this.update, iedom);
		this.iefix = $(this.update.id+'_iefix');
	}
	if(this.iefix){
		setTimeout(bind(this.fixIEOverlapping, this), 50);
	}
}

AutoComplete.prototype.FixIEOverLapping = function() {
	this.ClonePosition(this.update, this.iefix);
	this.iefix.style.zIndex = 1;
	this.update.style.zIndex = 2;
	showElement(this.iefix);
}

AutoComplete.prototype.Hide = function() {
	this.StopIndicator();
	if(getStyle(this.update, 'display') !='none'){ 
		this.options.onHide(this.element, this.update);
	}
	if(this.iefix){ 
		hideElement(this.iefix);
	}
}

AutoComplete.prototype.StopIndicator = function() {
	if(this.options.indicator) {
		hideElement(this.options.indicator);
	}
}

AutoComplete.prototype.StartIndicator = function() {
	if(this.options.indicator) {
		showElement(this.options.indicator);
	}
}

AutoComplete.prototype.SelectEntry = function() {
	this.active = false;
	this.UpdateElement(this.GetCurrentEntry());
}

AutoComplete.prototype.UpdateElement = function(selected_element) {
	/*if (this.options.updateElement) {
		this.options.updateElement(selected_element);
		return;
    	}*/

	var value = scrapeText(selected_element);
	this.hidden_input.value = selected_element.id;
	var lastTokenPos = this.FindLastToken();
	if (lastTokenPos != -1) {
		var newValue = this.text_element.value.substr(0, lastTokenPos + 1);
		var whitespace = this.text_element.value.substr(lastTokenPos + 1).match(/^\s+/);
		if (whitespace)
			newValue += whitespace[0];
		this.text_element.value = newValue + value;
	} else {
		this.text_element.value = value;
	}

	this.text_element.focus();
	if (this.options.afterUpdateElement) {
		this.options.afterUpdateElement(this.element, selected_element);
	}
}

AutoComplete.prototype.GetCurrentEntry = function() {
	return this.GetEntry(this.index);
}

AutoComplete.prototype.GetEntry = function(ind) {
	return this.update.firstChild.childNodes[ind];
}

AutoComplete.prototype.Activate = function() {
	this.changed = false;
	this.hasFocus = true;
	this.GetUpdatedChoices();
}

AutoComplete.prototype.OnHover = function(e) {
	var ev = e.event();
	var element = ev.target || ev.srcElement;
	while (element.parentNode && (!element.tagName || (element.tagName.toUpperCase() != 'LI'))) {
		element = element.parentNode;
	}

	if(this.index != element.autocompleteIndex) {
		this.index = element.autocompleteIndex;
		this.Render();
	}
	e.stop();
}

AutoComplete.prototype.OnClick = function(e) {
	var ev = e.event();
	var element = ev.target || ev.srcElement;
	while (element.parentNode && (!element.tagName || (element.tagName.toUpperCase() != 'LI'))) {
		element = element.parentNode;
	}	
	this.index = element.autocompleteIndex;
	this.SelectEntry();
	this.Hide();
}

/* The choices coming in are an array of hashes.  Each hash is a { 'id':id, 'value':value } pair
 *
 */

/* descendants: function(element) {
 * 	element = $(element);
 *	return $A(element.getElementsByTagName('*'));
 * }
 * 
 * down: function(element, expression, index) {
 *	return Selector.findElement($(element).descendants(), expression, index);
 * }
 *
 */

AutoComplete.prototype.UpdateChoices = function(choices) {
	
	if(!this.changed && this.hasFocus) {
		var list = UL({})
		for(var i = 0; i < choices.length; i++) {
			appendChildNodes(list, LI({'id':choices[i].id}, choices[i].value))
		}
		replaceChildNodes(this.update, list);
		removeEmptyTextNodes(this.update);
		removeEmptyTextNodes(this.update.firstChild);
		if(this.update.firstChild && this.update.firstChild.childNodes) {
			this.entryCount =  this.update.firstChild.childNodes.length;
			for (var i = 0; i < this.entryCount; i++) {
				var entry = this.GetEntry(i);
				entry.autocompleteIndex = i;
				this.AddObservers(entry);
			}
		} else { 
			this.entryCount = 0;
		}
		this.StopIndicator();
		this.index = 0;
		if(this.entryCount==1 && this.options.autoSelect) {
			this.SelectEntry();
			this.Hide();
		} else {
			this.Render();
		}
	}
}

AutoComplete.prototype.AddObservers = function(element) {
	connect(element, 'onmouseover', this, 'OnHover');	 
	connect(element, 'onclick', this, 'OnClick');
}

/* Inheiratance in javascript is so retarded.  Sheesh.  All power to Bob Ippolito!
 *
 */

AutoComplete.Remote = function(element, update, url, options) {
	bindMethods(this);
	this.e = element;
	this.update = update;
	this.options = options;
	this.adminproxy = new JsonRpcProxy('http://' + location.host + url, [ options.method ]);
}

AutoComplete.Remote.prototype.initialize = function() {
	update(this, AutoComplete.prototype);
	this.base_initialize(this.e, this.update, this.options);
	this.options.defaultParams = this.options.parameters || null;
}

AutoComplete.Remote.prototype.GetUpdatedChoices = function() {
	entry = encodeURIComponent(this.options.paramName) + '=' + encodeURIComponent(this.GetToken());
	this.options.parameters = this.options.callback ? this.options.callback(this.element, entry) : entry;
	if(this.options.defaultParams) {
		this.options.parameters += '&' + this.options.defaultParams;
	}
	var token = this.GetToken()
	this.deferred = eval('this.adminproxy.' + this.options.method + '(\'' + token + '\')');
	this.deferred.addCallback(this.OnComplete);
	this.deferred.addErrback(function(e) { log(e); });
}

AutoComplete.Remote.prototype.OnComplete = function(req) {
	this.UpdateChoices(req);
}
