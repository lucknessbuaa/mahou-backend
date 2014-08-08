# coding: utf-8
import logging
from datetime import datetime

from underscore import _ as us
from django.db.models import Q
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
@active_tab('new')
def new(request):
    form = NewForm()
    return render(request, "new.html", {
        "form": form
    })

class NewForm(forms.Form):

    start = forms.DateTimeField(label="开始时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    name1 = forms.ModelChoiceField(label=u'姓名', queryset=Magician.objects.all(),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    start1 = forms.DateTimeField(label="开始时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    stop1 = forms.DateTimeField(label=u"结束时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    score11 = forms.ChoiceField(label=u'评分一', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    score12 = forms.ChoiceField(label=u'评分二', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    score13 = forms.ChoiceField(label=u'评分三', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    name2 = forms.ModelChoiceField(label=u'姓名', queryset=Magician.objects.all(),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    start2 = forms.DateTimeField(label="开始时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    stop2 = forms.DateTimeField(label=u"结束时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    score21 = forms.ChoiceField(label=u'评分一', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    score22 = forms.ChoiceField(label=u'评分二', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    score23 = forms.ChoiceField(label=u'评分三', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    name3 = forms.ModelChoiceField(label=u'姓名', queryset=Magician.objects.all(),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    start3 = forms.DateTimeField(label="开始时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    stop3 = forms.DateTimeField(label=u"结束时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    score31 = forms.ChoiceField(label=u'评分一', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    score32 = forms.ChoiceField(label=u'评分二', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    score33 = forms.ChoiceField(label=u'评分三', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    name4 = forms.ModelChoiceField(label=u'姓名', queryset=Magician.objects.all(),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    start4 = forms.DateTimeField(label="开始时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    stop4 = forms.DateTimeField(label=u"结束时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    score41 = forms.ChoiceField(label=u'评分一', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    score42 = forms.ChoiceField(label=u'评分二', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    score43 = forms.ChoiceField(label=u'评分三', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    name5 = forms.ModelChoiceField(label=u'姓名', queryset=Magician.objects.all(),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    start5 = forms.DateTimeField(label="开始时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    stop5 = forms.DateTimeField(label=u"结束时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    score51 = forms.ChoiceField(label=u'评分一', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    score52 = forms.ChoiceField(label=u'评分二', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    score53 = forms.ChoiceField(label=u'评分三', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    name6 = forms.ModelChoiceField(label=u'姓名', queryset=Magician.objects.all(),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    start6 = forms.DateTimeField(label="开始时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    stop6 = forms.DateTimeField(label=u"结束时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    score61 = forms.ChoiceField(label=u'评分一', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    score62 = forms.ChoiceField(label=u'评分二', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    score63 = forms.ChoiceField(label=u'评分三', choices=((0,'---'), (1,'A'), (3,'3'), (5,'5'), (7,'7'), (9,'9'), (11,'J'), (13,'K')),
        widget=forms.Select(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    stop = forms.DateTimeField(label=u"结束时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    def clean(self):
        cleaned_data = self.cleaned_data = super(ShowForm, self).clean()

        return cleaned_data

