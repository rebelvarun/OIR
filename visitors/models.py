from django.db import models
from requests.models import museum
import datetime
#from django.utils.timezone import utc


#Expiry Time is 60 min
expiry_period=3600


class visitorToken(models.Model):
	visitorToken=models.CharField(null=False, blank=False,primary_key=True,max_length=6,unique=True)
	museum=models.ForeignKey(museum,null=True)
	time_created=models.DateTimeField()
	login_time=models.DateTimeField(null=True)
	token_expiry_time=models.DateTimeField(null=True)


class session(models.Model):
	key=models.CharField(primary_key=True,max_length=40)
	visitortoken=models.ForeignKey(visitorToken,null=True)
	last_request_time=models.DateTimeField(null=True)
  

 
    

