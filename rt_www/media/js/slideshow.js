"use strict";

/* slideshow code modified from Jon Raasch's Simple JQuery Slideshow
	http://jonraasch.com/blog/a-simple-jquery-slideshow
*/
RedTide.slideshow = (function () {
	function init() {
		$(function(){
			setInterval("RedTide.slideshow.slideSwitch()", 5000 );
		});
	}
	
	function slideSwitch() {
		var $active = $('#homeslides .active');
		var $next =  $active.next().length ? $active.next()
		        : $('#homeslides img:first'); 
		
		$active.addClass('last-active');
		$next.css({opacity: 0.0})
			.addClass('active')
			.animate({opacity: 1.0}, 1000, function() {
				$active.removeClass('active last-active');
			});
		
	}
	
	return { 
		init: init,
		slideSwitch: slideSwitch
	};
})();

$(document).ready(RedTide.slideshow.init);