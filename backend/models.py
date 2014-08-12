# coding: utf-8
from django.db import models
from datetime import datetime
#from base.loggers import 


class Magician(models.Model):
    name = models.CharField(verbose_name=u'名称',max_length=100)
    cover = models.CharField(verbose_name=u'头像',max_length=1024)
    remove = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Show(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    remove = models.BooleanField(default=False)

    def __unicode__(self):
        return self.pk


class Magician_Show(models.Model):
    magician = models.ForeignKey(Magician,verbose_name=u'魔术师',max_length=100)
    show = models.ForeignKey(Show,verbose_name=u'show',max_length=100)
    start = models.DateTimeField()
    scoretime = models.DateTimeField()
    stop = models.DateTimeField()
    score1 = models.IntegerField(verbose_name=u'score1') 
    score2 = models.IntegerField(verbose_name=u'score2') 
    score3 = models.IntegerField(verbose_name=u'score3')
    remove = models.BooleanField(default=False)
     
    
class Audience(models.Model):
    token = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)


class AudienceScore(models.Model):
    audience = models.ForeignKey(Audience)
    show = models.ForeignKey(Show)
    magician = models.ForeignKey(Magician)

    score = models.IntegerField()

    class Meta:
        unique_together=("audience", "show", "magician")


class AudienceAccuracy(models.Model):
    audience = models.ForeignKey(Audience)
    show = models.ForeignKey(Show)
    
    accuracy = models.IntegerField(default=0)

    class Meta:
        unique_together=("audience", "show")
