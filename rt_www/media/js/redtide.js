"use strict";

var RedTide = (function () {
	function init() {
		setActiveNavTab();
	}
	
	// set the correct tab as active
	function setActiveNavTab() {	
		
		var section = jQuery("#main").attr("section");
		
		if (section)
			jQuery("#tabnav a:contains('" + section.toUpperCase() + "')").addClass("active");
		
		
		if(jQuery(".subleft")) {
			jQuery(".subleft ul li a").each(function() {
				if(jQuery(this).attr("href") == location.pathname) {
					jQuery(this).addClass("active");
				}
			});
		}
	}
	
	return { 
		init: init
	};
})();

jQuery(document).ready(RedTide.init);