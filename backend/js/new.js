define(function(require) {
    require("jquery");
    require("jquery.serializeObject");
    require("jquery.iframe-transport");
    require("bootstrap");
    require("moment");
    require("bootstrap-datetimepicker");
    require("zh-CN");
    require("select2");
    require("parsley");
    var csrf_token = require("django-csrf-support");
    var when = require("when/when");
    var _ = require("underscore");
    require("backbone/backbone");

    var errors = require("errors");
    var utils = require("utils");
    var mapErrors = utils.mapErrors;
    var throwNetError = utils.throwNetError;
    var handleErrors = utils.handleErrors;
    var formProto = require("formProto");
    var formValidationProto = require("formValidationProto");
    var modals = require('modals');
    var SimpleUpload = require("simple-upload");

    $(function(){
        $form = $("form.form-horizontal");
        form = $form[0];

        $(form.start).datetimepicker({
            maxView: 2,
            minView: 0,
            language: 'zh-CN',    
            format: 'yyyy-mm-dd hh:ii',
            viewSelect: 'month',
            autoclose: "true",
            minuteStep: 1,
        });
        $(form.stop).datetimepicker({
            maxView: 2,
            minView: 0,
            language: 'zh-CN',    
            format: 'yyyy-mm-dd hh:ii',
            viewSelect: 'month',
            autoclose: "true",
        });

        var i = 1;
        for(i = 1; i <= 6; i++){
            $("#id_start"+i).datetimepicker({
                maxView: 2,
                minView: 0,
                language: 'zh-CN',    
                format: 'yyyy-mm-dd hh:ii',
                viewSelect: 'month',
                autoclose: "true",
                minuteStep: 1,
            });
        }
        for(i = 1; i <= 6; i++){
            $("#id_stop"+i).datetimepicker({
                maxView: 2,
                minView: 0,
                language: 'zh-CN',    
                format: 'yyyy-mm-dd hh:ii',
                viewSelect: 'month',
                autoclose: "true",
                minuteStep: 1,
            });
        }

        function addShow(data) {
            var request = $.post("/backend/show/add", {
                data: data
            }, 'json');
            return when(request).then(mapErrors, throwNetError);
        }

        $(form.hello).click(function(){
            var data = getData();
            var onComplete = _.bind(function() {
                this.trigger('save');
            }, this);
            var onReject = _.bind(function(err) {
                handleErrors(err,
                    _.bind(this.onAuthFailure, this),
                    _.bind(this.onCommonErrors, this),
                    _.bind(this.onUnknownError, this)
                );
            }, this);

            var onFinish = _.bind(function() {
                this.tip('成功！', 'success');
                utils.reload(500);
            }, this);
        });

        function getData(){
            var data = {
                start: $(form.start).val(),

                name1: $(form.name1).val(),
                start1: $(form.start1).val(),
                stop1: $(form.stop1).val(),
                score11: $(form.score11).val(),
                score12: $(form.score12).val(), 
                score13: $(form.score13).val(),

                name2: $(form.name2).val(),
                start2: $(form.start2).val(),
                stop2: $(form.stop2).val(),
                score21: $(form.score21).val(),
                score22: $(form.score22).val(),
                score23: $(form.score23).val(),

                name3: $(form.name3).val(),
                start3: $(form.start3).val(),
                stop3: $(form.stop3).val(),
                score31: $(form.score31).val(),
                score32: $(form.score32).val(),
                score33: $(form.score33).val(),

                name4: $(form.name4).val(),
                start4: $(form.start4).val(),
                stop4: $(form.stop4).val(),
                score41: $(form.score41).val(),
                score42: $(form.score42).val(),
                score43: $(form.score43).val(),

                name5: $(form.name5).val(),
                start5: $(form.start5).val(),
                stop5: $(form.stop5).val(),
                score51: $(form.score51).val(),
                score52: $(form.score52).val(),
                score53: $(form.score53).val(),

                name6: $(form.name6).val(),
                start6: $(form.start6).val(),
                stop6: $(form.stop6).val(),
                score61: $(form.score61).val(),
                score62: $(form.score62).val(),
                score63: $(form.score63).val(),

                stop: $(form.stop).val(),
            };
            return data;
        }

        $(form.start).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.stop).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));

    });
});
