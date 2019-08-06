from django.db import models
from django.contrib.auth.models import User, Permission
from django import forms



class UserInterest (models.Model):
    user = models.CharField(max_length=500, null=False)
    origin = models.CharField(max_length=200, null=False)
    destination = models.CharField(max_length=200, null=False)
    searches = models.IntegerField(null=True)


    def __str__(self):
        return self.user + "  searched-> " + self.origin + "  to  "+ self.destination +  "-" + str(self.searches)