BlogManager = function() {
    bindMethods(this);
}

BlogManager.prototype.initialize = function() {
    var sub_lis = getElementsByTagAndClassName('li', null, 'rightnav');
    var dom = getFirstElementByTagAndClassName('div', 'redline', 'subright');
    this.cid = dom.id.replace(/current_(\d+)/, "$1");
    for(var i = 0; i < sub_lis.length; i++) {
        if(sub_lis[i].id != 'blog_' + this.cid) {
            connect(sub_lis[i].id, 'onclick', this, 'SwapBlog');
        }
    }

    this.servicesproxy = new JsonRpcProxy('http://' + location.host + '/services/blog/', ['get_blog']);
}

BlogManager.prototype.SwapBlog = function(e) {
    var id = e.src().id.replace(/blog_(\d+)/, "$1");
    var link = 'http://' + location.host + '/blog/xml/' + id + '/';
    var def = this.servicesproxy.get_blog(id);
    def.addCallback(this.PostBlog);
    var def2 = doSimpleXMLHttpRequest(link);
    def2.addCallback(swapFromHttp, 'blog');
    def2.addErrback(function(e) { log(e); });
    disconnectAllTo(e.src().id); 
}

BlogManager.prototype.PostBlog = function(bdata) {
    log(this.cid);
    swapDOM('current_' + this.cid, DIV({'id':'current_' + bdata.id, 'class':'redline'}, H2({}, bdata.author + ' ' + bdata.title)));
    swapDOM('pub_date', H3({'id':'pub_date'}, bdata.pub_date));
    var content = scrapeText($('blog_' + this.cid));
    swapDOM('blog_' + this.cid, LI({'id':'blog_'+ this.cid }, A({'href':'javascript:void(0);'}, content)));
    connect('blog_' + this.cid, 'onclick', this, 'SwapBlog');
    
    this.cid = bdata.id;
    log(this.cid);
    swapDOM('blog_' + this.cid, LI({'id':'blog_'+ this.cid }, bdata.author + ' "' + bdata.title + '"')); 
    
}

blogManager = new BlogManager();
addLoadEvent(blogManager.initialize);
