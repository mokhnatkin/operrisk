from django.shortcuts import render
from django.http import HttpResponse
from operrisk.models import Category, Incident
from operrisk.forms import IncidentForm

# Create your views here.
def index (request):#home page
    incidents = Incident.objects.order_by('-incident_date')[:5] #5 last incidents
    categories = Category.objects.order_by('name')#list of all categories
    context_dict={'incidents':incidents,'categories':categories}
    return render(request, 'operrisk/index.html',context=context_dict)


def show_category(request,category_URL_name):#shows the category w/ list of incidents
    context_dict = {}
    try:
        category = Category.objects.get(URL_name=category_URL_name)
        incidents = Incident.objects.filter(category_id=category)
        context_dict['incidents'] = incidents
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['incidents'] = None
        context_dict['category'] = None
    return render(request,'operrisk/category.html',context_dict)


def show_incident(request,incident_id):#shows the incident
    context_dict = {}
    try:
        incident = Incident.objects.get(id=incident_id)
        category = Category.objects.get(id=incident.category_id.id)
        context_dict['incident'] = incident
        context_dict['category'] = category
    except Incident.DoesNotExist:
        context_dict['incident'] = None
        context_dict['category'] = None
    return render(request,'operrisk/incident.html',context_dict)


def show_all_incidents(request):#shows the list of all incidents
    incidents = Incident.objects.order_by('-incident_date')
    context_dict = {'incidents':incidents}
    return render(request, 'operrisk/all_incidents.html',context=context_dict)


def add_incident(request):
    form = IncidentForm
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request,'operrisk/add_incident.html',{'form':form})