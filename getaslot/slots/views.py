import json

# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers
from django.template import RequestContext
from django.http import HttpResponse
from django import forms

from slots.models import Business, Appointment, WorkSchedule, BusinessEmployee

def business(request, slug):    
    b = get_object_or_404(Business, slug=slug)    
    return render_to_response("business/business.html", {
        "business": b,
    }, context_instance=RequestContext(request))
    
def appointments(request, business):
    b = get_object_or_404(Business, slug=business)
    appointments = Appointment.objects.filter(
                            work_schedule__employee__id__in=b.employees.values_list('pk', flat=True)
                            )
    
    l = []
    for a in appointments:
        o = {}
        o['id'] = a.id
        #o['title'] = a.name
        o['name'] = a.name
        o['body'] = a.phone
        #o['phone'] = a.phone
                
        o['start'] = a.starttime.isoformat()
        o['end'] = a.endtime.isoformat()
        l.append(o)
    
    if request.is_ajax() or True:        
        mimetype = 'application/javascript'
        data = json.dumps(l)
        return HttpResponse(data,mimetype)
    else:
        return HttpResponse(status=400)

def schedule(request, business, employee_id):

    schedules = WorkSchedule.objects.filter(
                            employee__id=employee_id
                            )
    l = []
    for a in schedules:
        o = {}
        o['id'] = a.id
        o['title'] = ''
        o['start'] = a.starttime.isoformat()
        o['end'] = a.endtime.isoformat()
        o['readOnly'] = True
        l.append(o)
    if request.is_ajax() or True:        
        mimetype = 'application/javascript'
        data = json.dumps(l)
        return HttpResponse(data,mimetype)
    else:
        return HttpResponse(status=400)


class SimpleAppointmentForm(forms.Form):
    start = forms.CharField(max_length=200)
    end = forms.CharField(max_length=200)
    name = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=200)

def add_appointment(request, work_schedule_id):
    if (request.is_ajax() or True) and request.method == 'POST':
        ws = get_object_or_404(WorkSchedule, id=work_schedule_id)
        form = SimpleAppointmentForm(request.POST)
        if form.is_valid():
            ap = Appointment()
            ap.work_schedule = ws
            ap.name = form.cleaned_data['name']
            ap.phone = form.cleaned_data['phone']
            ap.save()
        mimetype = 'application/javascript'        
        return HttpResponse('OK',mimetype)
    return HttpResponse(status=400)

def add_appointment_noschedule(request, employee_id):
    if (request.is_ajax() or True) and request.method == 'POST':
        emp = get_object_or_404(BusinessEmployee, id=employee_id)        
        form = SimpleAppointmentForm(request.POST)
        if form.is_valid():
            #ws = get_object_or_404(WorkSchedule, employee__id=employee_id, starttime_)
            #ap = Appointment(work_schedule)
            ap = Appointment()
            #ap.work_schedule
        mimetype = 'application/javascript'        
        return HttpResponse('OK',mimetype)
    return HttpResponse(status=400)
