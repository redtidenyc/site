SurveyManager = function() {
    bindMethods(this);
}

SurveyManager.prototype.initialize = function() {
    /* This gets called before the page is done loading */
    this.survey_num = location.href.replace(/^http:\/\/[\w.]+\/\w+\/(\d+)\D+$/, '$1');
    this.loading_image = '/media/img/loading.gif';
    this.answers = {};
    this.uid = -1;
    this.qcounter = 0;
    this.servicesproxy = new JsonRpcProxy('http://' + location.host + '/services/survey/', 
        ['swimmer_login', 'get_questions', 'save_answers' ]);

    var def = this.servicesproxy.get_questions(this.survey_num);
    def.addCallback(this.LoadQuestionSet);
    def.addErrback(this.QuestionLoadFailed);
    

}

SurveyManager.prototype.QuestionLoadFailed = function(err) {

}

SurveyManager.prototype.OnLoad = function() {

    var res = TrimPath.processDOMTemplate('login_page');
    $('anchor_div').innerHTML = res;

    if( $('register') ) {
        connect('register', 'onclick', this, 'Login');
    } else if($('intro')) {
        connect('start_survey', 'onclick', this, 'StartSurvey'); 
    } 
}

SurveyManager.prototype.HistoryChange = function(newloc, data) {
    if(newloc == "login" || newloc == "start_survey") {
        var res = TrimPath.processDOMTemplate('login_page');
        $('anchor_div').innerHTML = res;
 
    } else if(newloc.match(/question(\d+)/)) {
        var qid = newloc.replace(/question(\d+)/, "$1");
        this.LoadQuestion(qid);
    }
}

SurveyManager.prototype.Login = function(e) {
        var usms = $('usms').value;
	var def = this.servicesproxy.swimmer_login(usms);
	def.addCallbacks(this.SurveyBuild, this.LoginError);
}

SurveyManager.prototype.LoginError = function(e) {
    this.InsertError('Invalid USMS number ' + e); 
}

SurveyManager.prototype.SurveyBuild = function(sid) {
    if(sid < 0) {
        this.InsertError('Invalid USMS number');     
    } else {
        log(sid);
        this.uid = sid;
        if(this.introduction) {
            log('displaying intro');
            $('main_box').innerHTML = this.introduction;
            appendChildNodes('main_box', P({}, INPUT({'type':'button',  'id':'start_survey', 'value':'Start Taking the Survey'})));
            connect('start_survey', 'onclick', this, 'StartSurvey'); 
        } else { 
            this.StartSurvey();   
        }
    }
}

SurveyManager.prototype.InsertError = function(msg) {
    var err_div = DIV({'id':'error', 'class':'error'},P({}, msg));
    if($('error')) {
        swapDOM('error', err_div);
    } else {
        insertSiblingNodesBefore($('main_box'), err_div);
    }
};

SurveyManager.prototype.StartSurvey = function() {
    log('loading question');
    this.LoadQuestion(this.qids[this.qcounter]);
    this.qcounter += 1;
}

SurveyManager.prototype.LoadQuestionSet = function(qarr) {
    if(qarr.introduction != '') {
        this.introduction = qarr.introduction;
    } else {
        this.introduction = null;
    }
    this.questions = {};
    this.qids = [];
    for(var i = 0; i < qarr.data.length; i++) {
        this.questions[qarr.data[i].id] = qarr.data[i];    
        this.qids[i] = qarr.data[i].id;
    }
}

SurveyManager.prototype.LoadQuestion = function(qid) {
    var question = this.questions[qid];
    var template = '';
    var qno = this.qcounter + 1;
    var data = { 'question':question.question, 'qno':qno };
    var pdata = { 'qno':qno, 'prev':false, 'next':false, 'qtotal':this.qids.length };
    if(qno > 1) {
        pdata['prev'] = true;
    }

    if(qno < this.qids.length) {
        pdata['next'] = true;
    }
    if( question.type == 'choice' ) {
        template = 'vert_choice_template';
        data['multiple'] = question.data['multiple'];
        data['choices'] = question.data['choices'];
    } else if ( question.type == 'comment' ) {
        template = 'comment_template';
    } else if ( question.type == 'matrix') {
        template = 'matrix_template';
        data['clabels'] = question.data['clabels'];
        data['rlabels'] = question.data['rlabels'];
    }
    
    var page = TrimPath.processDOMTemplate('pagination', pdata);
    var res = TrimPath.processDOMTemplate(template, data);
    $('anchor_div').innerHTML = res;
    $('main_box').innerHTML += page;
    if(pdata['prev']) {
        connect('prev_question', 'onclick', this, 'PrevQuestion');
    }
    if(pdata['next']) {
        connect('next_question', 'onclick', this, 'NextQuestion');
    } else {
        connect('finish', 'onclick', this, 'FinishSurvey');
    }
}

SurveyManager.prototype.PrevQuestion = function(e) {
    log('in prev');
    this.SaveCurrentQuestion();
    if(this.qcounter > 0) {
        this.qcounter -= 1;
    }
    log(this.qcounter);
    this.LoadQuestion(this.qids[this.qcounter]);
}

SurveyManager.prototype.SaveCurrentQuestion = function() {
    var current_type = this.questions[this.qids[this.qcounter]].type; 
    var current_qid = this.qids[this.qcounter];
    if($('prev_question')) {
        disconnectAllTo('prev_question');
    }
    if($('next_question')) {
        disconnectAllTo('next_question');
    }
    this.answers[current_qid] = [];
    if( current_type == 'comment' && $('comment')) {
        this.answers[current_qid] = [ $('comment').value ];   
    } else if ( current_type == 'choice' ) {
        var inputs = getElementsByTagAndClassName('input', null, 'main_box');
        for( var i = 0; i < inputs.length; i++ ) {
            if(inputs[i].checked) {
                log(inputs[i].value);
                this.answers[current_qid][this.answers[current_qid].length] = inputs[i].value;
            }
        }
        var tareas = getElementsByTagAndClassName('textarea', null, 'main_box');
        for( var i = 0; i < tareas.length; i++) {
            if(tareas[i].value != '') {
                this.answers[current_qid][this.answers[current_qid].length] = tareas[i].value;
            }
        }
    } else if ( current_type == 'matrix' ) {
        var inputs = getElementsByTagAndClassName('input', null, 'main_box');
        for( var i = 0; i < inputs.length; i++ ) {
            if(inputs[i].checked) {
                log(inputs[i].value);
                this.answers[current_qid][this.answers[current_qid].length] = inputs[i].value;
            }
        } 
    }
}

SurveyManager.prototype.NextQuestion = function(e) {
    /* First thing is that we save the answer */
    log('Next Question');
    this.SaveCurrentQuestion();
    this.qcounter += 1; 
    this.LoadQuestion(this.qids[this.qcounter]);
}

SurveyManager.prototype.SaveUnanswered = function(na_set) {

}

SurveyManager.prototype.FinishSurvey = function(e) {
    this.SaveCurrentQuestion(); 
    var def = this.servicesproxy.save_answers(this.answers, this.survey_num, this.uid);
    def.addCallback(this.SaveUnanswered);
    var res = TrimPath.processDOMTemplate('finished', {});
    $('anchor_div').innerHTML = res;
}

surveyManager = new SurveyManager();
surveyManager.initialize();
addLoadEvent(surveyManager.OnLoad);
