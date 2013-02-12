/*

<div>
  <ul>
  {% for video in object_list %}
    <li id="video_{{ video.id }}"><a href="javascript:loadFile({file:'{{ video.get_video }}', title:'{{ video.title }}', image:'{{ video.get_thumb }}'})">{{ video.title }}</a></li>
  {% endfor %}
  </ul>             
</div>


// in gallery div
{% for video in object_list %}
  <div class="videocell" id="video_{{ video.id }}">
    {{ video.title }}<br/>
    <a href="javascript:loadFile({file:'{{ video.get_video }}', title:'{{ video.title }}', image:'{{ video.get_thumb }}'})">
      <img src="{{ video.get_thumb }}" width="165" height="125">
    </a></li>
{% endfor %}

// VIDEO
    <div id="title" class="redline">{{ object.title }}</div>
    <div id="main" class="highlightbox">
        <p id="video" style="text-align: center;"><a href="http://www.macromedia.com/go/getflashplayer">
            Get the Flash Player</a> to see this player.</p>
    </div>     
<script type="text/javascript">
    var s1 = new SWFObject("/media/flash/flvplayer.swf","mpl","320","240","7");
    s1.addParam("allowfullscreen","true");
    s1.addVariable("file","{{ object.get_video }}");
    s1.addVariable("image", "{{ object.get_thumb }}");
    s1.addVariable("enablejs", "true");
    s1.addVariable("javascriptid", "mpl");
    s1.write("video");
</script>
<br class="clearme"/>
*/

"use strict";

RedTide.Videos = (function() {
    
	function init() {
		console.info("init videos");
		jQuery('.videocell a').prettyPhoto({
			title: this.title,
			file: this.file,
			href: "/media/flash/flvplayer.swf",
			width: "320",
			height: "240"
		});
	};
	
    function loadFile(obj) { 
        //swapDOM('title', DIV({'id':'title', 'class':'redline'}, obj.title)); 
        //thisMovie("mpl").loadFile(obj); 
    };

	return {
		init: init
	};

})();

jQuery(function() {
	RedTide.Videos.init();
});