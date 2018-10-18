from django import forms
from operrisk.models import Incident, Category

class IncidentForm(forms.ModelForm):#the form to create an incident
    name = forms.CharField(max_length=256,help_text="Укажите название инцидента")
    #category_id = forms.ChoiceField(help_text="Категория опер. риска")
    incident_date = forms.DateTimeField(help_text="Дата-время инцидента")
    description = forms.CharField(max_length=4096,help_text="Описание инцидента")
    loss_amount = forms.FloatField(initial=0.0,help_text="Сумма ущерба")
    measures_taken = forms.CharField(max_length=2048,help_text="Предпринятые меры")
    class Meta:
        model = Incident
        fields = ('name','category_id','incident_date','description','loss_amount','measures_taken')