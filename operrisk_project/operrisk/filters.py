from operrisk.models import Incident, Category
import django_filters
from django_filters import DateFromToRangeFilter, DateFilter, CharFilter, NumberFilter, ModelChoiceFilter, ChoiceFilter


class IncidentFilter(django_filters.FilterSet):    
    name = CharFilter(lookup_expr='icontains',label='Название')
    category_id = ModelChoiceFilter(queryset=Category.objects.all(), label='Категория')
    loss_amount__gt = NumberFilter(field_name='loss_amount',lookup_expr='gt',label='Убыток больше чем...')
    loss_amount__lt = NumberFilter(field_name='loss_amount',lookup_expr='lt',label='Убыток меньше чем...')    
    incident_year = NumberFilter(field_name='incident_date',lookup_expr='year',label='Год инцидента')
    
    class Meta:
        model = Incident
        fields = ['id','status','name','category_id']