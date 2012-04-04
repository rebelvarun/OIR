
from requests.models import museumItem,museum,category
from accounts.models import UserProfile
from django.contrib import admin
from django.db import models
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from django import forms
from uuid import uuid4 as uuid
#from django.contrib.sessions.models import Session

class MuseumItemAdmin(admin.ModelAdmin):
  def formfield_for_foreignkey(self, db_field, request, **kwargs):
   if db_field.name == "category":
      kwargs["queryset"] = category.objects.filter(museum=request.user.get_profile().museum)
      return db_field.formfield(**kwargs)

  #Limiting museum items display/edit on the basis of user logged-in
  def queryset(self, request):
   return museumItem.objects.filter(museum=request.user.get_profile().museum)

  #Display of Museum Items
  fields = ('title', 'image','podcast','synopsis','category')
  list_display = ('title','category', 'thumbnail','synopsis',)
  #list_editable = ('category','image','synopsis')
  #list_filter = ['category']
  search_fields = ['title']
  
  #Disallow oik admin to edit/add/delete museum Item
  def has_add_permission(self, request):  
      if request.user.is_superuser:   
         return False
      else:
         return True
  def has_change_permission(self, request,obj=None):
      if request.user.is_superuser:   
         return False
      else:
         return True 
  def has_delete_permission(self, request,obj=None):
      if request.user.is_superuser:   
         return False
      else:
         return True

  #To save museumitem.museum_id automatically to user logged in
  def save_model(self, request, obj, form, change):
      obj.museum = request.user.get_profile().museum
      obj.save()



admin.site.unregister(User)


class CategoryInline(admin.TabularInline):
    model = category
    max_num = 1

'''
class CustomUserCreationForm(forms.ModelForm):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField( max_length=30, blank=True)
    email = models.EmailField( blank=True)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField( default=False,)
    is_active = models.BooleanField( default=True,)
    is_superuser = models.BooleanField(default=False)
    museum_name=forms.CharField(required=False)
    museum_address=forms.CharField(required=False)
		
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','is_staff','is_superuser','museum_name', 'museum_address',)

    def clean_email(self):
        email = self.cleaned_data["email"]
        return email

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(user.password)
        user.save()
        if self.cleaned_data["museum_name"]!="" and self.cleaned_data["museum_address"]!="":
           museumObject=museum.objects.create(name=self.cleaned_data["museum_name"],address=self.cleaned_data["museum_address"])
	   UserProfile.objects.create(user=user,museum=museumObject)
        return user
'''
class ProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    max_num = 1
    
class CustomUserAdmin(UserAdmin):
    list_display = ('username','email','first_name', 'last_name', 'is_staff',
    )   
    inlines = [ProfileInline,]
    list_filter = ('username',)
        
'''
class CustomUserAdmin(UserAdmin):
     list_filter = ('is_superuser','is_staff')
     _list_filter = list_filter
     add_form = CustomUserCreationForm
     def changelist_view(self, request, extra_context=None):
    
         if request.user.is_superuser:
            self.add_fieldsets = (
                (('Personal info'), {'fields': ('username','password',)}),
                (('Musuem'),{'fields':('museum_name','museum_address')}),
            )
            self.list_display =['username','is_staff','is_superuser']
            self.fieldsets = (
       	        (None, {'fields': ('username',)}),
                      
             )
            self.list_filter = self._list_filter
              
         else:
            self.add_fieldsets = (
                (None, {'fields': ('username','password')}),
            )
            self.list_display =['username']
	    self.fieldsets = (
       	         (None, {'fields': ( 'username',)}),
            )
            self.list_filter = None
         
         return super(CustomUserAdmin, self).changelist_view(request, extra_context)
 
     def save_model(self, request, obj, form, change):
		#obj.save()
		if request.user.is_superuser:
			add_user = Permission.objects.get(codename="add_user")
			change_user = Permission.objects.get(codename="change_user")
			delete_user = Permission.objects.get(codename="delete_user")
			delete_userprofile = Permission.objects.get(codename="delete_userprofile") 
			add_museumitem = Permission.objects.get(codename="add_museumitem")
			change_museumitem = Permission.objects.get(codename="change_museumitem")
			delete_museumitem = Permission.objects.get(codename="delete_museumitem")
                        add_category = Permission.objects.get(codename="add_category")
			change_category = Permission.objects.get(codename="change_category")
			delete_category = Permission.objects.get(codename="delete_category")
                        obj.user_permissions.add(add_user,change_user,delete_user,delete_userprofile,add_museumitem,change_museumitem,delete_museumitem,add_category,
						 change_category,delete_category)
			obj.is_staff=1
                        obj.is_superuser=0
			obj.save()
                        
		#Create UserProfile object and assign museum_id in it
		if request.user.is_staff==1 and request.user.is_superuser==0:
			requestProfile=request.user.get_profile()
			if requestProfile.museum is not None:
				userprofile=UserProfile.objects.get_or_create(user=obj,museum=requestProfile.museum)
                


     def queryset(self, request):
         if request.user.is_superuser==1:
            return User.objects.filter(is_staff=1)
         else:
            wanted_items = set()
            for item in UserProfile.objects.all():
                if item.museum==request.user.get_profile().museum:
                   wanted_items.add(item.user.id)
         return User.objects.filter(id__in = wanted_items)
         
         
         
         
         
'''         

class CategoryAdmin(admin.ModelAdmin):
        #Disallow oik admin to edit/add/delete museum Item
  fields = ('category','image','caption','description',)
  list_display =  ('category','thumbnail','caption','description')

  #Limiting museum items display/edit on the basis of user logged-in
  def queryset(self, request):
   return category.objects.filter(museum=request.user.get_profile().museum)
  def has_add_permission(self, request):  
      if request.user.is_superuser:   
         return False
      else:
         return True
  def has_change_permission(self, request,obj=None):
      if request.user.is_superuser:   
         return False
      else:
         return True 
  def has_delete_permission(self, request,obj=None):
      if request.user.is_superuser:   
         return False
      else:
         return True
  def save_model(self, request, obj, form, change):
      obj.museum=request.user.get_profile().museum
      obj.save()
 
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(museumItem,MuseumItemAdmin)
#admin.site.register(museum,MuseumAdmin)
admin.site.register(category,CategoryAdmin)
admin.site.register(museum)
#admin.site.register(Session,SessionAdmin)


