from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import slots.urls

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
	url(r'^$', 'views.index'),
	url(r'^about/', 'views.about'),
    url(r"^(?P<slug>[\w-]+)/$", 'slots.views.business', name='business'),
	url(r'^slots/', include(slots.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()