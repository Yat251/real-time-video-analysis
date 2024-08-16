from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import datetime
import random


def video_upload_path(instance,filename):
    extension = filename.split('.')[-1]
    print(instance, instance.title, extension)
    # new_filename = "/uploads/%d-%d-%s-%d.%s" % (instance.ca_id, instance.task_id, datetime.datetime.now(), random.randint(0,10000), extension)
    new_filename = "%s-%d.%s" % (instance.title, random.randint(0,10000), extension)
    return '/'.join(['videos', new_filename])
    # return new_filename

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=255)
    videofile= models.FileField(upload_to=video_upload_path)
    watches = models.IntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class UserEvent(models.Model):
    user = models.IntegerField()
    video = models.IntegerField()
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserSession(models.Model):
    user = models.IntegerField()
    session = models.IntegerField()
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

