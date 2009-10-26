addLoadEvent(function() {
    var tareas = getElementsByTagAndClassName('textarea', null);
    for(var i = 0; i < tareas.length; i++) {
        if(typeof(tareas[i].id) != 'undefined') { 
            var oFCKeditor = new FCKeditor( tareas[i].id ) ;
            oFCKeditor.BasePath = "/media/js/fckeditor/" ;
            oFCKeditor.Width = "80%";
            oFCKeditor.Height = "500";
            oFCKeditor.Config["CustomConfigurationsPath"] = "/media/js/fckeditor/admin_config.js" ;
            oFCKeditor.ReplaceTextarea() ;
        }
    }
});
