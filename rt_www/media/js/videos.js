/*
	Control flow for the video manager is going to go like this.  On page load it calls back to 
	the server and get a list of the first ten videos.

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
        this.servicesproxy = new JsonRpcProxy('http://' + location.host + '/services/videos/', 
            ['gallery_view']); 
	var def = this.servicesproxy.gallery_view('0', this.limit);
	def.addCallback(this.PageBuild);
	def.addErrback(this.Errhandler);
/*	this.image_cache = {};
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
	this.BuildImageHtml();*/
}

/*
	Three galleries per row
 */

GalleryManager.prototype.PageBuild = function(req) {
    this.total = req.count;
    this.total_gallery_pages = Math.floor(this.total / 12);
    this.current_page += 1;
    if(this.total%12 > 0) 
        this.total_gallery_pages += 1;
        
    var rows = new Array();
    var row = new Array();       
    var rcount = 0;
    var ids = new Array();
    var i = 0;
    for(; i < req.list.length; i++ ) {
        var gallery = req.list[i];
	this.gallery_title_cache[gallery.gid] = gallery.title;
        if( i > 0 && i % 3 == 0) { rows[rcount] = row; rcount++; row = new Array(); }

        row[i%4] = { title : gallery.title, loc : gallery.thumburl, gid : gallery.gid };
        ids[i] = gallery.gid;
    }


    if(i%3>0) { while(i%3 > 0) { row[i%4] = { title : '', loc : '', gid : '' }; i++; } }
    rows[rcount] = row;
        
    var data = { rows : rows, next : false, prev : false, total : this.total_gallery_pages, pageno : this.current_page };

    if(this.current_page < this.total_gallery_pages) {
        data.next = true;
    }

    if(this.current_page > 1) {
        data.prev = true; 
    }
    
    var result = TrimPath.processDOMTemplate("video_table", data);

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
