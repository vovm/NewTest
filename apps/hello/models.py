from django.db import models
from django.utils import timezone


class About(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date = models.DateField(blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=100)
    jabber = models.CharField(max_length=100)
    skype = models.CharField(max_length=100)
    other_contact = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='imag', blank=True, null=True)

    def __unicode__(self):
        return self.last_name


class AllRequest(models.Model):
    priority = models.IntegerField(max_length=1, default=0)
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    method = models.CharField(max_length=50)
    path = models.CharField(max_length=200)

    def __unicode__(self):
        return "Request - " + str(self.id)


class SignalData(models.Model):
    date = models.DateTimeField(default=timezone.now)
    message = models.TextField(null=True, blank=True)
