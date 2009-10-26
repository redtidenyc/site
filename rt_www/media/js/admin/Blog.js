addLoadEvent(function() {
    var oFCKeditor = new FCKeditor( 'id_text' ) ;
    oFCKeditor.BasePath = "/media/js/fckeditor/" ;
    oFCKeditor.Width = "80%";
    oFCKeditor.Config["CustomConfigurationsPath"] = "/media/js/fckeditor/admin_config.js" ;
    oFCKeditor.ReplaceTextarea() ;
        
    var remote_autocompleter = new AutoComplete.Remote('id_author', 'autocompleter_choices', '/adminservices/swimmers/', 
	{'minChars':1, 'css':'/media/css/autocomplete.css', 
         'updateElement':'addItemToList', 'input_class':'vTextField', 'method':'get_swimmers' });
    remote_autocompleter.initialize()
});
