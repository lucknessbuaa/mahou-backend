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
from backend.models import Magician
from backend import models
from ajax_upload.widgets import AjaxClearableFileInput


logger = logging.getLogger(__name__)


@require_GET
@login_required
@active_tab('magician')
def magician(request):
    magician = Magician.objects.all()
    search = False
    if 'q' in request.GET and request.GET['q'] <> "":
        logger.error(request.GET['q'])
        magician = magician.filter(Q(name__contains=request.GET['q']))
        if not magician.exists() :
            search = True
    elif 'q' in request.GET and request.GET['q'] == "":
        return HttpResponseRedirect(request.path)
    table = MagicianTable(magician)
    if search:
        table = MagicianTable(magician, empty_text='没有搜索结果')
    form = MagicianForm()
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, "magician.html", {
        "table": table,
        "form": form
    })


class MagicianTable(tables.Table):
    name = tables.columns.Column(verbose_name='姓名', empty_values=(), orderable=False)
    cover = tables.columns.TemplateColumn(verbose_name='头像', template_name='magician_cover.html', orderable=False)
    ops = tables.columns.TemplateColumn(verbose_name='操作', template_name='magician_ops.html', orderable=False)

    class Meta:
        model = Magician
        empty_text = u'没有魔术师信息'
        fields = ("name", "cover")
        attrs = {
            'class': 'table table-bordered table-striped'
        }


class MagicianForm(forms.ModelForm):

    pk = forms.IntegerField(required=False,
        widget=forms.HiddenInput(attrs=us.extend({}, fieldAttrs)))
    name = forms.CharField(label=u"姓名",
        widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        })))

    def clean(self):
        cleaned_data = self.cleaned_data = super(MagicianForm, self).clean()

        return cleaned_data

    class Meta:
        model = Magician
        widgets = {
            'cover': AjaxClearableFileInput
        }


@require_POST
@json
def add_magician(request):
    def _add_magician(form):
        form.save()
        return {'ret_code': RET_CODES["ok"]}

    return with_valid_form(MagicianForm(request.POST), _add_magician)


@require_POST
@json
def delete_magician(request):
    Magician.objects.filter(pk=request.POST["id"]).delete()
    return {'ret_code': RET_CODES['ok']}


@require_POST
@json
def edit_magician(request, id):
    magician = Magician.objects.get(pk=id)
    form = MagicianForm(request.POST, instance=magician)

    def _edit_magician(form):
        form.save()
        return {'ret_code': RET_CODES["ok"]}

    return with_valid_form(form, _edit_magician)

