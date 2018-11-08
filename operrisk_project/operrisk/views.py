from django.shortcuts import render, redirect, reverse, get_object_or_404
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
from operrisk.emailing import send_email


# Create your views here.
@login_required
def index (request):#home page
    incidents = Incident.objects.order_by('-created_date')[:5] #5 last incidents
    categories = Category.objects.order_by('name')#list of all categories
    context_dict={'incidents':incidents,'categories':categories}
    return render(request, 'operrisk/index.html',context=context_dict)


@login_required
@permission_required('operrisk.view_category',raise_exception=True)
def show_category(request,category_URL_name):#shows the category w/ list of incidents
    context_dict = {}
    try:
        category = Category.objects.get(URL_name=category_URL_name)
        incidents = Incident.objects.filter(category=category)
        context_dict['incidents'] = incidents
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['incidents'] = None
        context_dict['category'] = None
    return render(request,'operrisk/category.html',context_dict)


@login_required
@permission_required('operrisk.view_incident',raise_exception=True)
def show_incident(request,id):#shows the incident
    context_dict = {}
    try:
        incident = Incident.objects.get(id=id)
        category = Category.objects.get(id=incident.category.id)
        context_dict['incident'] = incident
        context_dict['category'] = category
    except Incident.DoesNotExist:
        context_dict['incident'] = None
        context_dict['category'] = None
    return render(request,'operrisk/incident.html',context_dict)


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
    header_style = xlwt.XFStyle()
    header_style.font.bold = True
    date_style = xlwt.XFStyle()
    date_style.num_format_str='DD.MM.YYYY'#set format for incident_date
    float_style = xlwt.XFStyle()
    float_style.num_format_str='#,##0'#set format for loss_amount
    columns = ['дата инцидента', 'название', 'статус', 'категория', 'ущерб', 'кем создан', ]      
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], header_style)
    incidents = Incident.objects.all()
    for incident in incidents:
        row_num += 1
        ws.write(row_num,0,incident.incident_date,date_style)
        ws.write(row_num,1,incident.name)
        ws.write(row_num,2,incident.status)
        ws.write(row_num,3,incident.category.name)
        ws.write(row_num,4,incident.loss_amount,float_style)
        ws.write(row_num,5,incident.created_by.username)
    wb.save(response)
    return response


def send_email_incident_added(inc_id,inc_name,inc_created_by,inc_url):#function sends email to all RMs when icident with given id is created      
    msg_subject = 'База опер.рисков - создан новый инцидент, ID ' + inc_id    
    msg_body = 'В базе опер.рисков пользователем ' + inc_created_by + ' был создан новый инцидент: ' + inc_name + '. ID инцидента: ' + inc_id + '. Детали: ' + inc_url
    RMS = User.objects.filter(groups__name='risk-managers')
    for RM in RMS:#send email to each user in 'risk-managers' group
        send_email(msg_subject,msg_body,RM.username)


@login_required
@permission_required('operrisk.add_incident',raise_exception=True)
def edit_incident(request, id=None,template_name = ''):#view is used to add or edit incident
    if id:#incident already existing
        incident = get_object_or_404(Incident, pk=id)
        if incident.status not in ('1',):#one can edit only incidents with status=Черновик
            return redirect('show_incident',id=incident.id)
        template_name='operrisk/edit_incident.html'
    else:#new incident
        incident = Incident(created_by=request.user) 
        template_name='operrisk/add_incident.html'
        
    form = IncidentForm(request.POST or request.FILES or None, instance=incident)

    if request.POST and form.is_valid():        
        instance = form.save(commit=False)        
        if id:#editing existing incident
            instance.status = '2'#status=создан
            redirected_url='show_incident'
            inc_id = str(instance.id)
            inc_name = str(instance.name)
            inc_created_by = str(instance.created_by.username)
            inc_url = request.build_absolute_uri(reverse('show_incident', args=(instance.id, )))
            try:
                send_email_incident_added(inc_id,inc_name,inc_created_by,inc_url)#send email to all RMs
            except:
                pass
        else:#adding new incident
            instance.status = '1'#status=черновик
            redirected_url = 'edit_incident'            
        form.save()
        return redirect(redirected_url,id=instance.id)

    return render(request, template_name, {'form': form})

@login_required
@permission_required('operrisk.add_incident',raise_exception=True)
def show_my_incidents(request):#shows the list of all incidents added by current user
    current_user = request.user
    incidents = Incident.objects.all().filter(created_by=current_user)
    context_dict = {'current_user':current_user,'incidents':incidents}
    return render(request, 'operrisk/my_incidents.html',context=context_dict)


@login_required
@permission_required('auth.view_user',raise_exception=True)
def list_users(request):#list of users
    users = User.objects.all()
    context_dict = {'users':users}
    return render(request, 'operrisk/list_users.html',context=context_dict)


@login_required
@permission_required('operrisk.approve_incident',raise_exception=True)
def approve_incident(request,id=None):#approve incident
    if id:
        incident = get_object_or_404(Incident, pk=id)
        if incident.status == '2':
            incident.status = '3'#status=Утвержден
            incident.save()
            response = HttpResponse()#redirect to show_incident
        else:
            return redirect('show_incident',id=id)
    else:
        return redirect('show_incident',id=id)
    return redirect('show_incident',id=id)


@login_required
@permission_required('operrisk.approve_incident',raise_exception=True)
def cancel_incident(request,id=None):#cancel incident
    if id:
        incident = get_object_or_404(Incident, pk=id)
        if incident.status == '2':
            incident.status = '4'#status=Ошибка
            incident.save()
            response = HttpResponse()#redirect to show_incident
        else:
            return redirect('show_incident',id=id)
    else:
        return redirect('show_incident',id=id)
    return redirect('show_incident',id=id)