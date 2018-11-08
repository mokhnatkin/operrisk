from django import forms
from operrisk.models import Incident, Category, Subcategory
import datetime



class IncidentForm(forms.ModelForm):#the form to create an incident    
    cur_year = datetime.datetime.today().year
    year_range = tuple([i for i in range(cur_year, cur_year+1)])#year_range - what years can be selected in incident_date field
    MONTHS = {
        1: ('января'), 2: ('февраля'), 3: ('марта'), 4:('апреля'),
        5: ('мая'), 6:('июня'), 7: ('июля'), 8: ('августа'),
        9: ('сентября'), 10: ('октября'), 11: ('ноября'), 12: ('декабря')
    }
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    empty_subcategories = Subcategory.objects.none()
    
    name = forms.CharField(max_length=256,help_text="Укажите название инцидента",label="Название")
    category = forms.ModelChoiceField(queryset=categories,help_text="Выберите категорию, к которой относится инцидент",label="Категория")
    subcategory = forms.ModelChoiceField(queryset=subcategories,help_text="Выберите подкатегорию, к которой относится инцидент",label="Подкатегория")
    incident_date = forms.DateField(initial=datetime.date.today(),widget=forms.SelectDateWidget(years=year_range, months=MONTHS),help_text="Укажите, когда произошел инцидент",label="Дата инцидента")         
    description = forms.CharField(max_length=4096,help_text="Подробно опишите инцидент",widget=forms.Textarea,label="Описание инцидента")
    loss_amount = forms.FloatField(initial=0.0,help_text="Укажите сумму ущерба в тенге (если применимо)",label="Сумма ущерба")
    measures_taken = forms.CharField(max_length=2048,help_text="Опишите, какие меры были предприняты для того, чтобы избежать подобных инцидентов в будущем, или минимизировать ущерб",widget=forms.Textarea,label="Предпринятые меры")
    att = forms.FileField(help_text="Прикрепите относящиеся к инциденту файлы (если применимо). Если хотите прикрепить несколько файлов, добавьте их в один архив.",widget=forms.FileInput,label="Файл")

    class Meta:
        model = Incident
        fields = ('name','category','subcategory','incident_date','description','loss_amount','measures_taken','att')
    
    def __init__(self, *args, **kwargs):
        super(IncidentForm, self).__init__(*args, **kwargs)
        self.fields['att'].required = False
        self.fields['loss_amount'].required = False

    def clean_loss_amount(self):
        data = self.cleaned_data['loss_amount']
        if data<0:
            raise forms.ValidationError("Сумма ущерба не может быть отрицательной!")
        return data

    def clean_incident_date(self):
        data = self.cleaned_data['incident_date']
        cur_date = datetime.date.today()
        if data > cur_date:#incident_date should not be in a future
            raise forms.ValidationError("Дата инцидента не может быть больше текущей!")
        return data

    def clean_subcategory(self):
        data = self.cleaned_data['subcategory']
        cat = self.cleaned_data['category']
        if data.category.id != cat.id:#subcategory should belong to the category selected
            raise forms.ValidationError("Выберите подкатегорию корректно. Подкатегория должна относиться к выбранной категории!")
        return data        
