/* This just adds in the thumbnail of the photo to tahe admin add page */

PhotoManager = function() {
    bindMethods(this);
}

PhotoManager.prototype.initialize = function() {
    var photo_num = location.href.replace(/^http:\/\/[\w.]+\/\w+\/\D+\/(\d+)\D+/, '$1'); 
    this.adminservices = new JsonRpcProxy('http://' + location.host + '/services/photogallery/', ['get_thumb']);
    var def = this.adminservices.get_thumb(photo_num);
    def.addCallback(this.PreloadImage);
    def.addErrback(this.PreloadNoImage);
}

PhotoManager.prototype.PreloadNoImage = function(e) {
    this.image_url = '';
    log(e);
}

PhotoManager.prototype.PreloadImage = function(url) {
    this.image_url = url;
    var image = new Image();
    image.src = url;
}

PhotoManager.prototype.ShowThumb = function() {
    var remote_autocompleter = new AutoComplete.Remote('id_photographer', 'autocompleter_choices', '/adminservices/swimmers/', 
        {'minChars':1, 'css':'/media/css/autocomplete.css', 
        'updateElement':'addItemToList', 'input_class':'vTextField', 'method':'get_swimmers' });
    remote_autocompleter.initialize()
 
    var div_first = getFirstElementByTagAndClassName('div', 'form-row');
    insertSiblingNodesBefore(div_first, DIV({'class':'form-row'}, LABEL({'for':'id_image'}, 'Image:'), IMG({'src':this.image_url, 'border':'0', 'alt':'thumb'})));
}

photoManager = new PhotoManager();
photoManager.initialize();
addLoadEvent(photoManager.ShowThumb);
