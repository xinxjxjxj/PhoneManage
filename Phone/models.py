from __future__ import unicode_literals
from django.db import models
import django.utils.timezone as timezone
from django.contrib import admin

# Create your models here.
class Android(models.Model):
    brand = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50)
    Android_version = models.CharField(max_length=50, blank=True)
    Physical_size = models.CharField(max_length=50, blank=True)
    owner = models.CharField(max_length=50, blank=True)
    status = models.BooleanField()
    createdtime = models.DateTimeField(default = timezone.now)
    modifiedtime = models.DateTimeField(auto_now = True)
    system = models.CharField(max_length=50, default='Android')
    applicant = models.CharField(max_length=50, blank=True)
    breakdown = models.BooleanField(default=True)
    assetnum = models.CharField(max_length=50, blank=True)
    
    def __unicode__(self):
        return self.name
    
class iOS(models.Model):
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=50, blank=True)
    iOS_version = models.CharField(max_length=50, blank=True)
    Physical_size = models.CharField(max_length=50, blank=True)
    owner = models.CharField(max_length=50, blank=True)
    status = models.BooleanField()
    createdtime = models.DateTimeField(default = timezone.now)
    modifiedtime = models.DateTimeField(auto_now = True)
    system = models.CharField(max_length=50, default='iOS')
    applicant = models.CharField(max_length=50, blank=True)
    breakdown = models.BooleanField(default=True)
    assetnum = models.CharField(max_length=50, blank=True)
    
    def __unicode__(self):
        return self.name
    
class borrowHistory(models.Model):
    devicename = models.CharField(max_length=50)
    owner= models.CharField(max_length=50)
    managername = models.CharField(max_length=50)
    status = models.BooleanField()
    createdtime = models.DateTimeField(default = timezone.now)
    modifiedtime = models.DateTimeField(auto_now = True)
    assetnum = models.CharField(max_length=50, blank=True)
    
    def __unicode__(self):
        return self.devicename
