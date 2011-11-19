from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
#from django.conf import settings
def index(request):
#	print settings.STATIC_ROOT
	return render_to_response("index.html", {}, context_instance=RequestContext(request))