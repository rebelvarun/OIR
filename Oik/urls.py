from django.conf.urls.defaults import patterns, include, url
from Oik.settings import MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Oik.views.home', name='home'),
    # url(r'^Oik/', include('Oik.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url(r'^museum/home', 'requests.views.home'),
	url(r'^museum/visitor/login', 'visitors.views.visitorLogin'),
	url(r'^museum/window/tokenCreate', 'visitors.views.tokenCreate'),
	url(r'^museum/window/login', 'visitors.views.windowUserLogin'),
	url(r'^museum/window/logout', 'visitors.views.windowUserLogout'),
	url(r'^museum/podcast/(\d+)/', 'requests.views.get_podcast'),
	url(r'^museum/(\d+)/(\d+)', 'requests.views.get_items'),
	url(r'^museum/(\d+)/', 'requests.views.get_category'),
	#url(r'^admin/analytics', 'graph.views.index'),
        url(r'^grappelli/', include('grappelli.urls')),
        url(r'^admin/', include(admin.site.urls)),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': MEDIA_ROOT}),
)
