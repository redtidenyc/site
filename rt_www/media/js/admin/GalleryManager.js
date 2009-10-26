/* This is to manage galleries via the admin.  I was initially going to use drag and drop but it's too much of a pain 
 *
 */

GalleryAdministrator = function() {
	bindMethods(this);
}

GalleryAdministrator.prototype.initialize = function() {
	connect('chooseall', 'onclick', this, 'ChooseAll');
	connect('clearall', 'onclick', this, 'ClearAll');
        var avail_lis = getElementsByTagAndClassName('li', null, 'available');
	for( var i = 0; i < avail_lis.length; i++) {
		connect(avail_lis[i], 'onclick', this, 'MarkSelected');
	}

	var chosen_lis = getElementsByTagAndClassName('li', null, 'chosen');
	for( var i = 0; i < chosen_lis.length; i++) {
		connect(chosen_lis[i], 'onclick', this, 'MarkSelected');
	}
	connect('add_selected', 'onclick', this, 'MoveChosen');	
	connect('remove_selected', 'onclick', this, 'MoveAvailable');
	connect('galleryform', 'onsubmit', this, 'SubmitImageAssociations');
	MochiKit.Sortable.create('chosen');
}

GalleryAdministrator.prototype.SubmitImageAssociations = function(e) {
	var form = $('galleryform');
	
	/* associate images to this gallery */
	var value = '';
	var lis_to_keep = getElementsByTagAndClassName('li', null, 'chosen');
	for(var i = 0; i < lis_to_keep.length; i++) {
		value += lis_to_keep[i].id + ',';
	}
	appendChildNodes(form, INPUT({'type':'hidden', 'name':'keep_ims', 'value':value}));
	
	/* these we disassocate */
	value = '';
	var lis_to_disassoc = getElementsByTagAndClassName('li', null, 'available');
	for(var i = 0; i < lis_to_disassoc.length; i++) {
		value += lis_to_disassoc[i].id + ',';
	}	
	appendChildNodes(form, INPUT({'type':'hidden', 'name':'disassoc_ims', 'value':value}));
}

GalleryAdministrator.prototype.MoveTo = function(from, classname, to) {
	var lis = getElementsByTagAndClassName('li', classname, from);
	for(var i = 0; i < lis.length; i++) {
		lis[i] = removeElement(lis[i]);
		removeElementClass(lis[i], 'selected');
		appendChildNodes(to, lis[i]);
	}
	MochiKit.Sortable.destroy('chosen');
	MochiKit.Sortable.create('chosen');
}

GalleryAdministrator.prototype.ChooseAll = function(e) {
	this.MoveTo('available', null, 'chosen');
}

GalleryAdministrator.prototype.ClearAll = function(e) {
	this.MoveTo('chosen', null, 'available');	
}

GalleryAdministrator.prototype.MoveChosen = function(e) {
	this.MoveTo('available', 'selected', 'chosen');	
}

GalleryAdministrator.prototype.MoveAvailable = function(e) {
	this.MoveTo('chosen', 'selected', 'available');	
}

GalleryAdministrator.prototype.MarkSelected = function(e) {
	var li = e.src();
	if(hasElementClass(li, 'selected')) {
		removeElementClass(li, 'selected');
	} else {
		addElementClass(li, 'selected');
	}
}

galleryAdministrator = new GalleryAdministrator();
addLoadEvent(galleryAdministrator.initialize);
