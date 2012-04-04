from django.db import models
from requests.models import museum
import datetime
#from django.utils.timezone import utc

class analyticsData(models.Model):
	time = models.TimeField()
	date = models.DateField()
	userNo = models.IntegerField()
	clickedItem = models.IntegerField()
	itemId = models.IntegerField()