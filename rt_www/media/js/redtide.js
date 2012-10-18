"use strict";

var RedTide = (function () {
	function init() {
		setActiveNavTab();
	}
	
	// set the correct tab as active
	function setActiveNavTab() {	
		var i = 0;
		if($("#tabnav")) {
			$("#tabnav a").each(function() {
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