from operrisk.models import Incident
import django_filters

class IncidentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')    
    loss_amount__gt = django_filters.NumberFilter(field_name='loss_amount',lookup_expr='gt')
    loss_amount__lt = django_filters.NumberFilter(field_name='loss_amount',lookup_expr='lt')    
    incident_year = django_filters.NumberFilter(field_name='incident_date',lookup_expr='year')
    incident_year__gt = django_filters.NumberFilter(field_name='incident_date',lookup_expr='year__gt')
    incident_year__lt = django_filters.NumberFilter(field_name='incident_date',lookup_expr='year__lt')
    
    class Meta:
        model = Incident
        fields = ['name','loss_amount','category_id','incident_date']