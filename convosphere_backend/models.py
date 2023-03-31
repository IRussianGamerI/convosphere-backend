from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.CharField(max_length=1000, blank=True, null=False)


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    sender = models.ForeignKey(User, models.DO_NOTHING, blank=False, null=False)
    topic = models.ForeignKey(Topic, models.DO_NOTHING, blank=False, null=False)
    text = models.TextField(blank=False, null=False)
    sent_time = models.DateTimeField(blank=False, null=False, default=timezone.now)
    edit_time = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(blank=False, null=False, default=False)
