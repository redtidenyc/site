"use strict";

/* slideshow code modified from Jon Raasch's Simple JQuery Slideshow
	http://jonraasch.com/blog/a-simple-jquery-slideshow
*/
RedTide.slideshow = (function () {
	
	var startSlides = null;
	function init() {
		$(function(){
			startSlides = setInterval("RedTide.slideshow.slideSwitch()", 5000 );
		});
		
		$(".forward").click(function() {
			if ($(this).hasClass("on")) {
				slideSwitch();
			}
			return false;
		});
		
		$(".back").click(function() {
			if ($(this).hasClass("on")) {
				slideSwitch($('#homeslides .active').index() - 1 );
			}
			return false;
		});
	}
	
	function slideSwitch(index) {
		clearInterval(startSlides);
		$("#homeslides .loading").animate({opacity: 0.0}, 1000);
		var $active = $('#homeslides .active');
		var $active_bullet = $('#slide_controls ul li.active');
		
		var $next, $next_bullet ;
		
		if (index) {
			
			$next =  $('#homeslides img.slide').eq(index - 1);
			$next_bullet = $('#slide_controls ul li').eq(index - 1);
		} else {
			$next =  $active.next().length ? $active.next()
			        : $('#homeslides img.slide:first');
			$next_bullet = $active_bullet.next().length ? $active_bullet.next() : $('#slide_controls ul li:first');
		}
		
		
		$active.addClass('last-active');
		$next.css({opacity: 0.0})
			.addClass('active')
			.animate({opacity: 1.0}, 1000, function() {
				$active.removeClass('active last-active');
			});
		$next_bullet.addClass('active');
		$active_bullet.removeClass('active');
		if ($next.index() > 1) {
			$(".back").addClass('on');
		} else {
			$(".back").removeClass('on');
		}
		
		if ($next.index() === 8) {
			$(".forward").removeClass('on');
		} else {
			$(".forward").addClass('on');
		}
		
		startSlides = setInterval("RedTide.slideshow.slideSwitch()", 5000 );
		
	}
	
	return { 
		init: init,
		slideSwitch: slideSwitch
	};
})();

$(document).ready(RedTide.slideshow.init);