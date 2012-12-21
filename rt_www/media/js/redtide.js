"use strict";

var RedTide = (function () {
	function init() {
		setActiveNavTab();
	}
	
	// set the correct tab as active
	function setActiveNavTab() {	
		
		var section = $("#main").attr("section").toUpperCase();
		console.info("section: " + section);
		$("#tabnav a:contains('" + section + "')").addClass("active");
		
		
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