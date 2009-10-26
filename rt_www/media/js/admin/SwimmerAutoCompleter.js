addLoadEvent(function() {

	var remote_autocompleter = new AutoComplete.Remote('id_swimmer', 'autocompleter_choices', '/adminservices/swimmers/', 
		{'minChars':1, 'css':'/media/css/autocomplete.css', 
                 'updateElement':'addItemToList', 'input_class':'vTextField', 'method':'get_swimmers' });
	remote_autocompleter.initialize()
});
