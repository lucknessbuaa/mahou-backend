# coding: utf-8
import logging
from datetime import datetime

from underscore import _ as us
from django.db.models import Q
from django.db import connection
from django import forms
from django.core.cache import get_cache
from django.core.urlresolvers import reverse
from django.db import InternalError
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.conf import settings 
from django.utils.safestring import mark_safe
import django_tables2 as tables
from django_tables2 import RequestConfig
from django_render_json import json
from django.http import HttpResponseRedirect

from base.decorators import active_tab
from base.utils import fieldAttrs, with_valid_form, RET_CODES
from backend.models import Magician, Show, Magician_Show
from backend import models
from ajax_upload.widgets import AjaxClearableFileInput

logger = logging.getLogger(__name__)

@require_GET
@login_required
@active_tab('show')
def show(request):
    show =  Magician_Show.objects.all()
    show.order_by('-show')
    search = False
    if 'q' in request.GET and request.GET['q'] <> "":
        logger.error(request.GET['q'])
        show = show.filter(Q(speaker__contains=request.GET['q'])|\
	Q(university__name__contains=request.GET['q'])|\
	Q(university__city_id__name__contains=request.GET['q'])|\
	Q(place__contains=request.GET['q']))
        if not show.exists() :
            search = True
    elif 'q' in request.GET and request.GET['q'] == "":
        return HttpResponseRedirect(request.path)
    table = ShowTable(show)
    if search :
        table = ShowTable(show, empty_text='没有搜索结果')
    form = ShowForm()
    RequestConfig(request, paginate={"per_page": 6}).configure(table)
    return render(request, "show.html", {
        "table": table,
        "form": form
    })


class ShowTable(tables.Table):

    pk = tables.columns.Column(verbose_name='顺序', empty_values=(), orderable=False)
    magician = tables.columns.Column(verbose_name='姓名', empty_values=(), orderable=False)
    cover = tables.columns.TemplateColumn(verbose_name='头像', template_name='show_cover.html', orderable=False, accessor='magician.cover')
    show = tables.columns.Column(verbose_name='节目期数', empty_values=(), orderable=False)
    start = tables.columns.DateTimeColumn(verbose_name='开始时间', empty_values=(), orderable=False, format='Y-m-d H:i')
    stop = tables.columns.DateTimeColumn(verbose_name='结束时间', empty_values=(), orderable=False, format='Y-m-d H:i')
    score1 = tables.columns.Column(verbose_name='评分一', empty_values=(), orderable=False)
    score2 = tables.columns.Column(verbose_name='评分二', empty_values=(), orderable=False)
    score3 = tables.columns.Column(verbose_name='评分三', empty_values=(), orderable=False)
    ops = tables.columns.TemplateColumn(verbose_name='操作', template_name='show_ops.html', orderable=False)

    class Meta:
        model = Magician_Show
        empty_text = u'没有节目信息'
        fields = ('pk', 'show', 'magician', 'cover', 'start', 'stop', 'score1', 'score2', 'score3', 'ops') 
        attrs = {
            'class': 'table table-bordered table-striped'
        }


class ShowForm(forms.ModelForm):

    pk = forms.IntegerField(required=False,
        widget=forms.HiddenInput(attrs=us.extend({}, fieldAttrs)))

    magician = forms.ModelChoiceField(label=u'姓名', queryset=Magician.objects.all(),
        widget=forms.HiddenInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    show = forms.ModelChoiceField(label=u'节目期数', queryset=Show.objects.all(),
        widget=forms.HiddenInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    start = forms.DateTimeField(label="开始时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    stop = forms.DateTimeField(label=u"结束时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    score1 = forms.ChoiceField(label=u'评分一', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    score2 = forms.ChoiceField(label=u'评分二', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    score3 = forms.ChoiceField(label=u'评分三', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    def clean(self):
        cleaned_data = self.cleaned_data = super(ShowForm, self).clean()

        return cleaned_data

    class Meta:
        model = Magician_Show


@require_POST
@json
def add_show(request):
    start = request.POST["data[start]"]

    name1 = request.POST["data[name1]"]
    start1 = request.POST['data[start1]']
    stop1 = request.POST["data[stop1]"]
    score11 = request.POST['data[score11]']
    score12 = request.POST['data[score12]']
    score13 = request.POST['data[score13]']

    name2 = request.POST["data[name2]"]
    start2 = request.POST['data[start2]']
    stop2 = request.POST["data[stop2]"]
    score21 = request.POST['data[score21]']
    score22 = request.POST['data[score22]']
    score23 = request.POST['data[score23]']

    name3 = request.POST["data[name3]"]
    start3 = request.POST['data[start3]']
    stop3 = request.POST["data[stop3]"]
    score31 = request.POST['data[score31]']
    score32 = request.POST['data[score32]']
    score33 = request.POST['data[score33]']

    name4 = request.POST["data[name4]"]
    start4 = request.POST['data[start4]']
    stop4 = request.POST["data[stop4]"]
    score41 = request.POST['data[score41]']
    score42 = request.POST['data[score42]']
    score43 = request.POST['data[score43]']

    name5 = request.POST["data[name5]"]
    start5 = request.POST['data[start5]']
    stop5 = request.POST["data[stop5]"]
    score51 = request.POST['data[score51]']
    score52 = request.POST['data[score52]']
    score53 = request.POST['data[score53]']

    name6 = request.POST["data[name6]"]
    start6 = request.POST['data[start6]']
    stop6 = request.POST["data[stop6]"]
    score61 = request.POST['data[score61]']
    score62 = request.POST['data[score62]']
    score63 = request.POST['data[score63]']

    end = request.POST['data[stop]']

    cursor = connection.cursor()

    cursor.execute("insert into backend_show(start, end) values(%s,%s)", [start, end])
    cursor.execute("select id from backend_show where start = %s", [start])
    show = cursor.fetchone()
    cursor.execute("insert into backend_magician_show(magician_id, show_id, start, stop, score1,score2, score3) values(%s,%s,%s,%s,%s,%s,%s)", [name1, show, start1, stop1, score11, score12, score13])
    cursor.execute("insert into backend_magician_show(magician_id, show_id, start, stop, score1,score2, score3) values(%s,%s,%s,%s,%s,%s,%s)", [name2, show, start2, stop2, score21, score22, score23])
    cursor.execute("insert into backend_magician_show(magician_id, show_id, start, stop, score1,score2, score3) values(%s,%s,%s,%s,%s,%s,%s)", [name3, show, start3, stop3, score31, score32, score33])
    cursor.execute("insert into backend_magician_show(magician_id, show_id, start, stop, score1,score2, score3) values(%s,%s,%s,%s,%s,%s,%s)", [name4, show, start4, stop4, score41, score42, score43])
    cursor.execute("insert into backend_magician_show(magician_id, show_id, start, stop, score1,score2, score3) values(%s,%s,%s,%s,%s,%s,%s)", [name5, show, start5, stop5, score51, score52, score53])
    cursor.execute("insert into backend_magician_show(magician_id, show_id, start, stop, score1,score2, score3) values(%s,%s,%s,%s,%s,%s,%s)", [name6, show, start6, stop6, score61, score62, score63])
    
    return {'ret_code': REET_CODES["ok"]} 
    


@require_POST
@json
def delete_show(request):
    speaker = forms.CharField(label=u"主讲人", required=False,
        widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        })))

    wtdate = forms.DateTimeField(label=u"结束时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    def clean(self):
        cleaned_data = self.cleaned_data = super(ShowForm, self).clean()

        if cleaned_data["capacity"] > 2000:
            raise ValidationError('座位数应该在2000以下！')
       
        if cleaned_data["cover"] == "False":
            raise ValidationError('地点图片不能为空！')

        return cleaned_data

    class Meta:
        model = Talk
        widgets = {
            'cover': AjaxClearableFileInput
        }

@require_POST
@json
def edit_show(request, id):
    show = Magician_Show.objects.get(pk=id)
    form = ShowForm(request.POST, instance=show)

    def _edit_show(form):
        form.save()
        return {'ret_code': RET_CODES["ok"]}

    return with_valid_form(form, _edit_show)

@require_POST
@json
def requireMag(request):
    selectMag = Magician.objects.all()

    def mapMag(mag):
        return {
            'id': str(mag.pk),
            'type': 'magician',
            'name': mag.name,
            'text': mag.name
        }

    selectMag = map(mapMag, selectMag)
    return {
        'ret_code': RET_CODES['ok'],
        'selectMag': selectMag
    }
