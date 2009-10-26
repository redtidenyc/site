function ShowSelectBoxes() {
	var selects = MochiKit.DOM.getElementsByTagAndClassName('select');
	for(var i = 0; i < selects.length; i++) {
		setStyle(selects[i], {'visibility':'visible'});
	}
}

function HideSelectBoxes() {
	var selects = MochiKit.DOM.getElementsByTagAndClassName('select');
	for(var i = 0; i < selects.length; i++) {
		setStyle(selects[i], {'visibility':'hidden'});
	}
}
