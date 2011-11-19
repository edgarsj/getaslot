# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from slots.models import Business

def business(request, slug):
    
    b = get_object_or_404(Business, slug=slug)
    
    return render_to_response("business/business.html", {
        "business": b,
    }, context_instance=RequestContext(request))
    
