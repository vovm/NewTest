from django.db import models


class About(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date = models.DateField(blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=100)
    jabber = models.CharField(max_length=100)
    skype = models.CharField(max_length=100)
    other_contact = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.last_name
