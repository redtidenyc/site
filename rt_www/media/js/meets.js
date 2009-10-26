MeetManager = function() {
    bindMethods(this);
}

MeetManager.prototype.initialize = function() {
    this.cyears_dom = $('subleft');
    this.lyears_dom = null;
    var today = new Date();
    this.current_year = today.getFullYear();
    this.last_year = this.current_year - 1;
    this.servicesproxy = new JsonRpcProxy('http://' + location.host + '/services/meets/', [ 'get_results' ]);
    this.CurrentRightNav();
}

MeetManager.prototype.CurrentRightNav = function() {
    disconnectAllTo('cyear');
    removeElement('rightnav');
    appendChildNodes('subright', UL({'id':'rightnav'},
        LI({'id':'cyear'}, STRONG({}, this.current_year + ' Meet Schedule and Results')), 
        LI({}, A({'id':'lyear', 'href':'javascript:void(0);'}, this.last_year + ' Meet Results'))));
    connect('lyear', 'onclick', this, 'DisplayMeets');
}

MeetManager.prototype.LastRightNav = function() {
    disconnectAllTo('lyear');
    removeElement('rightnav');
    appendChildNodes('subright', UL({'id':'rightnav'},
        LI({}, A({'id':'cyear', 'href':'javascript:void(0);'}, this.current_year + ' Meet Schedule and Results')), 
        LI({'id':'lyear'}, STRONG({}, this.last_year + ' Meet Results'))));
    connect('cyear', 'onclick', this, 'DisplayMeets');
}

MeetManager.prototype.DisplayMeets = function(e) {
    var id = e.src().id;
    if(id == 'lyear') {
        if(this.lyears_dom == null) {
            var def = this.servicesproxy.get_results(this.last_year, 10);
            def.addCallback(this.DisplayPastMeets);
            def.addErrback(function(e) { log(e); });
        } else {
            swapDOM('subleft', this.lyears_dom);
        }
            this.LastRightNav(); 
    } else {
        swapDOM('subleft', this.cyears_dom);
        this.CurrentRightNav();
    }
}

MeetManager.prototype.DisplayPastMeets = function(meet_arr) {
    var data = { meets : meet_arr, year : this.last_year };
    var result = TrimPath.processDOMTemplate('results', data);
    this.lyears_dom = MochiKit.DOM.DIV({'id':'subleft', 'class':'subleft'});
    this.lyears_dom.innerHTML = result;
    MochiKit.DOM.swapDOM('subleft', this.lyears_dom);
}

meetManager = new MeetManager();
addLoadEvent(meetManager.initialize);
