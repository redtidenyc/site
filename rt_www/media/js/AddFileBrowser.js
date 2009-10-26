FileBrowser = function() {
	bindMethods(this);
};

FileBrowser.prototype.initialize = function() {
	this.admin_media_prefix = '';
	this.no_thumb = '/media/img/no_thumb.gif';
	var help = getElementsByTagAndClassName('p', 'help');
	for (var i=0; i<help.length; i++) {
		// check if p contains the text "FileBrowser"
		if (scrapeText(help[i]).substr(0,11) == "FileBrowser") {
			this.AddFileBrowseField(help[i]);
		}
	}
}


FileBrowser.prototype.Show = function(e) {
	var href = "/admin/filebrowser" + this.helpPath + "?pop=1";
	log(' In show ' + this.inputfield_id); 
        FBWindow = window.open(href, this.inputfield_id, 'height=600,width=840,resizable=yes,scrollbars=yes');
        FBWindow.focus();
}

FileBrowser.prototype.GetThumb = function(imgSRC) {
	newImg = "";
	if (imgSRC) {
		imgtemp = imgSRC.split("/");
		imglength = imgtemp.length - 1;
		newimgSRC = 'tn_' + imgtemp[imglength];
		newImg = imgSRC.replace(imgtemp[imglength], newimgSRC);
		img_temp = new Image();
		img_temp.src = newImg;
		if (!img_temp.width) { newImg = this.no_thumb; }
	}
	return newImg;
}

FileBrowser.prototype.GetHelpPath = function(helpnode) {
	var text = scrapeText(helpnode);
	if (text.indexOf('/') >= 11) {
		helpPath = text.substr(text.indexOf('/'));
	} else {
		helpPath = '/media';
        }
	return helpPath;
}

FileBrowser.prototype.FieldChange = function(e) {
	log(e.src());
	var inputfield = $(this.inputfield_id);
	if (inputfield.value == "") {
		inputfield.parentNode.lastChild.setAttribute('style', 'display: none;');
	} else {
		imgSRC = inputfield.value;
		newImg = this.getThumb(imgSRC);
		inputfield.parentNode.lastChild.firstChild.setAttribute('src', newImg);
		inputfield.parentNode.lastChild.setAttribute('style', 'display: block;');
	}
}

FileBrowser.prototype.AddFileBrowseField = function(help) {
	// check if there's an image in the input-field before the help_text
	imgSRC = help.previousSibling.previousSibling.value;
	newImg = this.GetThumb(imgSRC);
        
	// FileBrowser: Path
        this.helpPath = this.GetHelpPath(help);
        // Link to FileBrowser (search_icon)
        this.inputfield_id = help.previousSibling.previousSibling.getAttribute('id');
	log(this.inputfield_id);
	connect(this.inputfield_id, 'onchange', this, 'FieldChange');
        var fb_link = A({'id':'fblink_' + this.inputfield_id, 'href':'javascript:void(0);'},
			IMG({'src':'/media/img/icon_search.png'}));
	appendChildNodes(help.parentNode, fb_link);
	connect('fblink_' + this.inputfield_id, 'onclick', this, 'Show');
        // Image Preview
	var img_preview = P({'class':'help'}, IMG({'src':newImg, 'id':'image_' + this.inputfield_id}));
        if (newImg == "") {
		setStyle(img_preview, {'display':'none'})
	} else {
		setStyle(img_preview, {'display':'block'});
        }
	appendChildNodes(help.parentNode, img_preview);
        // add on change handle for input_fields
        // remove help_text
        help.parentNode.removeChild(help);

}

fileBrowser = new FileBrowser();
addLoadEvent(fileBrowser.initialize);
