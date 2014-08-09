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
from backend.models import Magician, Show, Magician_Show, Audience, AudienceScore, AudienceAccuracy
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
    scoretime = tables.columns.DateTimeColumn(verbose_name='打分时间', empty_values=(), orderable=False, format='Y-m-d H:i')
    stop = tables.columns.DateTimeColumn(verbose_name='结束时间', empty_values=(), orderable=False, format='Y-m-d H:i')
    score1 = tables.columns.Column(verbose_name='评分一', empty_values=(), orderable=False)
    score2 = tables.columns.Column(verbose_name='评分二', empty_values=(), orderable=False)
    score3 = tables.columns.Column(verbose_name='评分三', empty_values=(), orderable=False)
    ops = tables.columns.TemplateColumn(verbose_name='操作', template_name='show_ops.html', orderable=False)

    def render_score1(score1, value):
        if value == 1:
            return 'A'
        elif value == 11:
            return 'J'
        elif value == 13:
            return 'K'
        else:
            return value

    def render_score2(score2, value):
        if value == 1:
            return 'A'
        elif value == 11:
            return 'J'
        elif value == 13:
            return 'K'
        else:
            return value

    def render_score3(score3, value):
        if value == 1:
            return 'A'
        elif value == 11:
            return 'J'
        elif value == 13:
            return 'K'
        else:
            return value

    class Meta:
        model = Magician_Show
        empty_text = u'没有节目信息'
        fields = ('pk', 'show', 'magician', 'cover', 'start', 'scoretime', 'stop', 'score1', 'score2', 'score3', 'ops') 
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

    scoretime = forms.DateTimeField(label="打分时间", input_formats=["%Y-%m-%d %H:%M"],
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


def ensureAudience(token):
    audience = None
    try:
        audience = Audience.objects.get(token=token)
    except:
        audience = Audience(token=token)
        audience.save()

    return audience


@require_POST
@json
def record_mobile(request):
    token = request.POST.get('token', None)
    phone = request.POST.get('phone', None)

    if not phone or not token:
        return {'ret_code': 1001}

    audience = ensureAudience(token)
    audience.phone = phone
    audience.save()

    return {'ret_code': 0}


@require_POST
@json
def record_score(request):
    token = request.POST.get('token', None)
    show_id = request.POST.get('show_id', None)
    magician_id = request.POST.get('magician_id', None)
    score = request.POST.get('score', None)

    if not phone or not token or not show_id or not score:
        return {'ret_code': 1001}

    audience = ensureAudience(token)
    show = Show.objects.get(pk=show_id)
    magician = Magician.objects.get(pk=magician_id)

    AudienceScore(audience=audience, show=show, magician=magician, score=score).save()
    # TODO add accuracy
    score3 = Magician_Show.objects.get(magician=magician, shhow=show)
    if score == score3.score3:
        audience.score += 1
     
    return {'ret_code': 0}

def magician_score(request):
    show_id = request.POST.get('show_id', None)
    magician_id = request.POST.get('magician_id', None)
    
    if not show_id or not magician_id:
        return {'ret_code': 1001}

    magician = Magician.objects.get(pk=magician_id)
    show = Show.objects.get(pk=show_id)
    scores = AudienceScore(show=show, magician=magician)
    def mapScore(scores):
        score1 = 0
        score3 = 0
        score5 = 0
        score7 = 0
        score9 = 0
        score11 = 0
        score13 = 0
    
        for item in scores:
           'score' + str(item.score) += 1

        sum = score1 + score3 + score5 + score7 + score9 +score11 + score13
        if sum == 0:
            per1 = 0
            per3 = 0
            per5 = 0
            per7 = 0
            per9 = 0
            per11 = 0
            per13 = 0
        else:
            per1 = 1.0 * per1 / sum
            per3 = 1.0 * per3 / sum
            per5 = 1.0 * per5 / sum
            per7 = 1.0 * per7 / sum
            per9 = 1.0 * per9 / sum
            per11 = 1.0 * per11 / sum
            per13 = 1.0 * per13 / sum
        return {
            'scoreA': per1,
            'score3': per3,
            'score5': per5,
            'score7': per7,
            'score9': per9,
            'scoreJ': per11,
            'scoreK': per13,
        }

  percent = map(mapScore, scores)
  return{
      'ret_code': 0,
      'percent': percent,
  }


def accuracy(request):
    token = request.POST.get('token', None)
    show_id = request.POST.get('show_id', None)

    audience = ensureAudience(token)
    auScore = AudienceScore.objects.get(pk=show_id)
    magician = Magician_Show.objects.get(pk=show_id)
    def mapAuScore(auScore):
        score1 = 0
        score2 = 0
        score3 = 0
        score4 = 0
        score5 = 0
        score6 = 0

        scoreA1 = 0
        scoreA2 = 0
        scoreA3 = 0
        scoreA4 = 0
        scoreA5 = 0
        scoreA6 = 0

        for subitem in magician:
            i = 1
            for item in auScore:
                if item.magician == subitem.magician






















