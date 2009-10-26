MapManager = function() {
	bindMethods(this);
}

MapManager.prototype.initialize = function() {
	var jdim = getElementDimensions('jjmap');
        var bdim = getElementDimensions('barmap');
	
	if(GBrowserIsCompatible()) {
		var msize = new GSize(jdim.w, jdim.h);
		this.jjmap = new GMap2($('jjmap'), { 'size':msize });
		var jjpoint = new GLatLng(40.769865, -73.988024);
		this.jjmap.setCenter(jjpoint, 15);
		this.jjmap.addOverlay(new GMarker(this.jjmap.getCenter()));
		msize = new GSize(bdim.w, bdim.h);
		var barpoint = new GLatLng(40.740577, -73.983957); 
		this.barmap = new GMap2($('barmap'), { 'size':msize });
		this.barmap.setCenter(barpoint, 15);
		this.barmap.addOverlay(new GMarker(this.barmap.getCenter()));
		var ymcapoint = new GLatLng(40.723724, -73.992669); 
		this.ymcamap = new GMap2($('ymcamap'), { 'size': msize}) ;
		this.ymcamap.setCenter(ymcapoint, 15) ;
		this.ymcamap.addOverlay(new GMarker(this.ymcamap.getCenter()));
	}
}

mapManager = new MapManager();
addLoadEvent(mapManager.initialize);
