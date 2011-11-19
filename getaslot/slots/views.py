# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers
from django.template import RequestContext
from django.http import HttpResponse
from slots.models import Business,Appointment

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
    if request.is_ajax() or True:        
        mimetype = 'application/javascript'
        data = serializers.serialize('json', Appointment.objects.all())
        return HttpResponse(data,mimetype)
    else:
        return HttpResponse(status=400)
