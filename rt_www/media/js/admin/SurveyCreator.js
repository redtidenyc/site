/*
	This manages the form creation in the admin
 */

QuestionManager = function() {
    bindMethods(this);
}

QuestionManager.prototype.initialize = function() {
    this.ConnectTypeSelector();
    this.typemap = {};
    var _this = this;
    this.adminproxy = new JsonRpcProxy('http://' + location.host + '/adminservices/survey/', 
        [ 'get_type_options', 'delete_question', 'get_type_mapping', 'save_question', 'get_question', 'edit_question']);
	
    this.servicesproxy = new JsonRpcProxy('http://' + location.host + '/services/survey/', ['get_question']);
    var def = this.adminproxy.get_type_mapping();
    def.addCallback(function(typemap){ for(var i in typemap){ _this.typemap[i] = typemap[i]; }});
    def.addErrback(function(e) { log(e); });
	
    var links = getElementsByTagAndClassName('a', null, $('id_questions'));
    for(var i = 0; i < links.length; i++) {
        if( links[i].id.match(/delq\d+/) ) {
            connect(links[i].id, 'onclick', this, 'DeleteQuestion');
        } else if ( links[i].id.match(/preview\d+/)) {
	    connect(links[i].id, 'onclick', this, 'PreviewQuestion');
	} else if( links[i].id.match(/edit\d+/) ) {
	    connect(links[i].id, 'onclick', this, 'EditQuestion');
	}
    }
    var body = getFirstElementByTagAndClassName('body', null);
    appendChildNodes(body, DIV({'id':'display_question'}, DIV({}, A({'id':'close_preview', 'href':'javascript:void(0);'}, 
            IMG({'border':'0', 'alt':'Close Preview', 'src':'/media/img/admin/icon_deletelink.gif'})))));
    var oFCKeditor = new FCKeditor( 'id_introduction' ) ;
    oFCKeditor.BasePath = "/media/js/fckeditor/" ;
    oFCKeditor.Width = "80%";
    oFCKeditor.Config["CustomConfigurationsPath"] = "/media/js/fckeditor/admin_config.js" ;
    oFCKeditor.ReplaceTextarea() ;
    this.loading_image = '/media/img/loadingAnimation.gif';
    /* Make the list sortable */
    MochiKit.Sortable.Sortable.create('question_list', { 'onChange':this.SortUpdate });
}

QuestionManager.prototype.SortUpdate = function(e) {
    log('in sort update');
    var lis = getElementsByTagAndClassName('li', null, $('question_list'));
    for(var i = 0; i < lis.length; i++) {
        var inputs = getElementsByTagAndClassName('input', null, lis[i]);
        for(var j = 0; j < inputs.length; j++) {
            if(inputs[j].name.match(/order\d+/)) {
                inputs[j].name = 'order' + i;
            }
        }
    }
}

QuestionManager.prototype.PreviewQuestion = function(e) {
    var qid = e.src().id.replace(/preview(\d+)/, "$1");
    var def = this.servicesproxy.get_question(qid);
    def.addCallback(this.OpenPreview);
    def.addErrback(function(e) { log(e) });
}

QuestionManager.prototype.OpenPreview = function(question) {
    var template_id = 'comment';
    if( question.type == 'choice') {
        template_id = 'vert_choice';
    } else if( question.type == 'matrix') {
        template_id = 'matrix';
    }
    
    var res = TrimPath.processDOMTemplate(template_id, question);
    $('display_question').innerHTML += res;
    var qdim = elementDimensions('id_questions');
    connect('close_preview', 'onclick', this, 'ClosePreview');
    appear('display_question', {'duration':1});
}

QuestionManager.prototype.ClosePreview = function(e) {
	log('Close preview');
        disconnectAllTo('close_preview');
        fade('display_question', {'duration':1});
        removeElement('preview_question');
}

QuestionManager.prototype.EditQuestion = function(e) {
	var qid = e.src().id.replace(/edit(\d+)/, "$1");
	var def = this.adminproxy.get_question(qid);
	def.addCallback(this.LoadQuestion);
	def.addErrback(function(e) { log(e); });
}

QuestionManager.prototype.ConnectTypeSelector = function() {
	var type_list = $('type_selector');
	var type_links = getElementsByTagAndClassName('li', null, type_list);
	for(var i = 0; i < type_links.length; i++) {
		connect(type_links[i], 'onclick', this, 'TypeSelected');
	}
}

QuestionManager.prototype.DisconnectTypeSelector = function() {
	var type_list = $('type_selector');
	var type_links = getElementsByTagAndClassName('li', null, type_list);
	for(var i = 0; i < type_links.length; i++) {
		disconnectAll(type_links[i]);
	}
}

QuestionManager.prototype.TypeSelected = function(e) {
	var selected_li = e.src();
	var opt_value = selected_li.id.replace(/type(\d+)/, "$1");
	var def = this.adminproxy.get_type_options(opt_value);
	def.addCallback(this.LoadTypeOptions);
	def.addErrback(function(err) { log(err); });
	def.addErrback(this.ReturnToBuild);
	this.DisconnectTypeSelector();
}

QuestionManager.prototype.CreateBlankChoice = function(is_multiple) {
	var tag = 'Build Choice Question:';
	if(is_multiple) {
		tag = 'Build Multiple Choice Question:';
	}
	var label = LABEL({'id':'creator_label'}, tag);
	var choice_dom = P({}, A({'id':'add_choice', 'class':'connected'}, SPAN({'style':'padding-right: .5em;'}, 'Add Choice:'),
		IMG({'alt':'Add Choice', 'src':'/media/img/admin/icon_addlink.gif'})), BR({}),
		SPAN({'style':'padding-right: .5em;'}, 'Question:'), 
		TEXTAREA({'rows':'2', 'cols':'30', 'id':'question', 'value':''}), HR({}),
		OL({'id':'choicelist'}), INPUT({'type':'button', 'id':'save_choice', 'class':'connected', 'value':'Save Question'}),
		INPUT({'type':'button', 'class':'connected', 'id':'discard_choice', 'value':'Discard Question'}));
	swapDOM('creator_label', label);
	replaceChildNodes('create_container', choice_dom);
	connect('add_choice', 'onclick', this, 'CreateChoice');
	connect('save_choice', 'onclick', this, 'SaveChoice');
	connect('discard_choice', 'onclick', this, 'ReturnToBuild');
}

QuestionManager.prototype.EditChoice = function(q) {
	var tag = 'Edit Choice Question:';
	
	if(q.multiple != 0) {
		tag = 'Edit Multiple Choice Question:';
	}
	var label = LABEL({'id':'creator_label'}, tag);
	var choice_dom = P({}, A({'id':'add_choice', 'class':'connected'}, SPAN({'style':'padding-right: .5em;'}, 'Add Choice:'),
		IMG({'alt':'Add Choice', 'src':'/media/img/admin/icon_addlink.gif'})), 
		INPUT({'type':'hidden', 'id':'qid', 'name':'qid', 'value':q.qid}), BR({}),
		SPAN({'style':'padding-right: .5em;'}, 'Question:'), 
		TEXTAREA({'rows':'2', 'cols':'30', 'id':'question'}, q.question), HR({}),
		OL({'id':'choicelist'}), INPUT({'type':'button', 'id':'save_choice', 'class':'connected', 'value':'Save Question'}),
		INPUT({'type':'button', 'class':'connected', 'id':'discard_choice', 'value':'Discard Edit'}));
	swapDOM('creator_label', label);
	replaceChildNodes('create_container', choice_dom);
	connect('add_choice', 'onclick', this, 'CreateChoice');
	connect('save_choice', 'onclick', this, 'SaveEditedChoice');
	connect('discard_choice', 'onclick', this, 'ReturnToBuild');
	
	/* Add in previous choices */
	
	for(var i = 0; i < q.choices.length; i++) {
		var comment_val = 'off';
		if(q.choices[i].has_comment == 1) {
			comment_val = 'on';
		}
		var choice_li = LI({'class':'choice'}, INPUT({'type':'text', 'id':'choice_' + i, 
			'name':'choice_' + i, 'value':q.choices[i].choice}), 
			SPAN({'style':'padding-right: .5em; padding-left: .5em;'}, 'Allow Comment?'), 
			SPAN({'style':'padding-right: .5em; padding-left: .5em;'}, 
				INPUT({'type':'checkbox', 'name':'checkedchoice_' + i, 'value':comment_val})),
			A({'id':'delchoice_' + i, 'class':'connected', 'href':'javascript:void(0);'}, 
			IMG({'alt':'Delete Choice', 'src':'/media/img/admin/icon_deletelink.gif'})));
		appendChildNodes('choicelist', choice_li);
		connect('delchoice_' + i, 'onclick', this, 'DeleteChoice');
	}
}

QuestionManager.prototype.SaveEditedChoice = function(e) {
	var choicelist = $('choicelist');
	var choices = getElementsByTagAndClassName('input', null, choicelist);
	var data_hash = {};
	for(var i = 0; i < choices.length; i++) {
		data_hash[choices[i].name] = choices[i].value;
	}
	disconnectAll(e.src());
        var li = getFirstParentByTagAndClassName($('delq'+$('qid').value), 'li');
	var def = this.adminproxy.edit_question($('question').value, $('qid').value, data_hash);
	def.addCallback(function(hash) { hash['order'] = li.id.replace(/list(\d+)/, "$1"); return hash; });
	def.addCallback(this.SaveQuestion);
	def.addErrback(function(e) { log(e); });
}

QuestionManager.prototype.CreateBlankMatrix = function() {
	var label = LABEL({'id':'creator_label'}, 'Build Question Matrix:');
	var matrix_dom = P({}, A({'id':'add_row', 'class':'connected'}, SPAN({'style':'padding-right: .5em;'}, 'Add Row:'),
		IMG({'alt':'Add Row', 'src':'/media/img/admin/icon_addlink.gif'})), BR({}),
		A({'id':'add_column', 'class':'connected'}, SPAN({'style':'padding-right: .5em;'}, 'Add Column:'),
		IMG({'alt':'Add Column', 'src':'/media/img/admin/icon_addlink.gif'}), BR({})),
		SPAN({'style':'padding-right: .5em;'}, 'Question:'), 
		TEXTAREA({'rows':'2', 'cols':'30', 'id':'question', 'value':''}), HR({}),
		TABLE({'id':'question_matrix'}, TR({'id':'header_row'}, TH({}, INPUT({'type':'text', 'disabled':''})))),
		INPUT({'type':'button', 'id':'save_matrix', 'class':'connected', 'value':'Save Question'}),
		INPUT({'type':'button', 'id':'discard_matrix', 'class':'connected', 'value':'Discard Question'}));
	swapDOM('creator_label', label);
	replaceChildNodes('create_container', matrix_dom);
	connect('add_row', 'onclick', this, 'CreateRow');
	connect('add_column', 'onclick', this, 'CreateColumn');
	connect('save_matrix', 'onclick', this, 'SaveMatrix');
	connect('discard_matrix', 'onclick', this, 'ReturnToBuild');
	this.column_count = 0;
	this.row_count = 0;
}

QuestionManager.prototype.EditMatrix = function(q) {
	this.CreateBlankMatrix();
	appendChildNodes('question_matrix', INPUT({'type':'hidden', 'id':'qid', 'name':'qid', 'value':q.qid}));
	appendChildNodes('question', q.question);
	$('discard_matrix').value = 'Discard Edit';
	for(var i = 0; i < q.rows.length; i++) {
		this.CreateRow();
		var curr_count = this.row_count - 1;
		$('rlabel' + curr_count ).value = q.rows[i]
	}

	for(var i = 0; i < q.cols.length; i++) {
		this.CreateColumn();
		var curr_count = this.column_count - 1;
		$('clabel' + curr_count ).value = q.cols[i]
	}
	disconnectAll('save_matrix');
	connect('save_matrix', 'onclick', this, 'SaveEditedMatrix');
}

QuestionManager.prototype.SaveEditedMatrix = function(e) {
        var li = getFirstParentByTagAndClassName($('delq'+$('qid').value), 'li');
	var def = this.adminproxy.edit_question($('question').value, $('qid').value, this.GetMatrixData());
	def.addCallback(function(hash) { hash['order'] = li.id.replace(/list(\d+)/, "$1");return hash; });
	def.addCallback(this.SaveQuestion);
	def.addErrback(function(e) { log(e); });
}

QuestionManager.prototype.CreateRow = function(e) {
	var add_tr = TR({}, TD({}, INPUT({'id':'rlabel' + this.row_count, 'type':'text', 
		'name':'rlabel' + this.row_count, 'value':''}), A({'id':'delrow_' + this.row_count, 
		'class':'connected', 'href':'javascript:void(0);'}, 
		IMG({'alt':'Delete Row', 'src':'/media/img/admin/icon_deletelink.gif'}))));
	for(var i = 0; i < this.column_count; i++) {
		appendChildNodes(add_tr, TD({}));
	}
	appendChildNodes('question_matrix', add_tr);
	connect('delrow_' + this.row_count, 'onclick', this, 'DeleteRow');
	this.row_count += 1
}

QuestionManager.prototype.DeleteRow = function(e) {
	var row_link = e.src();
	disconnectAll(row_link);
	var table = $('question_matrix');
	var trs = getElementsByTagAndClassName('tr', null, table);
	for(var i = 0; i < trs.length; i++) {
		if(isChildNode(row_link, trs[i])) {
			removeElement(trs[i]);
		}
	}
}

QuestionManager.prototype.CreateColumn = function(e) {
	/* first we create the header, then add the column to all rows */
	var th_col = TH({}, INPUT({'type':'text', 'id':'clabel' + this.column_count, 'name':'clabel' + this.column_count,
		'value':''}), A({'id':'delcol_' + this.column_count, 'class':'connected', 'href':'javascript:void(0);'}, 
		IMG({'alt':'Delete Column', 'src':'/media/img/admin/icon_deletelink.gif'})));
	var table = $('question_matrix');
	var trs = getElementsByTagAndClassName('tr', null, table);
	for(var i = 1; i < trs.length; i++) {
		appendChildNodes(trs[i], TD({}));
	}
	appendChildNodes('header_row', th_col);
	connect('delcol_' + this.column_count, 'onclick', this, 'DeleteColumn');
	this.column_count += 1;
}

QuestionManager.prototype.DeleteColumn = function(e) {
	var col_link = e.src();
	disconnectAll(col_link);
	var hrow = $('header_row');
	var cols = getElementsByTagAndClassName('th', null, hrow);
	for(var i = 1; i < cols.length; i++) {
		if(isChildNode(col_link, cols[i])) {
			removeElement(cols[i]);
		}
	}
}

QuestionManager.prototype.GetMatrixData = function() {
	var data_hash = {};
	/* Sweep in all the row labels */
	var cols = getElementsByTagAndClassName('th', null, $('header_row'));
	for(var i = 1; i < cols.length; i++) {
		var input = getFirstElementByTagAndClassName('input', null, cols[i]);
		data_hash[input.name] = input.value;
	}

	var rows = getElementsByTagAndClassName('tr', null, $('question_matrix'));
	for(var i = 1; i < rows.length; i++) {
		var input = getFirstElementByTagAndClassName('input', null, rows[i]);
		data_hash[input.name] = input.value;
	}
	return data_hash;	
}

QuestionManager.prototype.SaveMatrix = function(e) {
	return this.SendSave($('question').value, this.typeid, this.GetMatrixData());
}

QuestionManager.prototype.CreateBlankComment = function() {
	var label = LABEL({'id':'creator_label'}, 'Create Comment-Type Question');
	var comment_dom = P({}, SPAN({'style':'padding-right: .5em;'}, 'Question:'), 
		TEXTAREA({'rows':'4', 'cols':'30', 'id':'question', 'value':''}), HR({}),
		OL({'id':'choicelist'}), INPUT({'type':'button', 'class':'connected', 'id':'save_comment', 'value':'Save Question'}),
		INPUT({'type':'button', 'class':'connected', 'id':'discard_comment', 'value':'Discard Question'}));

	swapDOM('creator_label', label);
	replaceChildNodes('create_container', comment_dom);
	connect('save_comment', 'onclick', this, 'SaveComment');
	connect('discard_comment', 'onclick', this, 'ReturnToBuild')	
}

QuestionManager.prototype.EditComment = function(q) {
	this.CreateBlankComment();
	appendChildNodes('question', q.question)
        insertSiblingNodesBefore('question', INPUT({'type':'hidden', 'id':'qid', 'name':'qid', 'value':q.qid}));
	$('discard_comment').value = 'Discard Edit';
	disconnectAll('save_comment');
	connect('save_comment', 'onclick', this, 'SaveEditedComment');
}

QuestionManager.prototype.SaveEditedComment = function(e) {
        var li = getFirstParentByTagAndClassName($('delq'+$('qid').value), 'li');
	var def = this.adminproxy.edit_question($('question').value, $('qid').value, {});
	def.addCallback(function(hash) { hash['order'] = li.id.replace(/list(\d+)/, "$1");  return hash; });
	def.addCallback(this.SaveQuestion);
	def.addErrback(function(e) { log(e); });	
}

QuestionManager.prototype.SaveComment = function(e) {
	return this.SendSave($('question').value, this.typeid, {});
}

QuestionManager.prototype.SendSave = function(question, qtype, data_hash) {
	
	/* We need to disconnect all signals in the html under create_container */
	var connected_elems = getElementsByTagAndClassName(null, 'connected', 'create_container');
	for(var i = 0; i < connected_elems.length; i++) {
		disconnectAll(connected_elems[i]);
	}
	
	var def = this.adminproxy.save_question(question, qtype, data_hash);
	def.addCallback(this.SaveQuestion);
	def.addErrback(function(e) { log(e); });
	return;
}

QuestionManager.prototype.ReturnToBuild = function(e) {
	/* We need to disconnect all signals in the html under create_container. This prevents memory leaks. */
	var connected_elems = getElementsByTagAndClassName(null, 'connected', 'create_container');
	for(var i = 0; i < connected_elems.length; i++) {
		disconnectAll(connected_elems[i]);
	}
	this.CreateQuestionBuild();
}

QuestionManager.prototype.CreateChoice = function(e) {
	var choicelist = $('choicelist');
	var choices = getElementsByTagAndClassName('li', null, choicelist);
	var counter = choices.length;
	var choice_li = LI({'class':'choice'}, INPUT({'type':'text', 'id':'choice_' + counter, 'name':'choice_' + counter, 'value':''}), 
		SPAN({'style':'padding-right: .5em; padding-left: .5em;'}, 'Allow Comment?'), 
		SPAN({'style':'padding-right: .5em; padding-left: .5em;'}, 
			INPUT({'type':'checkbox', 'name':'checkedchoice_' + counter, 'value':'off'})),
		A({'id':'delchoice_' + counter, 'class':'connected', 'href':'javascript:void(0);'}, 
		IMG({'alt':'Delete Choice', 'src':'/media/img/admin/icon_deletelink.gif'})));
	appendChildNodes(choicelist, choice_li);
	connect('delchoice_' + counter, 'onclick', this, 'DeleteChoice');
}

QuestionManager.prototype.SaveChoice = function(e) {
    var choicelist = $('choicelist');
    var choices = getElementsByTagAndClassName('input', null, choicelist);
    var data_hash = {};
    for(var i = 0; i < choices.length; i++) {
        if(choices[i].type == 'checkbox') {
           data_hash[choices[i].name] = ( choices[i].checked ) ? 'on' : 'off'; 
        } else {
            data_hash[choices[i].name] = choices[i].value;
        }
    }
    disconnectAll(e.src());
    return this.SendSave($('question').value, this.typeid, data_hash);
}

QuestionManager.prototype.DeleteChoice = function(e) {
	var link = e.src();
	disconnectAll(link);
	var choicelist = $('choicelist');
	var new_choicelist = OL({'id':'choicelist'});
	var choices = getElementsByTagAndClassName('li', null, choicelist);
	for(var i = 0; i < choices.length; i++) {
		if(!isChildNode(link, choices[i])) {
			appendChildNodes(new_choicelist, choices[i]);	
		}
	}
	swapDOM('choicelist', new_choicelist);
}

/* the request has keys question, qid, and errors */

QuestionManager.prototype.SaveQuestion = function(reply) {
    var qdiv = $('id_questions');
    var qid = reply.qid;
    var question = reply.question;
    var qlist = getFirstElementByTagAndClassName('ol', null, qdiv);
    var lis = getElementsByTagAndClassName('li', null, qlist);
    var qcount = lis.length;
    
    if(reply.order) {
        qcount = reply.order;
        swapDOM('list'+reply.order, LI({'id':'list' + qcount }, INPUT({ 'type':'hidden', 'name':'question' + qid, 'value':qid }),
                INPUT({ 'type':'hidden', 'name':'order' + qcount, 'value':qid }),
			SPAN({'style':'padding-right: .5em;'}, question),  
		SPAN({'style':'padding-right: .5em;'}, A({'id':'delq' + qid, 'href':'javascript:void(0);'}, 
			IMG({'alt':'Delete Question', 'src':'/media/img/admin/icon_deletelink.gif'}))), 
		SPAN({'style':'padding-right: .5em;'}, A({'id':'preview' + qid, 'href':'javascript:void(0);'}, 
			IMG({'alt':'Preview Question', 'src':'/media/img/admin/icon_searchbox.png'}))),
		SPAN({'style':'padding-right: .5em;'}, A({'id':'edit' + qid, 'href':'javascript:void(0);'}, 
			IMG({'alt':'Edit Question', 'src':'/media/img/admin/icon_changelink.gif'})))));
    } else {    
        appendChildNodes(qlist, LI({'id':'list' + qcount }, INPUT({ 'type':'hidden', 'name':'question' + qid, 'value':qid }),
                INPUT({ 'type':'hidden', 'name':'order' + qcount, 'value':qid }),
			SPAN({'style':'padding-right: .5em;'}, question),  
		SPAN({'style':'padding-right: .5em;'}, A({'id':'delq' + qid, 'href':'javascript:void(0);'}, 
			IMG({'alt':'Delete Question', 'src':'/media/img/admin/icon_deletelink.gif'}))), 
		SPAN({'style':'padding-right: .5em;'}, A({'id':'preview' + qid, 'href':'javascript:void(0);'}, 
			IMG({'alt':'Preview Question', 'src':'/media/img/admin/icon_searchbox.png'}))),
		SPAN({'style':'padding-right: .5em;'}, A({'id':'edit' + qid, 'href':'javascript:void(0);'}, 
			IMG({'alt':'Edit Question', 'src':'/media/img/admin/icon_changelink.gif'})))));
	
    }
    connect('delq' + qid, 'onclick', this, 'DeleteQuestion');
    connect('preview' + qid, 'onclick', this, 'PreviewQuestion');
    connect('edit' + qid, 'onclick', this, 'EditQuestion');
    this.CreateQuestionBuild();
}

QuestionManager.prototype.DeleteQuestion = function(e) {
    disconnectAllTo(e.src());
    var qid = e.src().id.replace(/delq(\d+)/, '$1');
    var id = getFirstParentByTagAndClassName(e.src(), 'li', null).id;
    var def = this.adminproxy.delete_question(qid);
    def.addCallback(this.HandleDelete, id);
    def.addCallback(this.SortUpdate, e);
    def.addErrback(function(err) { log(err); });
}

QuestionManager.prototype.HandleDelete = function(id, qid) {	
    if( qid > 0) {
        removeElement(id);
    }
}

QuestionManager.prototype.CreateQuestionBuild = function() {
	var label = LABEL({'id':'creator_label'}, 'Start by choosing a question type:');
	var ul = UL({'id':'type_selector'});
	for(var i in this.typemap) {
		log(i + ' ' + this.typemap[i]);
		appendChildNodes(ul, LI({'id':'type' + i}, this.typemap[i]));
	}
	swapDOM('creator_label', label);
	replaceChildNodes('create_container', ul);
	this.ConnectTypeSelector(); 
}

QuestionManager.prototype.LoadQuestion = function(q) {
	this.DisconnectTypeSelector();
	this.typeid = q.typeid
	switch(q.type) {
		case 'choice':
			this.EditChoice(q);
			break;
		case 'matrix':
			this.EditMatrix(q);
			break;
		case 'comment':
			this.EditComment(q);
			break;
		default:
			break;
	}
}

QuestionManager.prototype.LoadTypeOptions = function(typeopts) {
	this.DisconnectTypeSelector();	
	this.typeid = typeopts.typeid;
	switch(typeopts.type) {
		case 'choice':
			this.CreateBlankChoice(typeopts.multiple);
			break;
		case 'matrix':
			this.CreateBlankMatrix();
			break;
		case 'comment':
			this.CreateBlankComment();
			break;
		case 'error':
			break;
		default:
			break;
	}
}

questionManager = new QuestionManager();
addLoadEvent(questionManager.initialize); 
