from django.db import models
from django.utils import timezone
from django.db.models import signals
from django.core.validators import MaxValueValidator, MinValueValidator


class About(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=100)
    jabber = models.CharField(max_length=100)
    skype = models.CharField(max_length=100)
    other_contact = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='imag', null=True, blank=True)

    def __unicode__(self):
        return self.last_name


class AllRequest(models.Model):
    priority = models.IntegerField(validators=[MinValueValidator(0),
                                               MaxValueValidator(9)],
                                   default=0)
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    method = models.CharField(max_length=50)
    path = models.CharField(max_length=200)

    def __unicode__(self):
        return "Request - " + str(self.id)


class SignalData(models.Model):
    date = models.DateTimeField(default=timezone.now)
    message = models.TextField(null=True, blank=True)


from .signals import add_signal_save, add_signal_delete


signals.post_save.connect(add_signal_save, dispatch_uid='SomeText')
signals.post_delete.connect(add_signal_delete, dispatch_uid='SomeText2')
