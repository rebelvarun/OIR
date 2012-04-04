import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models.fields.files import FileField
from django.db.models.signals import post_delete
from django.core.files import File
from os.path import join as pjoin
from tempfile import *

#import Oik.settings
from Oik.settings import MEDIA_ROOT

#Global Variable
item_id_image=0
category_id_image=0


#Different Image Sizes
smallImgSize=(30,30)#where (width,length) tuple
middleImgSize=(100,100)
largeImgSize=(250,250)

#Delete actual uploaded image on deleting museumItem Object
def clean_files(sender, **kwargs):
    for field in sender._meta._fields():
        if isinstance(field, FileField):
            inst = kwargs['instance']
            f = getattr(inst, field.name)
            m = inst.__class__._default_manager
            if os.path.exists(f.path) \
                    and not m.filter(**{'%s__exact' % field.name: getattr(inst, field.name)})\
                    .exclude(pk=inst._get_pk_val()):
                        os.remove(f.path) 


#Overwrite exiting image with new uploaded image 
class OverwriteStorage(FileSystemStorage):
      def get_available_name(self, name):
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

# Model for Museum Owners
class museum(models.Model):
	name=models.CharField(max_length=30)
	address=models.CharField(max_length=100)
       	def __unicode__(self):
		return self.name
        class Meta:
         verbose_name_plural = "Museums"
         verbose_name = "Museum"
#Return Image Paths        
def get_image_category_path(instance, filename):
        ext = filename.split('.')[-1]
        global category_id_image
        filename = "%d.%s" % (category_id_image, ext)
        #filename = "%s.%s" % ("cat, ext)    
        return os.path.join(instance.museum.name,"Category",filename)

class category(models.Model):
	category=models.CharField(max_length=30,null='True')
        #user=models.ForeignKey(User)
        image=models.FileField(upload_to=get_image_category_path,null='True',storage=OverwriteStorage())#Contain Small Image
        caption=models.CharField(max_length=100,null='True')
        description=models.TextField(max_length=200,null='True')
        museum=models.ForeignKey(museum)
        
        def __init__(self, *args, **kwargs):
           

            global category_id_image
            try:
                category_id_image=category.objects.latest('id').id
            except:
                category_id_image=0 
            super(category, self).__init__(*args, **kwargs) 

        def __unicode__(self):
            return self.category

        def thumbnail(self):
            if self.image:
               return '<img src="/media/%s" height=25 width=25 />' %(self.image)
        thumbnail.allow_tags = True
      
        class Meta:
              verbose_name_plural = "Category"
              verbose_name = "Category"
           
        def save(self, *args, **kwargs):
            global category_id_image
            category_id_image=category_id_image+1;
            super(category, self).save(*args, **kwargs)

#Return Image Paths        
def get_image_small_path(instance, filename):
        ext = filename.split('.')[-1]
        global item_id_image
        filename = "%d%s.%s" % (item_id_image,"_small", ext)    
        return os.path.join(instance.museum.name,"img",filename)



#Return Podcast Path
def get_podcast_path(instance, filename):
        ext = filename.split('.')[-1]
        global item_id_image
        filename = "%d.%s" % (item_id_image, ext)    
        return os.path.join(instance.museum.name,"podcast",filename)

   

# Model for Museum Items
class museumItem(models.Model):
	title = models.CharField(max_length=40)
	museum=models.ForeignKey(museum)
	category=models.ForeignKey(category)
	image=models.FileField(upload_to=get_image_small_path,null='True',storage=OverwriteStorage())#Contain Small Image
	synopsis=models.TextField(max_length=100)
	podcast=models.FileField(upload_to=get_podcast_path,null=True,storage=OverwriteStorage())


	def __init__(self, *args, **kwargs):
		global item_id_image
		try:
			item_id_image=museumItem.objects.latest('id').id
		except:
			item_id_image=0 
		super(museumItem, self).__init__(*args, **kwargs) 

	def __unicode__(self):
		return self.title

	def thumbnail(self):
		if self.image:
			return '<img src="/media/%s" height=%s width=%s/>' %(self.image,smallImgSize[1],smallImgSize[0])
	thumbnail.allow_tags = True

	def delete(self, *args, **kwargs):
		self.image.delete()
		super(museumItem, self).delete(*args, **kwargs)

	class Meta:
		verbose_name_plural = "Items"
		verbose_name = "Item"

	def save(self, *args, **kwargs):
		global item_id_image
		item_id_image=item_id_image+1;
		super(museumItem, self).save(*args, **kwargs)
		"""Save image dimensions."""
  
post_delete.connect(clean_files, sender=museumItem )


   
	















