import json
import datetime
# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers
from django.template import RequestContext
from django.http import HttpResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt


BUSINESS_HOURS_FROM = 8
BUSINESS_HOURS_TO = 20

from slots.models import Business, Appointment, WorkSchedule, BusinessEmployee

def business(request, slug):    
    b = get_object_or_404(Business, slug=slug)    
    return render_to_response("business/business.html", {
        "business": b,
    }, context_instance=RequestContext(request))
    
def appointments(request, business):
    b = get_object_or_404(Business, slug=business)
    l = []
    if request.user.is_authenticated():
        
        appointments = Appointment.objects.filter(customer__id = request.user.id).filter(
                                work_schedule__employee__id__in=b.employees.values_list('pk', flat=True)                                
                                )            
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

def busy(request, business, employee_id):

    schedules = WorkSchedule.objects.filter(
                            employee__id=employee_id
                            )
    l = []
    for a in schedules:
        start = datetime.datetime.combine(a.day,datetime.time(BUSINESS_HOURS_FROM))
        end = datetime.datetime.combine(a.day,datetime.time(BUSINESS_HOURS_TO))
        if start <= a.starttime:
            o = {}
            o['id'] = a.id
            o['title'] = ''
            o['start'] = start.isoformat()
            o['end'] = a.starttime.isoformat()
            o['readOnly'] = True
            l.append(o)
        
        for ap in a.appointments.all():
            o = {}
            o['id'] = a.id
            o['title'] = ''
            o['start'] = ap.starttime.isoformat()
            o['end'] = ap.endtime.isoformat()
            o['readOnly'] = True
            l.append(o)

        if end >= a.endtime:
            o = {}
            o['id'] = a.id
            o['title'] = ''
            o['start'] = a.endtime.isoformat()
            o['end'] = datetime.datetime.combine(a.day,datetime.time(BUSINESS_HOURS_TO)).isoformat()
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

@csrf_exempt
def add_appointment(request, work_schedule_id):
    if (request.is_ajax() or True) and request.method == 'POST':
        ws = get_object_or_404(WorkSchedule, id=work_schedule_id)
        form = SimpleAppointmentForm(request.POST)
        if form.is_valid():
            ap = Appointment()
            ap.work_schedule = ws
            ap.name = form.cleaned_data['name']
            ap.phone = form.cleaned_data['phone']
            ap.starttime = form.cleaned_data['start']
            ap.endtime = form.cleaned_data['end']
            ap.save()
        mimetype = 'application/javascript'        
        return HttpResponse('OK',mimetype)
    return HttpResponse(status=400)

@csrf_exempt
def add_appointment_noschedule(request, business, employee_id):
    if (request.is_ajax() or True) and request.method == 'POST':
        
        emp = get_object_or_404(BusinessEmployee, id=int(employee_id))
        form = SimpleAppointmentForm(request.POST)
        #print form.cleaned_data
        if form.is_valid():
            start = (datetime.datetime.fromtimestamp(int(form.cleaned_data['start'])).strftime('%Y-%m-%d %H:%M:%S'))
            end = (datetime.datetime.fromtimestamp(int(form.cleaned_data['end'])).strftime('%Y-%m-%d %H:%M:%S'))
            ws = get_object_or_404(WorkSchedule, employee__id=employee_id,
                                   starttime__lte=start,
                                   endtime__gte=end)
            #ap = Appointment(work_schedule)
            ap = Appointment()
            ap.work_schedule = ws
            ap.name = form.cleaned_data['name']
            ap.phone = form.cleaned_data['phone']
            ap.starttime = form.cleaned_data['start']
            ap.endtime = form.cleaned_data['end']
            ap.save()
        mimetype = 'application/javascript'        
        return HttpResponse('OK',mimetype)
    return HttpResponse(status=400)
