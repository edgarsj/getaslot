# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from slots.models import Business,Appointment
from django.core import serializers

def business(request, slug):
    
    b = get_object_or_404(Business, slug=slug)
    
    return render_to_response("business/business.html", {
        "business": b,
    }, context_instance=RequestContext(request))
    
def appointment(request, format):
    if request.is_ajax():
        if format == 'xml':
            mimetype = 'application/xml'
        if format == 'json':
            mimetype = 'application/javascript'
        data = serializers.serialize(format, Appointment.objects.all())
        return HttpResponse(data,mimetype)
    else:
        return HttpResponse(status=400)
