from django.shortcuts import render
from django.http import HttpResponse
from operrisk.models import Category, Incident
from operrisk.forms import IncidentForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required, permission_required
from operrisk.filters import IncidentFilter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import xlwt#write to excel
from django.contrib.auth.models import User



# Create your views here.
@login_required
def index (request):#home page
    incidents = Incident.objects.order_by('-incident_date')[:5] #5 last incidents
    categories = Category.objects.order_by('name')#list of all categories
    context_dict={'incidents':incidents,'categories':categories}
    return render(request, 'operrisk/index.html',context=context_dict)


@login_required
@permission_required('operrisk.view_category',raise_exception=True)
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


@login_required
@permission_required('operrisk.view_incident',raise_exception=True)
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


@login_required
@permission_required('operrisk.view_incident',raise_exception=True)
def show_all_incidents(request):#shows the list of all incidents
    incidents = Incident.objects.order_by('-incident_date')
    context_dict = {'incidents':incidents}
    return render(request, 'operrisk/all_incidents.html',context=context_dict)


@login_required
@permission_required('operrisk.view_incident',raise_exception=True)
def show_all_incidents_p(request):#shows the list of all incidents (paginated)
    incident_list = Incident.objects.order_by('id')
    paginator = Paginator(incident_list, 25) # number of objects per page
    page = request.GET.get('page')
    incidents = paginator.get_page(page)
    return render(request, 'operrisk/all_incidents_p.html', {'incidents': incidents})


@login_required
@permission_required('operrisk.view_incident',raise_exception=True)
def show_all_incidents_f(request):#shows the list of all incidents and a filter to find the incident
    f = IncidentFilter(request.GET,queryset=Incident.objects.all())
    return render(request, 'operrisk/all_incidents_f.html',{'filter':f})


@login_required
@permission_required('operrisk.view_incident',raise_exception=True)
def export_incidents(request):#exports incidents to excel file    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="incidents.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('incidents')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['дата инцидента', 'название', 'категория', 'ущерб', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    incident_list = Incident.objects.all()
    rows = incident_list.values_list('incident_date', 'name', 'category_id', 'loss_amount')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


@login_required
@permission_required('operrisk.add_incident',raise_exception=True)
def add_incident(request):#add a new incident
    form = IncidentForm
    if request.method == 'POST':
        form = IncidentForm(request.POST, request.FILES, request.user)
        if form.is_valid():
            instance = form.save(commit=False)           
            instance.created_by = request.user
            instance.save()
            form.save(commit=True)
            return index(request)            
        else:
            print(form.errors)
    return render(request,'operrisk/add_incident.html',{'form':form})


@login_required
@permission_required('auth.view_user',raise_exception=True)
def list_users(request):#list of users
    users = User.objects.all()
    context_dict = {'users':users}
    return render(request, 'operrisk/list_users.html',context=context_dict)    
 