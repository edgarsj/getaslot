from django.conf.urls.defaults import *

from slots import views

urlpatterns = patterns("",
    # ajax validation
    url(r"^(?P<business>[\w-]+)/appointments/$", views.appointments, name="business_appointments"),
    )

