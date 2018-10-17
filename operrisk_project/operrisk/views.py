from django.shortcuts import render
from django.http import HttpResponse
from operrisk.models import Category, Incident

# Create your views here.
def index (request):
    incidents = Incident.objects.order_by('-incident_date')[:5] #5 last incidents
    context_dict={'incidents':incidents}
    return render(request, 'operrisk/index.html',context=context_dict)