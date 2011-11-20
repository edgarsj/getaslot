import json
import datetime
# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django import forms
from django.views.decorators.csrf import csrf_exempt


BUSINESS_HOURS_FROM = 8
BUSINESS_HOURS_TO = 20

from slots.models import Business, Appointment, WorkSchedule, BusinessEmployee, Subscriber

def business(request, slug):    
    b = get_object_or_404(Business, slug=slug)    
    return render_to_response("business/business.html", {
        "business": b,
    }, context_instance=RequestContext(request))

def businessAdmin(request, slug):
    b = get_object_or_404(Business, slug=slug)    
    return render_to_response("business/businessAdmin.html", {
        "business": b,
    }, context_instance=RequestContext(request))



def appointments(request, business):
    b = get_object_or_404(Business, slug=business)
    l = []
    admin = request.GET.get('admin')

    if request.user.is_authenticated():
        if admin == "1":
            appointments = Appointment.objects.filter(
                                work_schedule__employee__id__in=b.employees.values_list('pk', flat=True)                                
                                )
        else:
            appointments = Appointment.objects.filter(customer__id = request.user.id).filter(
                                work_schedule__employee__id__in=b.employees.values_list('pk', flat=True)                                
                                )
        for a in appointments:
            o = {}
            o['id'] = a.id
            #o['title'] = a.name
            o['name'] = a.name
            #o['body'] = a.phone
            o['phone'] = a.phone
                    
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


def busy_date(date):
    start = datetime.datetime.combine(date,datetime.time(BUSINESS_HOURS_FROM))
    end = datetime.datetime.combine(date,datetime.time(BUSINESS_HOURS_TO))
    o = {}
    o['id'] = 'null'
    o['title'] = ''
    o['start'] = start.isoformat()
    o['end'] = end.isoformat()
    o['readOnly'] = True
    return o

def daterange(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield start_date + datetime.timedelta(n)
        
def busy(request, business, employee_id):

    from_date = datetime.datetime.fromtimestamp(int(request.GET.get('start'))).date()
    to_date = datetime.datetime.fromtimestamp(int(request.GET.get('end'))).date()
    schedules = WorkSchedule.objects.filter(
                            employee__id=employee_id
                            ).order_by('day')
    l = []
    last_date = None
    for a in schedules:
        if not last_date and a.day:
            for single_date in daterange(from_date, a.day):
                l.append(busy_date(single_date))
        elif a.day-last_date > datetime.timedelta(1):
            for single_date in daterange(last_date+datetime.timedelta(1), a.day):
                l.append(busy_date(single_date))
        last_date = a.day
        day_start_time = datetime.datetime.combine(a.day,datetime.time(BUSINESS_HOURS_FROM))
        day_end_time = datetime.datetime.combine(a.day,datetime.time(BUSINESS_HOURS_TO))
        if day_start_time <= a.starttime:
            o = {}
            o['id'] = a.id
            o['title'] = ''
            o['start'] = day_start_time.isoformat()
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

        if day_end_time >= a.endtime:
            o = {}
            o['id'] = a.id
            o['title'] = ''
            o['start'] = a.endtime.isoformat()
            o['end'] = day_end_time.isoformat()
            o['readOnly'] = True
            l.append(o)
    if to_date > last_date:
        for single_date in daterange(a.day+datetime.timedelta(1), to_date):
            l.append(busy_date(single_date))            
        
        
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
        if form.is_valid():
            start = datetime.datetime.fromtimestamp(int(form.cleaned_data['start']))
            end = datetime.datetime.fromtimestamp(int(form.cleaned_data['end']))
            ws = get_object_or_404(WorkSchedule, employee__id=employee_id,
                                   starttime__lte=start,
                                   endtime__gte=end)
            #ap = Appointment(work_schedule)
            ap = Appointment()
            ap.work_schedule = ws
            ap.name = form.cleaned_data['name']
            ap.phone = form.cleaned_data['phone']
            ap.starttime = start
            ap.endtime = end
            ap.save()
            mimetype = 'application/javascript'
            return HttpResponse('OK',mimetype)
        mimetype = 'application/javascript'        
        return HttpResponse('ERROR',mimetype)
    return HttpResponse(status=400)

class SubscriberForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (SubscriberForm,self ).__init__(*args,**kwargs) # populates the post
    class Meta:
        model = Subscriber
        #exclude = ('creator, created_on',)
        fields = ('email')
        
@csrf_exempt        
def save_subscriber(request):
    form = SubscriberForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            subscriber = form.save(commit=False)
            subscriber.ip_address = request.META['REMOTE_ADDR']
            subscriber.save()                        
            return HttpResponse("{'result':'ok'}",mimetype = 'application/json')
        else:
            return HttpResponse(form.errors,mimetype = 'application/json')
    else: 
        raise Http404("")
