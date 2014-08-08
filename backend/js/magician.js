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

    function modifyMagician(data) {
        var request = $.post("/backend/magician/" + data.pk, data, 'json');
        return when(request).then(mapErrors, throwNetError);
    }

    function addMagician(data) {
        var request = $.post("/backend/magician/add", data, 'json');
        return when(request).then(mapErrors, throwNetError);
    }

    function deleteMagician(id) {
        var request = $.post("/backend/magician/delete", {
            id: id
        }, 'json');
        return when(request).then(mapErrors, throwNetError);
    }

    var proto = _.extend({}, formProto, formValidationProto);
    var MagicianForm = Backbone.View.extend(_.extend(proto, {
        initialize: function() {
            this.setElement($.parseHTML(MagicianForm.tpl().trim())[0]);
            this.$alert = this.$("p.alert");
            this.$(".glyphicon-info-sign").tooltip();
            this.$("[name=name]").attr({maxlength: 100});
        },

        setMagician: function(magician) {
            _.each(['pk', 'name', 'cover'], _.bind(function(attr) {
                this.el[attr].value = magician[attr];
            }, this));
        },

        onShow: function() {
        },

        bind: function(data) {
            var defaults = {
                id: '',
                title: '',
                description: '',
                url: ''
            };
            data = _.defaults(data, defaults);
            _.each(['pk', 'name', 'cover'], _.bind(function(attr) {
                this.el[attr].value = data[attr];
            }, this));
        },

        clear: function() {
            _.each(['pk', 'name', 'cover'], _.bind(function(field) {
                $(this.el[field]).val('');
            }, this));

            $('[name=cover]').val("").trigger('change');
            this.clearTip();
        },

        onHide: function() {
            this.clear();
            this.clearErrors(['name', 'cover']);
            $(this.el).parsley('destroy');
        },

        getData: function() {
            var data = this.$el.serializeObject();

            return data;
        },

        validate: function() {
            this.clearErrors(['name', 'cover']);

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
                modifyMagician(data)
                    .then(onFinish, onReject)
                    .ensure(onComplete);
            } else {
                addMagician(data)
                    .then(onFinish, onReject)
                    .ensure(onComplete);
            }
        }
    }));

    $(function() {
        MagicianForm.tpl = _.template($("#form-tpl").html());

        var form = new MagicianForm();
        var modal = new modals.FormModal();
        modal.setForm(form);
        $(modal.el).appendTo(document.body);

        $create = $("#create-magician");
        $create.click(function() {
            modal.show();
            modal.setTitle('创建魔术师信息');
            modal.setSaveText("创建", "创建中...");
        });

        var hello = new AjaxUploadWidget($('[name=cover]'), {
            changeButtonText : "修改图片",
            removeButtonText : "删除图片",
            onError: function(data) {
                toast('error', '图片上传失败，请重试。');
            }
        });

        $("table").on("click", ".edit", function() {
            modal.setTitle('编辑魔术师信息');
            modal.setSaveText("保存", "保存中...");
            var magician = $(this).parent().data();
            $('[name=cover]').val(magician.cover).trigger('change');
            form.setMagician(magician);
            modal.show();
        });
    });

    $(function() {
        var modal = new modals.ActionModal();
        modal.setAction(function(id) {
            return deleteMagician(id).then(function() {
                utils.reload(500);
            }, function(err) {
                if (err instanceof errors.AuthFailure) {
                    window.location = "/welcome";
                }

                throw err;
            });
        });
        modal.setTitle('删除魔术师信息');
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
