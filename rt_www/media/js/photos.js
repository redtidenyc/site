/*
	Control flow for the gallery manager is going to go like this.  On page load it calls back to 
	the server and get a list of the first ten gallerys.

 */
GalleryManager = function() {
	bindMethods(this);
};

GalleryManager.prototype.Errhandler = function(e) {
	console.info(e);
};

GalleryManager.prototype.initialize = function() {
	this.current_page = 0;
	this.limit = 16;
        this.servicesproxy = new JsonRpcProxy('http://' + location.host + '/services/photogallery/', 
            ['gallery_view', 'gallery_details']); 
	var def = this.servicesproxy.gallery_view('0', this.limit);
	def.addCallback(this.PageBuild);
	def.addErrback(this.Errhandler);
	var def2 = this.servicesproxy.gallery_details('0', this.limit);
	def2.addCallback(this.CacheBuild);
	def2.addErrback(this.Errhandler);
	this.image_cache = {};
	this.gallery_title_cache = {};
	this.imageArray = new Array;
	this.activeImage;
	this.resizeSpeed = 7;
	this.borderSize = 10;
	if(this.resizeSpeed > 10){ 
		this.resizeSpeed = 10;
	}
	if(this.resizeSpeed < 1){ 
		this.resizeSpeed = 1;
	}
	this.resizeDuration = (11 - this.resizeSpeed) * 0.15;
	this.BuildImageHtml();
}

GalleryManager.prototype.ChangeImage = function(imageNum) {
	this.activeImage = imageNum;
	showElement('loading');
	hideElement('lightboxImage');
	hideElement('hoverNav');
	hideElement('prevLink');
	hideElement('nextLink');
	hideElement('imageDataContainer');
	hideElement('numberDisplay');
	var _this = this;
	imgPreloader = new Image();
	imgPreloader.onload = function(){ 
		setNodeAttribute('lightboxImage', 'src', _this.imageArray[_this.activeImage].url); 
		galleryManager.ResizeImageContainer(imgPreloader.width, imgPreloader.height);
	}
	imgPreloader.src = this.imageArray[this.activeImage].url;	
}

GalleryManager.prototype.ResizeImageContainer = function(imgWidth, imgHeight) {
	// get current height and width
	var dim = elementDimensions('outerImageContainer');
	this.wCur = dim.w;
	this.hCur = dim.h;

	// scalars based on change from old to new
	this.xScale = ((imgWidth  + (this.borderSize * 2)) / this.wCur) * 100;
	this.yScale = ((imgHeight  + (this.borderSize * 2)) / this.hCur) * 100;

	// calculate size difference between new and old image, and resize if necessary
	wDiff = (this.wCur - this.borderSize * 2) - imgWidth;
	hDiff = (this.hCur - this.borderSize * 2) - imgHeight;

	if(!( hDiff == 0)){
		Scale('outerImageContainer', this.yScale, {scaleX: false, duration: this.resizeDuration, queue:'front' }); 
	}
	if(!( wDiff == 0)){ 
		Scale('outerImageContainer', this.xScale, {scaleY: false, delay: this.resizeDuration, duration: this.resizeDuration}); 
	}

	// if new and old image are same size and no scaling transition is necessary, 
	// do a quick pause to prevent image flicker.
	if((hDiff == 0) && (wDiff == 0)){
		if (navigator.appVersion.indexOf("MSIE")!=-1){ 
			pause(250); 
		} else { 
			pause(100);
		} 
	}
	var dcontainer_width = imgWidth + ( this.borderSize * 2);
	setStyle('prevLink', { 'height':imgHeight + 'px' });
	setStyle('nextLink', { 'height':imgHeight + 'px' });
	setStyle('imageDataContainer', { 'width':dcontainer_width + 'px' });

	this.ShowImage();
}

GalleryManager.prototype.ShowImage = function() {
	hideElement('loading');
	appear('lightboxImage', { duration: 0.5, queue: 'end', afterFinish: this.UpdateDetails });
}

GalleryManager.prototype.UpdateDetails = function() {
	showElement('caption');
	replaceChildNodes('caption', this.imageArray[this.activeImage].title);
		
		// if image is part of set display 'Image x of x' 
	if(this.imageArray.length > 1){
		showElement('numberDisplay');
		replaceChildNodes('numberDisplay', "Image " + eval(this.activeImage + 1) + " of " + this.imageArray.length);
	}

	Parallel(
		[ slideDown( 'imageDataContainer', { sync: true, duration: this.resizeDuration + 0.25, from: 0.0, to: 1.0 }), 
		appear('imageDataContainer', { sync: true, duration: 1.0 }) ],  { duration: 0.65, afterFinish: this.UpdateNav } 
	);

}

GalleryManager.prototype.Start = function(gid) {
	
    var arrayPageSize = GetPageSize();
    var pagedim = { 'w':arrayPageSize[0], 'h':arrayPageSize[1] };
    setElementDimensions('overlay', pagedim);
    appear('overlay', { 'from':0.0, 'to':0.8 });
	

    this.imageArray = this.image_cache[gid];
    var def  = maybeDeferred(this.LoadImages);
    swapDOM('tcaption', SPAN({'id':'tcaption'}, this.gallery_title_cache[gid]));
    arrayPageSize = GetPageSize();
    var arrayPageScroll = GetPageScroll();
    var lightboxTop = arrayPageScroll[1] + (arrayPageSize[3] / 15);
    console.info(lightboxTop);
    setStyle('lightbox', { 'top':lightboxTop + 'px' });
    showElement('lightbox');
		
    this.ChangeImage(0);
	
}

GalleryManager.prototype.LoadImages = function() {
    for(var i = 0; i < this.imageArray.length; i++) {
        preloadImage = new Image();
	preloadImage.src = this.imageArray[i].url;
    }
}

GalleryManager.prototype.KeyboardAction = function(e) {
    var keycode = e.key().code;
    var kstring = e.key().string;
    key = String.fromCharCode(keycode).toLowerCase();
    if((key == 'x') || (key == 'o') || (key == 'c') || (key == 'q')){	// close lightbox
        this.End();
    } else if(key == 'p' || kstring == 'KEY_ARROW_LEFT' ){	// display previous image
        if(this.activeImage != 0){
	    this.DisableKeyboardNav();
	    this.ChangeImage(this.activeImage - 1);
	}
    } else if(key == 'n' || kstring == 'KEY_ARROW_RIGHT' ){	// display next image
	if(this.activeImage != (this.imageArray.length - 1)){
	    this.DisableKeyboardNav();
	    this.ChangeImage(this.activeImage + 1);
	}
    }
}

GalleryManager.prototype.DecrImage = function(e) {
    this.ChangeImage(this.activeImage - 1);
    return false;
}

GalleryManager.prototype.IncrImage = function(e) {
    this.ChangeImage(this.activeImage + 1);
    return false;
}

GalleryManager.prototype.UpdateNav = function() {
    showElement('hoverNav');				
    // if not first image in set, display prev image button
    if(this.activeImage != 0){
        showElement('prevLink');
	document.getElementById('prevLink').onclick = function() {
	    galleryManager.DecrImage(); return false;
	}
    }

    // if not last image in set, display next image button
    if(this.activeImage < (this.imageArray.length - 1)){
        showElement('nextLink');
	document.getElementById('nextLink').onclick = function() {
	    galleryManager.IncrImage(); return false;
	}
    } 

    this.EnableKeyboardNav();	
}

GalleryManager.prototype.DisableKeyboardNav = function() {
    var objBody = getFirstElementByTagAndClassName('body');
    disconnectAll(objBody, 'onkeydown');
}

GalleryManager.prototype.EnableKeyboardNav = function() {
    var objBody = getFirstElementByTagAndClassName('body');
    connect(objBody, 'onkeydown', this, 'KeyboardAction');
}

GalleryManager.prototype.End = function(e) {
    this.DisableKeyboardNav();
    hideElement('lightbox');
    fade('overlay', {'duration':0.2});
}

GalleryManager.prototype.BuildImageHtml = function() {
    var objBody = getFirstElementByTagAndClassName('body');
    var res = TrimPath.processDOMTemplate("lightbox_template", {});
    var objOverlay = DIV({'id':'overlay', 'style':'display: none;'});
    insertSiblingNodesBefore('container', objOverlay);
    connect('overlay', 'onclick', this, 'End');

    objBody.innerHTML = res + objBody.innerHTML;
	
    connect('loadingLink', 'onclick', this, 'End');
    connect('bottomNavClose', 'onclick', this, 'End');
}

GalleryManager.prototype.CacheBuild = function(req) {
    for( var gid in req ) {
        this.image_cache[gid] = req[gid];
    }
}

/*
	Four galleries per row
 */

GalleryManager.prototype.PageBuild = function(req) {
    this.total = req.count;
    this.total_gallery_pages = Math.floor(this.total / 16);
    this.current_page += 1;
    if(this.total%16 > 0) 
        this.total_gallery_pages += 1;
        
    var rows = new Array();
    var row = new Array();       
    var rcount = 0;
    var ids = new Array();
    var i = 0;
    for(; i < req.list.length; i++ ) {
        var gallery = req.list[i];
	this.gallery_title_cache[gallery.gid] = gallery.title;
        if( i > 0 && i % 4 == 0) { rows[rcount] = row; rcount++; row = new Array(); }

        row[i%4] = { title : gallery.title, loc : gallery.thumburl, gid : gallery.gid };
        ids[i] = gallery.gid;
    }


    if(i%4>0) { while(i%4 > 0) { row[i%4] = { title : '', loc : '', gid : '' }; i++; } }
    rows[rcount] = row;
        
    var data = { rows : rows, next : false, prev : false, total : this.total_gallery_pages, pageno : this.current_page };

    if(this.current_page < this.total_gallery_pages) {
        data.next = true;
    }

    if(this.current_page > 1) {
        data.prev = true; 
    }
    
    var result = TrimPath.processDOMTemplate("photo_table", data);

    $('gallery').innerHTML = result;

    for(i = 0; i < ids.length; i++) { connect('gallery' + ids[i], 'onclick', this, 'ShowGallery'); }
	
    if(this.current_page < this.total_gallery_pages) {
        connect('next_galleries', 'onclick', this, 'NextGalleryPage');	
    }

    if(this.current_page > 1) {
        connect('prev_galleries', 'onclick', this, 'PrevGalleryPage');
    }
}

GalleryManager.prototype.NextGalleryPage = function(e) {
	var def = this.serviceproxy.gallery_view(this.current_page*this.limit, this.limit);
	def.addCallback(this.PageBuild);
	def.addErrback(this.Errhandler);
	var def2 = this.servicesproxy.gallery_details(this.current_page*this.limit, this.limit);
	def2.addCallback(this.CacheBuild);
	def2.addErrback(this.Errhandler);
}

GalleryManager.prototype.PrevGalleryPage = function(e) {
	this.current_page -= 1;
	var def = this.servicesproxy.gallery_view((this.current_page-1)*this.limit, this.limit);
	def.addCallback(this.PageBuild);
	def.addErrback(this.Errhandler);
	var def2 = this.servicesproxy.gallery_details((this.current_page-1)*this.limit, this.limit);
	def2.addCallback(this.CacheBuild);
	def2.addErrback(this.Errhandler);	
}

GalleryManager.prototype.ShowGallery = function(e) {
	var gid = e.src().id.replace(/gallery(\d+)/, "$1");
	console.info(gid);
        this.Start(gid);
}

//
// pause(numberMillis)
// Pauses code execution for specified time. Uses busy code, not good.
// Code from http://www.faqts.com/knowledge_base/view.phtml/aid/1602
//
function pause(numberMillis) {
	var now = new Date();
	var exitTime = now.getTime() + numberMillis;
	while (true) {
		now = new Date();
		if (now.getTime() > exitTime)
			return;
	}
}


galleryManager = new GalleryManager();
addLoadEvent(galleryManager.initialize);
