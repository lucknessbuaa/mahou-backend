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
            minuteStep: 1,
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

            //validate
            //选手一
            if(data['name1']==''){
                alert('选手一不能为空！');
                return false;
            }
            if(data['start1'] <= data['start'] || data['start1']==''){
                alert('选手一开始时间应该在节目开始时间之后！');
                return false;
            }else if(data['scoretime1'] <= data['start1'] || data['scoretime1']==''){
                alert('选手一打分时间应该在开始时间之后！');
                return false;
            }else if(data['stop1'] <= data['scoretime1'] || data['stop1']==''){
                alert('选手一结束时间应该在打分时间之后！');
                return false;
            }
            if(data['score11']==0){
                alert('评委一评分不能为空！');
                return false;
            }
            if(data['score21']==0){
                alert('评委二评分不能为空！');
                return false;
            }
            if(data['score31']==0){
                alert('评委三评分不能为空！');
                return false;
            }

            //选手二
            if(data['name2']==''){
                alert('选手二不能为空！');
                return false;
            }
            if(data['name1']==data['name2']){
                alert('选手二重复！');
                return false;
            }
            if(data['start2'] <= data['stop1']||data['start2']==''){
                alert('选手二开始时间应该在选手一开始时间之后！');
                return false;
            }else if(data['scoretime2'] <= data['start2']||data['scoretime2']==''){
                alert('选手二打分时间应该在开始时间之后！');
                return false;
            }else if(data['stop2'] <= data['scoretime2']||data['stop2']==''){
                alert('选手二结束时间应该在打分时间之后！');
                return false;
            }else if(data['score21']== data['score11']||data['score21']==0){
                alert('评委一打分重复！');
                return false;
            }else if(data['score22']== data['score12']|| data['score22']==0){
                alert('评委二打分重复！');
                return false;
            }else if(data['score23']== data['score13']||data['score23']==0){
                alert('评委三打分重复！');
                return false;
            }

            //选手三
            if(data['name3']==''){
                alert('选手三不能为空！');
                return false;
            }
            if(data['name1']==data['name3']||data['name2']==data['name3']){
                alert('选手三重复！');
                return false;
            }
            if(data['start3'] <= data['stop2']||data['start3']==''){
                alert('选手三开始时间应该在选手一开始时间之后！');
                return false;
            }else if(data['scoretime3'] <= data['start3']||data['scoretime3']==''){
                alert('选手三打分时间应该在开始时间之后！');
                return false;
            }else if(data['stop3'] <= data['scoretime3']||data['stop3']==''){
                alert('选手三结束时间应该在打分时间之后！');
                return false;
            }else if(data['score31']== data['score11'] || data['score31']==data['score21'] || data['score31']==0){
                alert('评委一打分重复！');
                return false;
            }else if(data['score32']== data['score12'] || data['score32']==data['score22']|| data['score32']==0){
                alert('评委二打分重复！');
                return false;
            }else if(data['score33']== data['score13'] || data['score33']==data['score23']||data['score33']==0){
                alert('评委三打分重复！');
                return false;
            }

            //选手四
            if(data['name4']==''){
                alert('选手四不能为空！');
                return false;
            }
            if(data['name1']==data['name4']||data['name2']==data['name4']||data['name3']==data['name4']){
                alert('选手四重复！');
                return false;
            }
            if(data['start4'] <= data['stop3']|| data['start4']==''){
                alert('选手四开始时间应该在选手三开始时间之后！');
                return false;
            }else if(data['scoretime4'] <= data['start4']||data['scoretime4'] ==''){
                alert('选手四打分时间应该在开始时间之后！');
                return false;
            }else if(data['stop4'] <= data['scoretime4']||data['stop4']==''){
                alert('选手四结束时间应该在打分时间之后！');
                return false;
            }
            if(data['score41']==0){
                alert('评委一评分不能为空！');
                return false;
            }
            for(var i=1; i<4; i++){
                if(data['score4'+1]==data['score'+i+1]){
                    alert('评委一重复打分！');
                    return false;
                }
            }
            if(data['score42']==0){
                alert('评委二评分不能为空！');
                return false;
            }
            for(var i=1; i<4; i++){
                if(data['score4'+2]==data['score'+i+2]){
                    alert('评委二重复打分！');
                    return false;
                }
            }
            if(data['score43']==0){
                alert('评委三评分不能为空！');
                return false;
            }
            for(var i=1; i<4; i++){
                if(data['score4'+3]==data['score'+i+3]){
                    alert('评委三重复打分！');
                    return false;
                }
            }

            //选手五
            if(data['name5']==''){
                alert('选手五不能为空！');
                return false;
            }
            if(data['name1']==data['name5']||data['name2']==data['name5']||data['name3']==data['name5']||data['name5']==data['name4']){
                alert('选手五重复！');
                return false;
            }
            if(data['start5'] <= data['stop4']|| data['start5']==''){
                alert('选手五开始时间应该在选手四开始时间之后！');
                return false;
            }else if(data['scoretime5'] <= data['start5']||data['scoretime5']==''){
                alert('选手五打分时间应该在开始时间之后！');
                return false;
            }else if(data['stop5'] <= data['scoretime5']||data['stop5']==''){
                alert('选手五结束时间应该在打分时间之后！');
                return false;
            }
            if(data['score51']==0){
                alert('评委一评分不能为空！');
                return false;
            }
            for(var i=1; i<5; i++){
                if(data['score5'+1]==data['score'+i+1]){
                    alert('评委一重复打分！');
                    return false;
                }
            }
            if(data['score52']==0){
                alert('评委二评分不能为空！');
                return false;
            }
            for(var i=1; i<5; i++){
                if(data['score5'+2]==data['score'+i+2]){
                    alert('评委二重复打分！');
                    return false;
                }
            }
            if(data['score53']==0){
                alert('评委三评分不能为空！');
                return false;
            }
            for(var i=1; i<5; i++){
                if(data['score5'+3]==data['score'+i+3]){
                    alert('评委三重复打分！');
                    return false;
                }
            }
            
            //选手六
            if(data['name6']==''){
                alert('选手六不能为空！');
                return false;
            }
            if(data['name1']==data['name6']||data['name2']==data['name6']||data['name3']==data['name6']||data['name6']==data['name4']||data['name5']==data['name6']){
                alert('选手六重复！');
                return false;
            }
            if(data['start6'] <= data['stop5']||data['start6']==''){
                alert('选手六开始时间应该在选手五开始时间之后！');
                return false;
            }else if(data['scoretime6'] <= data['start6']||data['scoretime6']==''){
                alert('选手六打分时间应该在开始时间之后！');
                return false;
            }else if(data['stop6'] <= data['scoretime6']||data['stop6']==''){
                alert('选手六结束时间应该在打分时间之后！');
                return false;
            }
            if(data['score61']==0){
                alert('评委一评分不能为空！');
                return false;
            }
            for(var i=1; i<6; i++){
                if(data['score6'+1]==data['score'+i+1]){
                    alert('评委一重复打分！');
                    return false;
                }
            }
            if(data['score62']==0){
                alert('评委二评分不能为空！');
                return false;
            }
            for(var i=1; i<6; i++){
                if(data['score6'+2]==data['score'+i+2]){
                    alert('评委二重复打分！');
                    return false;
                }
            }
            if(data['score63']==0){
                alert('评委三评分不能为空！');
                return false;
            }
            for(var i=1; i<6; i++){
                if(data['score6'+3]==data['score'+i+3]){
                    alert('评委三重复打分！');
                    return false;
                }
            }
            $this.button('loading');
            if(data['pk']){
                $.post('/backend/new/edit', data, "json").then(function(data) {
                    if (data.ret_code === 0) {
                        alert('修改成功');
                        window.location = '/backend/show';
                    } else {
                        alert('数据错误');
                    }
                }).always(function() {
                    $this.button('reset');
                });

            }else{
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
            }
        });


        function getData() {
            var data = {
                pk: $(form.pk).val(),
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
        $(form.start1).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.start2).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.start3).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.start4).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.start5).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.start6).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.stop1).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.stop2).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.stop3).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.stop4).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.stop5).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.stop6).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.scoretime1).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.scoretime2).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.scoretime3).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.scoretime4).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.scoretime5).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
        $(form.scoretime6).datetimepicker('setStartDate', moment().format("YYYY-MM-DD HH:mm"));
    });
});
