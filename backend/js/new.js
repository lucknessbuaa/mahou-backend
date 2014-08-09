define(function(require) {
    require("jquery");
    require("jquery.serializeObject");
    require("jquery.iframe-transport");
    require("ajax_upload"),
    require("bootstrap");
    require("moment");
    require("bootstrap-datetimepicker");
    require("zh-CN");
    require("select2");
    require("parsley");
    var csrf_token = require("django-csrf-support");

    $(function() {
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
        for (i = 1; i <= 6; i++) {
            $("#id_start" + i).datetimepicker({
                maxView: 2,
                minView: 0,
                language: 'zh-CN',
                format: 'yyyy-mm-dd hh:ii',
                viewSelect: 'month',
                autoclose: "true",
                minuteStep: 1,
            });
        }
        for (i = 1; i <= 6; i++) {
            $("#id_scoretime" + i).datetimepicker({
                maxView: 2,
                minView: 0,
                language: 'zh-CN',
                format: 'yyyy-mm-dd hh:ii',
                viewSelect: 'month',
                autoclose: "true",
                minuteStep: 1,
            });
        }
        for (i = 1; i <= 6; i++) {
            $("#id_stop" + i).datetimepicker({
                maxView: 2,
                minView: 0,
                language: 'zh-CN',
                format: 'yyyy-mm-dd hh:ii',
                viewSelect: 'month',
                autoclose: "true",
                minuteStep: 1,
            });
        }

        $(form.hello).click(function() {
            var data = getData();
            var $this = $(this);

            $this.button('loading');
            $.post('/backend/new/add', data, "json").then(function(data) {
                if (data.ret_code === 0) {
                    alert('创建成功');
                    window.location = '/backend/show';
                } else {
                    alert('数据错误');
                }
            }).always(function() {
                $this.button('reset');
            });
        });

        function getData() {
            var data = {
                start: $(form.start).val(),

                name1: $(form.name1).val(),
                start1: $(form.start1).val(),
                scoretime1: $(form.scoretime1).val(),
                stop1: $(form.stop1).val(),
                score11: $(form.score11).val(),
                score12: $(form.score12).val(),
                score13: $(form.score13).val(),

                name2: $(form.name2).val(),
                start2: $(form.start2).val(),
                scoretime2: $(form.scoretime2).val(),
                stop2: $(form.stop2).val(),
                score21: $(form.score21).val(),
                score22: $(form.score22).val(),
                score23: $(form.score23).val(),

                name3: $(form.name3).val(),
                start3: $(form.start3).val(),
                scoretime3: $(form.scoretime3).val(),
                stop3: $(form.stop3).val(),
                score31: $(form.score31).val(),
                score32: $(form.score32).val(),
                score33: $(form.score33).val(),

                name4: $(form.name4).val(),
                start4: $(form.start4).val(),
                scoretime4: $(form.scoretime4).val(),
                stop4: $(form.stop4).val(),
                score41: $(form.score41).val(),
                score42: $(form.score42).val(),
                score43: $(form.score43).val(),

                name5: $(form.name5).val(),
                start5: $(form.start5).val(),
                scoretime5: $(form.scoretime5).val(),
                stop5: $(form.stop5).val(),
                score51: $(form.score51).val(),
                score52: $(form.score52).val(),
                score53: $(form.score53).val(),

                name6: $(form.name6).val(),
                start6: $(form.start6).val(),
                scoretime6: $(form.scoretime6).val(),
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
