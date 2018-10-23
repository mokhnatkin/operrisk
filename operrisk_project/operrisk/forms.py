from django import forms
from operrisk.models import Incident, Category
import datetime



class IncidentForm(forms.ModelForm):#the form to create an incident
    #year_range - what years can be selected in incident_date field
    cur_year = datetime.datetime.today().year
    year_range = tuple([i for i in range(cur_year - 3, cur_year+1)])

    name = forms.CharField(max_length=256,help_text="Укажите название инцидента")
    incident_date = forms.DateField(initial=datetime.date.today(),widget=forms.SelectDateWidget(years=year_range))    
    description = forms.CharField(max_length=4096,help_text="Описание инцидента")
    loss_amount = forms.FloatField(initial=0.0,help_text="Сумма ущерба")
    measures_taken = forms.CharField(max_length=2048,help_text="Предпринятые меры")
    att = forms.FileField(help_text="Относящиеся к инциденту файлы (в архиве)")

    class Meta:
        model = Incident
        fields = ('name','category_id','incident_date','description','loss_amount','measures_taken','att')
    
    def __init__(self, *args, **kwargs):
        super(IncidentForm, self).__init__(*args, **kwargs)
        self.fields['att'].required = False
        self.fields['loss_amount'].required = False
        

