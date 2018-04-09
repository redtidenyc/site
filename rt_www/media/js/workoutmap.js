"use strict";

RedTide.MapManager = (function() {
	function init() {
		console.info("init map manager");
		
		var jjLatLng = new google.maps.LatLng(40.769865, -73.988024);
		var jjMapOptions = {
			center: jjLatLng,
			zoom: 15,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		var jjmap = new google.maps.Map(document.getElementById("jjmap"),
			jjMapOptions);
			
		var jjmarker = new google.maps.Marker({
			    position: jjLatLng,
			    title:"John Jay"
			});

		// To add the marker to the map, call setMap();
		jjmarker.setMap(jjmap);
			
		var barLatLng = new google.maps.LatLng(40.740577, -73.983957);
		var barMapOptions = {
				center: barLatLng,
				zoom: 15,
				mapTypeId: google.maps.MapTypeId.ROADMAP
			};
		var barmap = new google.maps.Map(document.getElementById("barmap"),
				barMapOptions);
				
		var barmarker = new google.maps.Marker({
		    position: barLatLng,
		    title:"Baruch"
		});
		
		barmarker.setMap(barmap);
		
		var ymcaLatLng = new google.maps.LatLng(40.723724, -73.992669)
		var ymcaMapOptions = {
				center: ymcaLatLng,
				zoom: 15,
				mapTypeId: google.maps.MapTypeId.ROADMAP
			};
		var ymcamap = new google.maps.Map(document.getElementById("ymcamap"),
				ymcaMapOptions);
				
		var ymcamarker = new google.maps.Marker({
		    position: ymcaLatLng,
		    title:"Baruch"
		});

		ymcamarker.setMap(ymcamap);
		/*
			var rooseveltpoint = new GLatLng(40.75699374459088, -73.95562648773193);
			this.rooseveltmap = new GMap2($('rooseveltmap'), { 'size': msize}) ;
			this.rooseveltmap.setCenter(rooseveltpoint, 15) ;
			this.rooseveltmap.addOverlay(new GMarker(this.rooseveltmap.getCenter()));
		*/
		var sacredLatLng = new google.maps.LatLng(40.782952,-73.9579644);
		var sacredMapOptions = {
			center: sacredLatLng,
			zoom: 15,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		var sacredmap = new google.maps.Map(document.getElementById("sacredmap"),
			sacredMapOptions);
			
		var sacredmarker = new google.maps.Marker({
			    position: sacredLatLng,
			    title:"Convent of the Sacred Heart School"
			});

		// To add the marker to the map, call setMap();
		sacredmarker.setMap(sacredmap);
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
