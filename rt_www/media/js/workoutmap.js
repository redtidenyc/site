"use strict";

RedTide.MapManager = (function() {
	function init() {
		console.info("init map manager");
	}
	
	return {
		init: init
	}
})();


$(document).ready(function() {
	RedTide.MapManager.init();
});

/*MapManager = function() {
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
		var rooseveltpoint = new GLatLng(40.75699374459088, -73.95562648773193);
		this.rooseveltmap = new GMap2($('rooseveltmap'), { 'size': msize}) ;
		this.rooseveltmap.setCenter(rooseveltpoint, 15) ;
		this.rooseveltmap.addOverlay(new GMarker(this.rooseveltmap.getCenter()));
	}
}

mapManager = new MapManager();
addLoadEvent(mapManager.initialize);
*/
