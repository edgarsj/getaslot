from django.contrib import admin
from slots.models import Business, BusinessEmployee, Appointment, WorkSchedule

admin.site.register(Business)
admin.site.register(BusinessEmployee)
admin.site.register(Appointment)
admin.site.register(WorkSchedule)