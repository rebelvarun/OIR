from django.db import models
from django.contrib.auth.models import User
from requests.models import museumItem,museum
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    museum = models.ForeignKey(museum)
    class Meta:
        verbose_name_plural = "Musuem"
        verbose_name = "Musuem"
    def __unicode__(self):
        return ""
    

