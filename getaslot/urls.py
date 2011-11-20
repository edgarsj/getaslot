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
    
	url(r'^slots/', include(slots.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r"^(?P<slug>[\w-]+)/$", 'slots.views.business', name='business'),
	url(r"^(?P<slug>[\w-]+)/admin/$", 'slots.views.businessAdmin', name='businessAdmin'),
    url(r"^(?P<business>[\w-]+)/appointments/$", 'slots.views.appointments', name="business_appointments"),
	url(r"^(?P<business>[\w-]+)/schedule/$", 'slots.views.busy',{'employee_id':'1'}, name="business_schedule"),
    url(r"^(?P<business>[\w-]+)/schedule/(?P<employee_id>\d+)$", 'slots.views.busy', name="business_schedule_employee"),
    url(r"^(?P<business>[\w-]+)/add_appointment/(?P<employee_id>\d+)/$", 'slots.views.add_appointment_noschedule', name="add_appointment_employee"),
)

urlpatterns += staticfiles_urlpatterns()