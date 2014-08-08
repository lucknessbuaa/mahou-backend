# coding: utf-8
from django.db import models
from datetime import datetime
#from base.loggers import 

class Magician(models.Model):
    name = models.CharField(verbose_name=u'name',max_length=100)
    cover = models.CharField(verbose_name=u'头像',max_length=1024)

    def __unicode__(self):
        return self.name

class Show(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __unicode__(self):
        return self.pk

class Magician_Show(models.Model):
    magician = models.ForeignKey(Magician,verbose_name=u'magician',max_length=100)
    show = models.ForeignKey(Show,verbose_name=u'show',max_length=100)
    start = models.DateTimeField()
    stop = models.DateTimeField()
    score1 = models.IntegerField(verbose_name=u'score1') 
    score2 = models.IntegerField(verbose_name=u'score2') 
    score3 = models.IntegerField(verbose_name=u'score3')
     
    

