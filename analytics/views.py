from django.http import HttpResponse
from django.shortcuts import render_to_response
from visitors.models import visitorToken, session
from analytics.models import analyticsData
from requests.models import museumItem
from django.contrib.auth import authenticate, login
from django.template import RequestContext, loader
import datetime
import uuid
import math
#from django.utils.timezone import utc
from django.contrib.auth import logout
TOOLBAR=1
MUSEUMITEM=2
CATEGORY=3
PODCAST=4

def DumpData(request):
	if request.method == 'POST' :
		time_now=datetime.datetime.utcnow().time()
		date_now=datetime.date.today()
		key = request.POST['key']
		userNo = session.objects.get(key=key).visitortoken.userNo
		clickedItem = request.POST['clickedItem']
		itemid = request.POST['itemId']
		analyticsData.objects.create(time=time_now,date=date_now,userNo=userNo,clickedItem=clickedItem,itemId=itemId)
		
def getPodcastPlays(request):
	objs = analyticsData.objects.filter(clickedItem=PODCAST).values('itemId').annotate(count=Count('itemId')).order_by('-count')
	str = '<podcast_play>'
	for obj in objs:
		itemId = int(obj['itemId'])
		itemName = museumItem.objects.get(id=itemId).name
		str = str + '<museum_item><plays>%d</plays><item_name>%s</item_name></museum_item>' % (int(obj['count']),itemName)
	
	str = str + '</podcast_play>'
	
	return HttpResponse(str)
	

def getUserPerDay(request):
	day = request.POST['startDate']
	month = request.POST['startMonth']
	year = request.POST['startYear']
	startDate = datetime.date(year,month,day)
	day = request.POST['endDate']
	month = request.POST['endMonth']
	year = request.POST['endYear']
	endDate = datetime.date(year,month,day)
	objs = analyticsData.objects.filter(date__gt=startDate).filter(date__lt=endDate).values('date_now').annotate(count=Count('userNo')).order_by('-count')
	
	str = '<users_per_day>'
	for obj in objs:
		itemId = int(obj['itemId'])
		itemName = museumItem.objects.get(id=itemId).name
		str = str + '<day><date>%s</date><number_of_users>%d</number_of_users></day>' % (obj['date_now'].strftime('%d %B'),int(obj['count']))
		
	str = str + '</users_per_day>'
		
	return HttpResponse(str)

def getUserPerTime(request):
	day = request.POST['date']
	month = request.POST['month']
	year = request.POST['year']
	date = datetime.date(year,month,day)
	
	str = '<users_per_time>'
	
	for i in range(24):
		gtTime = datetime.time(i,0)
		ltTime = datetime.time(i,59,59)
		count = analyticsData.objects.filter(date=date).filter(time__lte=ltTime).filter(time__gte=gtTime).count()
		str = str + '<time_instance><time>%s</time><number_of_users>%d</number_of_users></time_instance>' % (gtTime.strftime("%H:%M"),count))
	
	str = str + '</users_per_time>'
	
	return HttpResponse(str)
		

def getClicks(request):
	objs = analyticsData.objects.filter(clickedItem=MUSEUMITEM).values('itemId').annotate(count=Count('itemId')).order_by('-count')
	str = '<clicks_item>'
	for obj in objs:
		itemId = int(obj['itemId'])
		itemName = museumItem.objects.get(id=itemId).name
		str = str + '<museum_item><clicks>%d</clicks><item_name>%s</item_name></museum_item>' % (int(obj['count']),itemName)
	
	str = str + '</clicks_item>'
	
	return HttpResponse(str)
	
def getLikes(request):
	objs = museumItem.objects.all().order_by('-likes')
	str = '<likes_item>'
	
	for obj in objs:
		str = str + '<museum_item><likes>%d</likes><item_name>%s</item_name></museum_item>' % (obj.likes,obj.name)
		
	str = str + '</likes_item>'
	
	return HttpResponse(str)