from operrisk.models import Incident, Category, Subcategory
import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter, ModelChoiceFilter, ChoiceFilter


class IncidentFilter(django_filters.FilterSet):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    statuses = Incident.INCIDENT_STATUSES

    name = CharFilter(lookup_expr='icontains',label='Название')
    status = ChoiceFilter(choices=statuses, label='Статус')    
    category = ModelChoiceFilter(queryset=categories, label='Категория')
    subcategory = ModelChoiceFilter(queryset=subcategories, label='Причина')
    loss_amount__gt = NumberFilter(field_name='loss_amount',lookup_expr='gt',label='Убыток больше чем...')
    loss_amount__lt = NumberFilter(field_name='loss_amount',lookup_expr='lt',label='Убыток меньше чем...')    
    incident_year = NumberFilter(field_name='incident_date',lookup_expr='year',label='Год инцидента')
    
    class Meta:
        model = Incident
        fields = ['id','status','name','category','subcategory']
      
        