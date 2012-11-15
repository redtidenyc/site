/* */

RegistrationManager = function() {
	bindMethods(this);
};

RegistrationManager.prototype.initialize = function() {
    /* This is to handle state changes */
    dhtmlHistory.initialize();
    dhtmlHistory.addListener(this.HistoryChange);
    this.start_hash = { error:'', email:'', month:'', day:'', year:''};
    var res = TrimPath.processDOMTemplate('start', this.start_hash);
    $('reg_form').innerHTML = res;
    this.formvars = { email:'', usms:'', firstname:'', middle:'', lastname:'', 
            dob_month:'', dob_day:'', dob_year:'', address:'', address2:'', city:'', gender:'M', zip:'', 
            dayphone:'', evephone:'', terms:'0', iscoach:'0', errors: [] }; 
    historyStorage.put('start_hash', this.start_hash );
    historyStorage.put('formvars', this.formvars);
    
    if( dhtmlHistory.isFirstLoad()) { dhtmlHistory.add('start_page', this.start_hash); }

    connect('faq_link', 'onclick', this, 'ShowText');
    var _this = this;
    connect('empty_form', 'onclick', function(e) { _this.BuildForm({}); });
    connect('lookup_submit', 'onclick', this, 'Lookup');
    
    this.servicesproxy = new JsonRpcProxy('http://' + location.host + '/services/registration/', 
        [ 'getstates', 'getplans', 'lookup', 'calcowed' ]);
    /*
     * We immediantly pull the plans from the server to build out the registration 
     * form later on if we haven't gotten them previously
     */
    if( ! historyStorage.hasKey('plans')) {
        var def = this.servicesproxy.getplans();
        def.addCallback(this.GetPlans);
        def.addErrback(function(err) { log(err); });
    }
    if( ! historyStorage.hasKey('states')) {
        /* And then we get a list of states for populating the state drop down */
        var def2 = this.servicesproxy.getstates();
        def2.addCallback(this.GetStates);
        def2.addErrback(function(err) { log(err); });
    }
}

RegistrationManager.prototype.HistoryChange = function(newloc, data) {
    if(newloc == 'start_page') {
        this.start_data = historyStorage.get('start_data');
        this.ResetLookupForm(data);
    } else if( newloc == 'form_page' ) {
        this.formvars = historyStorage.get('formvars');
        this.BuildForm(data);
    } else if( newloc == 'confirm_page') {
        this.formvars = historyStorage.get('formvars');
        this.BuildConfirm(data);
    }
}

RegistrationManager.prototype.ApplyOverlay = function() {
    var arrayPageSize = GetPageSize();
    var pagedim = { 'w':arrayPageSize[0], 'h':arrayPageSize[1] };
    setElementDimensions('overlay', pagedim);
    setElementDimensions('content', { 'w':pagedim.w - 100, 'h':pagedim.h - 100 });
    setElementPosition('content', {'x':50});
}

RegistrationManager.prototype.ShowText = function(e) {
    this.ApplyOverlay();
    var link = 'http://' + location.host + '/terms/';
    
    if(e.src().id == 'faq_link') { 
        link = 'http://' + location.host + '/faq/';
    }
    appear('overlay', { 'from':0.0, 'to':1.0 });
    var def2 = doSimpleXMLHttpRequest(link);
    def2.addCallback(swapFromHttp, 'content');
    def2.addCallback(this.HangText);
    def2.addErrback(function(err){ log(err); });
    HideSelectBoxes();
};

RegistrationManager.prototype.HangText = function(e) {
    connect('close_link', 'onclick', this, 'HideText');
    connect('close_link_bottom', 'onclick', this, 'HideText');
}

RegistrationManager.prototype.HideText = function(e) {
    disconnectAllTo('close_link');
    disconnectAllTo('close_link_bottom');
    fade('overlay', {'duration' : 1});
    ShowSelectBoxes();
}

RegistrationManager.prototype.GetStates = function(states) {
    historyStorage.put('states', states);
}

RegistrationManager.prototype.GetPlans = function(plans) {
    historyStorage.put('plans', plans);
}

RegistrationManager.prototype.HoldPlace = function(mid_div, msg) {
    var placeholderdiv = DIV({'id':'reg_form', 'class':'subright'}, P({'style':'padding: 50px;' }, msg));
    swapDOM(mid_div, placeholderdiv);
}

RegistrationManager.prototype.ParseLookup = function(req) {
	log('Parseing lookup');
	var ret_val = { errors:[] };
	for(var k in req ) {
		if(k == 'error') {
			for(var j = 0; j < req.error.length; j++) {
				throw(req.error[j]);
			}
		}
                else if( k != 'dob') {
                    ret_val[k] = req[k];
                } else {
                    ret_val['dob_month'] = req[k].substr(0,2);
                    ret_val['dob_day'] = req[k].substr(2, 2);
                    ret_val['dob_year'] = req[k].substr(4, 4);
                }
	}
	var sid = ret_val.sid;
	if(!sid)
		sid = 0;
        historyStorage.put('formvars', ret_val);
        historyStorage.put('sid', sid);
	this.sid = sid;
        this.formvars = ret_val;
        return ret_val;
}

RegistrationManager.prototype.Lookup = function(e) {
	var email = $('email').value;
	var dob_month = unescape($('dob_month').value);
	dob_month = dob_month.replace(/\s+/g,'') ; 
	var dob_day = unescape($('dob_day').value);
	dob_day = dob_day.replace(/\s+/g,'') ;
	var dob_year = unescape($('dob_year').value);
	dob_year = dob_year.replace(/\s+/g,'') ;
	if(dob_month != '' && dob_month < 10 && dob_month.length == 1){
		dob_month = '0' + dob_month;
	}
	
	if(dob_day != '' && dob_day < 10 && dob_day.length == 1){
		dob_day = '0' + dob_day;
	}
	
	if(dob_year < 1900){
		dob_year = '19' + dob_year;
	}
	
	var date_string = dob_month + dob_day + dob_year;
	date_string.replace(/\D/, '');
	/* add the email and the dob in case we need them later */
	this.start_hash = {'email':email, 'month':dob_month, 'day':dob_day, 'year':dob_year} 
	/* Now we set the placeholder div while we do the lookup */
	this.HoldPlace('reg_form', IMG({'src':'/media/img/loadingAnimation.gif'}));
	dhtmlHistory.add('start_page', this.start_hash);
        historyStorage.put('start_hash', this.start_hash);
        var def = this.servicesproxy.lookup(email, date_string);
	def.addCallback(this.ParseLookup);
	def.addCallback(this.BuildForm);
	def.addErrback(this.ResetLookupForm);
	this.deferred = def;
	
};

RegistrationManager.prototype.ResetLookupForm = function(data, err) {
	/* And now we rebuild the original form with an error message */
	/* First diconnect the signal from the old form */
	disconnect('lookup_submit');
        log('In reset form ' + err + ' ' + typeof(this.start_hash));
        for(var d in data) {
            log(d + ' ' + data[d]);
        }
        if(data['name'].search(/Error/)) { err = data['message'] }
        if(data == null && typeof(this.start_hash) != 'object') { data = historyStorage.get('start_hash'); }
        else { data = this.start_hash; }
        if(err && err != '') {
            data['error'] = err;
        } else {
            data['error'] = undefined;
        }
        var res = TrimPath.processDOMTemplate('start', data);
        $('reg_form').innerHTML = res;
	connect('lookup_submit', 'onclick', this, 'Lookup');
}

RegistrationManager.prototype.Confirm = function(e) {
	/* First validate the existing form.  If it's fine we head to confirmation */
	var form = this.Validate();
        dhtmlHistory.add('form_page', form);
        historyStorage.put('formvars', form);
	if(form.errors.length > 0) {
		this.BuildForm(form);
	} else {
		if(!this.sid) {
			this.sid = -1;
		}
		var def = this.servicesproxy.calcowed($('plan').value, this.sid);
		def.addCallback(this.SetOwed);
		def.addCallback(this.BuildConfirm);
		def.addErrback(function(e) { log(e); });
	}
}

/* This builds the confirm template 
   Before this gets saved to the database there are sanity checks to make sure the data is
   consistent and then the user is redirected to paypal.
 */

RegistrationManager.prototype.BuildConfirm = function(formvars) {
    var data = { formvars : formvars };
    log(formvars.iscoach);
    var res = TrimPath.processDOMTemplate('confirm', data);
    $('reg_form').innerHTML = res;
    //connect('correct', 'onclick', this, 'Correct');
    if (formvars.owed > 0.0 || formvars.iscoach == '1') {
        connect('submit', 'onclick', this, 'Complete');
    }
    dhtmlHistory.add('confirm_page', formvars); 
    log('Done building');
}
/*
	Okay we are almost home here.  This fills out a big old get string and sends it to the server
 */
RegistrationManager.prototype.Complete = function(e) {
	var formvars = this.getformvars();
	
	var vars = {};
	for(v in formvars) { 
		/* There is some data cleaning going on in the validate */
		vars[v] = formvars[v].validator(formvars[v].value);
	}

	for(var i = 0; i < this.formvars.plans.length; i++) {
		vars['plan' + i] = this.formvars.plans[i];
	}
        vars['dob'] = vars['dob_year'] + '-' + vars['dob_month'] + '-' + vars['dob_day'];
	vars['owed'] = this.formvars.owed;
	for(v in vars) {
		log(v + '=' + vars[v]);
	}
	/*if (vars['iscoach'] == 1) {
		this.HoldPlace('reg_form', 'Saving registration information...');
		location.href = 'http://' + location.host + '/register/complete/?' + queryString(vars); 
	} else {*/
		this.HoldPlace('reg_form', 'Redirecting To Paypal...');
		var def = loadJSONDoc('http://' + location.host + '/register/complete', vars);
		log("finished saving registration information") ;	
		def.addCallback(this.BuildPayPalPost);
		def.addErrback(function(e) { log(e); });
	//} 
}

RegistrationManager.prototype.BuildPayPalPost = function(req) {
	log("in build paypal");
	var hash = req;
	hash.image_url = hash.image_url.replace('\\', '');
	var ppgateway = hash.vendor_link.replace('\\', '');
	log(hash.notify_url);
	log(ppgateway);
	
	var swap_dom = DIV({});
	var swap_form = FORM({'name':'swapform', 'action':ppgateway, 'method':'post'});
	for(var i in hash) {
		log(i + "=>" + hash[i]);
		appendChildNodes(swap_form, INPUT({'type':'hidden', 'name':i, 'value':hash[i] }));
	}
	appendChildNodes(swap_dom, swap_form);
	swapDOM('reg_form', swap_dom);
	document.swapform.submit();
}

/* This returns a hash of the registration form variables 
   Validators and all.  It first checks the current DOM
*/

RegistrationManager.prototype.getformvars = function() {
	var ret_val = {};
        var formvars = this.formvars;
        var inputs = getElementsByTagAndClassName('input');
        for(var i = 0; i < inputs.length; i++) {
            var key = inputs[i].name
            var value = inputs[i].value;
            if(key == 'gender' && inputs[i].checked ) { 
                formvars[key] = value; 
            } else if (key != 'gender' ) {
                formvars[key] = value;
            }
        }

        if($('state')) { 
            formvars['state'] = { id : $('state').options[$('state').selectedIndex].value, 
                             code : scrapeText($('state').options[$('state').selectedIndex]) }; }
        if($('plan')) { 
            formvars['plan'] = { id : $('plan').options[$('plan').selectedIndex].value, 
                name : scrapeText($('plan').options[$('plan').selectedIndex]) }; 
        }
       
        var reg = /Coach/;

        if( reg.test(formvars['plan'].name)) { 
            formvars['iscoach'] = '1'; 
        }
 	
	var generic_text_test = function(val) {
		var exp = /^(\w+)|(\s+)$/;
		if(exp.test(val)) {
			return val;
		} else {
			return 0;
		}	
	};

	var null_test = function(val) {
		return val;
	};

	var numeric_test = function(val) {
		var exp = /^\d+$/;
		if(exp.test(val)) {
			return val;
		} else {
			return 0;
		}
	};

	ret_val['email'] = { 'value': formvars['email'], 'validator':function(val) {
			var exp = /^[0-9a-zA-Z_.]+@[0-9a-zA-Z_.-]+$/;
			if(exp.test(val)) {
				return val;
			} else {
				return 0;
			}
		}, 'example':'joe@aol.com', 'required':1
	};
	ret_val['usms'] = { 'value':formvars['usms'], 'validator':function(val) {
			var d = new Date();
			var year = new String(d.getFullYear());
			year = year.substr(3, 1);
			var exp = /^\d{3}\w{1}-\d{2}\w{3}$/;
			/* require next years usms number if it's after Dec. 15 */
			if (d.getMonth() == 11 && d.getDate() >= 10) {
				if (exp.test(val) && val.substr(2,1) == (year*1+1)) {
					return val ;
				} else {
				 	return 0 ;
				}
			} else if(exp.test(val) && val.substr(2, 1) == year) {
				return val;
			} else if ((d.getMonth() == 10 || d.getMonth() == 11) && 
				exp.test(val) &&
				val.substr(2,1) == (year*1+1)) {	
				return val ;
			} else {
				return 0;
			}
		}, 'example':'065V-02XYZ', 'required':1
	};
	ret_val['firstname'] = { 'value':formvars['firstname'], 'validator':function(val) {
			var exp = /^[a-zA-Z ]+$/;
			if(exp.test(val)) {
				return val;
			} else {
				return 0;
			}	
		}, 'example':'John', 'required':1
	};
	ret_val['middle'] = { 'value':formvars['middle'], 'validator':function(val) {
			return (val) ? val.substr(0,1) : '';
		}, 'example':'Q', 'required':0
	};
	
        ret_val['plan'] = { 'value':formvars['plan'], 'validator':function(val) { return numeric_test(val.id) }, 'example':'', 'required':1 };
 
	ret_val['lastname'] = { 'value':formvars['lastname'], 'validator':function(val) {
			var exp = /^[a-zA-Z- ]+$/;
			if(exp.test(val)) {
				return val;
			} else {
				return 0;
			}	
		}, 'example':'Public', 'required':1 
	};
	ret_val['address'] = { 'value':formvars['address'],  'validator':generic_text_test, 'example':'123 Fake Street', 'required':1};
	ret_val['address2'] = { 'value':formvars['address2'], 'validator':generic_text_test, 'example':'Apt. 4A', 'required':0 };
	ret_val['city'] = { 'value':formvars['city'], 'validator':generic_text_test, 'example':'New York', 'required':1 };
	ret_val['state'] = { 'value':formvars['state'], 'validator':function(val) { return numeric_test(val.id) }, 'example':'NY', 'required':1 };
	ret_val['zip'] = { 'value':formvars['zip'], 'validator':function(val) {
			var exp = /^\d{5}(-\d{4})?$/;
			if(exp.test(val)) {
				return val;
			} else {
				return 0;
			}			
		}, 'example':'10011', 'required':1
	};
        
	ret_val['dob_year'] = { 'value':formvars['dob_year'], 'validator':numeric_test, 'required':1 };
	ret_val['dob_month'] = { 'value':formvars['dob_month'], 'validator':numeric_test, 'required':1 };
	ret_val['dob_day'] = { 'value':formvars['dob_day'], 'validator':numeric_test, 'required':1 };

	ret_val['dayphone'] = { 'value':formvars['dayphone'], 'validator':function(val) { return val.replace(/\D/g, ''); },
		'example':'(212) 555-5555', 'required':0
	};
	ret_val['evephone'] = { 'value':formvars['evephone'], 'validator':function(val) { return val.replace(/\D/g, ''); },
		'example':'(212) 555-5555', 'required':0 
	};
	ret_val['gender'] = { 'value':formvars['gender'], 'validator':null_test, 'required':1 };

	ret_val['iscoach'] = { 'value':(formvars['iscoach'] == undefined) ? '0' : formvars['iscoach'], 'validator':null_test, 'required':0 };

	ret_val['terms'] = {'value':formvars['terms'], 
			'validator':function(v) { if( v ) { return 1; } else { return 0; } }, 'required':1, 'example':'checked' };

	/* At this point we have all the static fields.  We take the selected plan and send it back to the server 
	for a calculation of the plans and amount owed.  The xml out to come back like 
	<
	*/
	return ret_val
}

RegistrationManager.prototype.SetOwed = function(req) {
	var pando = req;
	var fvals = this.getformvars();
	var ret_val = {};
	for( var f in fvals) {
		ret_val[f] = fvals[f].value;
	}
        
        ret_val.plans = pando.plans;
	ret_val.owed = pando.owed;
        log('iscoach val = ' + ret_val['iscoach']);
        historyStorage.put('formvars', ret_val);
        this.formvars = ret_val;
	return ret_val;
}

RegistrationManager.prototype.Correct = function(e) {
	log('in Correct');
	var formvars = this.getformvars();
	var tform = {};
	for(var i in formvars) {
		tform[i] = formvars[i].value;
	}
	this.BuildForm(tform);
}

RegistrationManager.prototype.Validate = function() {
	var err_count = 0;
	var formvars = this.getformvars();
	var ret_val = { 'errors' : new Array() };
	for(var v in formvars) {
	    var value = formvars[v].validator(formvars[v].value);
	    if( value == 0 && formvars[v].required == 1) {
		ret_val['errors'][err_count] = v + ' is required. It should look like: ' + formvars[v].example;
		err_count += 1;
	    } else if(v != 'errors') {
	        ret_val[v] = value;
	    }
        }
	return ret_val;
}

/* we use this to build out the form whether we have form data or no */

RegistrationManager.prototype.BuildForm = function(vars) {
        if(vars == null) { vars = historyStorage.get('formvars'); }
        var data = { formvars : vars, plans : historyStorage.get('plans') , states: historyStorage.get('states') };
        var res = TrimPath.processDOMTemplate('form', data);
        $('reg_form').innerHTML = res;
	connect('register', 'onclick', this, 'Confirm');
	connect('terms_link', 'onclick', this, 'ShowText');
        dhtmlHistory.add('form_page', vars);
}


registrationManager = new RegistrationManager();
addLoadEvent(registrationManager.initialize);
