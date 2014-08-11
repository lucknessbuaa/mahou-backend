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

    function modifyShow(data) {
        var request = $.post("/backend/show/" + data.pk, data, 'json');
        return when(request).then(mapErrors, throwNetError);
    }

    function addShow(data) {
        var request = $.post("/backend/show/add", data, 'json');
        return when(request).then(mapErrors, throwNetError);
    }

    function deleteShow(id) {
        var request = $.post("/backend/show/delete", {
            id: id
        }, 'json');
        return when(request).then(mapErrors, throwNetError);
    }

    function requireMag() {
        var request = $.post("/backend/show/requireMag", 'json');
        return when(request).then(mapErrors, throwNetError);
    }
    var selectMag = [];
    requireMag().then(_.bind(function(data) {
        selectMag = data.selectMag;
    }, this));

    var proto = _.extend({}, formProto, formValidationProto);
    var ShowForm = Backbone.View.extend(_.extend(proto, {
        initialize: function() {
            this.setElement($.parseHTML(ShowForm.tpl().trim())[0]);
            this.$alert = this.$("p.alert");
            this.$(".glyphicon-info-sign").tooltip();
        },

        setDate: function() {
            this.$("[name=stop]").attr({
                readOnly: "true"
            });
            this.$("[name=start]").attr({
                readOnly: "true"
            });
            this.$("[name=scoretime]").attr({
                readOnly: "true"
            });
            this.$("[name=start]").datetimepicker({
                maxView: 2,
                minView: 0,
                language: 'zh-CN',
                format: 'yyyy-mm-dd hh:ii',
                viewSelect: 'month',
                autoclose: "true",
                minuteStep: 1,
            });
            this.$("[name=scoretime]").datetimepicker({
                maxView: 2,
                minView: 0,
                language: 'zh-CN',
                format: 'yyyy-mm-dd hh:ii',
                viewSelect: 'month',
                autoclose: "true",
                minuteStep: 1,
            });
            this.$("[name=stop]").datetimepicker({
                maxView: 2,
                minView: 0,
                language: 'zh-CN',
                format: 'yyyy-mm-dd hh:ii',
                viewSelect: 'month',
                autoclose: "true",
                minuteStep: 1,
            });

            this.$("[name=start]").datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
            this.$("[name=scoretime]").datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
            this.$("[name=stop]").datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        },

        setShow: function(show) {
            _.each(['pk', 'show', 'magician', 'start', 'scoretime', 'stop', 'score1', 'score2', 'score3'], _.bind(function(attr) {
                this.el[attr].value = show[attr];
            }, this));
            $(this.el.magician).val(show.magician).trigger('change');
            var tempTime1 = moment(show['start'], "MMM DD,YYYY,h:m a");
            this.el['start'].value = tempTime1.format("YYYY-MM-DD HH:mm");
            var tempTime1 = moment(show['scoretime'], "MMM DD,YYYY,h:m a");
            this.el['scoretime'].value = tempTime1.format("YYYY-MM-DD HH:mm");
            var tempTime = moment(show['stop'], "MMM DD,YYYY,h:m a");
            this.el['stop'].value = tempTime.format("YYYY-MM-DD HH:mm");
        },

        bind: function(data) {
            var defaults = {
                id: '',
                title: '',
                description: '',
                url: ''
            };
            data = _.defaults(data, defaults);
            _.each(['pk', 'magician', 'show', 'scoretime', 'start', 'stop', 'score1', 'score2', 'score3'], _.bind(function(attr) {
                this.el[attr].value = data[attr];
            }, this));
        },

        initMag: function() {
            this.$("[name=magician]").select2({
                data: selectMag,
                formatNoMatches: '没有相关信息',
            });
        },

        onShow: function() {
            this.initMag();
            this.setDate();
        },

        clear: function() {
            _.each(['pk', 'magcian', 'show',  'start', 'scoretime', 'stop', 'score1', 'score2', 'score3'], _.bind(function(field) {
                $(this.el[field]).val('').trigger('change');
            }, this));

            this.clearTip();
        },

        onHide: function() {
            this.clear();
            this.clearErrors(['pk', 'magician', 'show', 'start', 'scoretime', 'stop', 'score1', 'score2', 'score3'])
            $(this.el).parsley('destroy');
        },

        getData: function() {
            var data = this.$el.serializeObject();

            return data;
        },

        validate: function() {
            this.clearErrors(['pk', 'magician', 'show', 'start', 'scoretime', 'stop', 'score1', 'score2', 'score3']);
            this.clearTip();

            return true;
        },

        save: function() {
            var onComplete = _.bind(function() {
                this.trigger('save');
            }, this);

            if (!this.validate()) {
                return setTimeout(onComplete, 0);
            }

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

            var data = this.getData();

            if (this.el.pk.value !== "") {
                modifyShow(data)
                    .then(onFinish, onReject)
                    .ensure(onComplete);
            } else {
                addShow(data)
                    .then(onFinish, onReject)
                    .ensure(onComplete);
            }
        }
    }));

    $(function() {
        ShowForm.tpl = _.template($("#form-tpl").html());

        var form = new ShowForm();
        var modal = new modals.FormModal();
        modal.setForm(form);
        $(modal.el).appendTo(document.body);

        $create = $("#create-show");
        $create.click(function() {
            location.href("/backend/new");
        });

        $('.edit').click(function(){
            var pk = $(this).parent().data('pk');
            var locStr = '/backend/new?id=' + pk; 
            location.href=locStr;
        });
    });

    $(function() {
        $("th.show, td.show").removeClass('show');
    });

    $(function() {
        var modal = new modals.ActionModal();
        modal.setAction(function(id) {
            return deleteShow(id).then(function() {
                utils.reload(500);
            }, function(err) {
                if (err instanceof errors.AuthFailure) {
                    window.location = "/welcome";
                }

                throw err;
            });
        });
        modal.setTitle('删除节目信息');
        modal.tip('确定要删除吗？');
        modal.setSaveText('删除', '删除中...');
        modal.on('succeed', function() {
            utils.reload(500);
        });
        $("table").on("click", ".delete", function() {
            modal.setId($(this).parent().data('pk'));
            modal.show();
        });
    });
});
