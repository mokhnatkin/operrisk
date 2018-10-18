from django.shortcuts import render
from django.http import HttpResponse
from operrisk.models import Category, Incident

# Create your views here.
def index (request):
    incidents = Incident.objects.order_by('-incident_date')[:5] #5 last incidents
    categories = Category.objects.order_by('name')#list of all categories
    context_dict={'incidents':incidents,'categories':categories}
    return render(request, 'operrisk/index.html',context=context_dict)