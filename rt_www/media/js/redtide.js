"use strict";

var RedTide = (function () {
	function init() {
		if (typeof MochiKit === 'undefined')
			setActiveNavTab();
	}
	
	// set the correct tab as active
	function setActiveNavTab() {	
		
		var section = $("#main").attr("section");
		
		if (section)
			$("#tabnav a:contains('" + section.toUpperCase() + "')").addClass("active");
		
		
		if($(".subleft")) {
			$(".subleft ul li a").each(function() {
				if($(this).attr("href") == location.pathname) {
					$(this).addClass("active");
				}
			});
		}
	}
	
	return { 
		init: init
	};
})();

$(document).ready(RedTide.init);