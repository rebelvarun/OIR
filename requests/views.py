from django.http import HttpResponse
from django.template.loader import render_to_string
from requests.models import *
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
# Create your views here.

def home(request):
	return render_to_response('index.html')

def get_category(request,id):
	items = category.objects.filter(museum__id=id)
	if items:
		xml = '<?xml version="1.0" standalone="yes"?> <slider>'
		for item in items:
			xml=xml+category_xml(item)
		
		xml=xml+'</slider>'
		return HttpResponse(xml)
	else:
		return HttpResponse("Error")
		
def get_items(request,museumId,categoryId):
	items = museumItem.objects.filter(museum__id=museumId).filter(category__id=categoryId)
	itemsCount = museumItem.objects.filter(museum__id=museumId).filter(category__id=categoryId).count()
	if items:
		xml = '<?xml version="1.0" standalone="yes"?> <musuem> <number_of_results>'+str(itemsCount)+'</number_of_results>'
		for item in items:
			xml=xml+item_xml(item)
		
		xml=xml+'</musuem>'
		return HttpResponse(xml)
	else:
		return HttpResponse("Error")
		
def get_podcast(request,museumId):
	categories = category.objects.filter(museum__id=museumId)
	xml = '<?xml version="1.0" standalone="yes"?> <museum>'
	for categry in categories:
		xml = xml + '<category name="'+categry.category+'">'
		items = museumItem.objects.filter(category__id=categry.id)
		
		for item in items:
			xml = xml + podcast_xml(item)
		
		xml = xml + '</category>'
	
	xml = xml + '</museum>'
	
	return HttpResponse(xml)
		
		

def podcast_xml(item):
    xml = render_to_string('podcast.xml', {'item': item})
    return xml
	
def category_xml(item):
    xml = render_to_string('category.xml', {'item': item})
    return xml

def item_xml(item):
    xml = render_to_string('item_info.xml', {'item': item})
    return xml
