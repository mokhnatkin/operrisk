from django import forms
from operrisk.models import Incident, Category, Subcategory
import datetime

"""
class CategorySelectForm(forms.ModelForm):#the form to select category in order to display proper list of subcategories when creating incident
    categories = Category.objects.all()

    class Meta:
        model = Category
        fields = ('name',)
"""

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
    subcategory = forms.ModelChoiceField(queryset=subcategories,help_text="Выберите причину",label="Причина")
    incident_date = forms.DateField(initial=datetime.date.today(),widget=forms.SelectDateWidget(years=year_range, months=MONTHS),help_text="Укажите дату начала инцидента",label="Дата начала инцидента")
    incident_end_date = forms.DateField(initial=datetime.date.today(),widget=forms.SelectDateWidget(years=year_range, months=MONTHS),help_text="Укажите дату окончания инцидента",label="Дата окончания инцидента")
    incident_balance_date = forms.DateField(required=False,widget=forms.SelectDateWidget(years=year_range, months=MONTHS),help_text="Укажите дату отражения инцидента на балансе (если был ущерб)",label="Дата отражения на балансе")    
    description = forms.CharField(max_length=4096,help_text="Подробно опишите инцидент",widget=forms.Textarea,label="Описание инцидента")
    loss_amount = forms.FloatField(initial=0.0,help_text="Укажите сумму ущерба в тенге (если применимо)",label="Сумма ущерба")
    measures_taken = forms.CharField(max_length=2048,help_text="Опишите, какие меры были предприняты для того, чтобы избежать подобных инцидентов в будущем, или минимизировать ущерб",widget=forms.Textarea,label="Предпринятые меры")
    att = forms.FileField(help_text="Прикрепите относящийся к инциденту файл (если применимо). Если хотите прикрепить несколько файлов, предварительно добавьте их в один архив.",widget=forms.FileInput,label="Файл")
    comment = forms.CharField(max_length=2048,help_text="Любая дополнительная информация",widget=forms.Textarea,label="Комментарий")

    class Meta:
        model = Incident
        fields = ('name','category','subcategory','incident_date', 'incident_end_date', 'incident_balance_date', 'description','loss_amount','measures_taken','att', 'comment')
    
    def __init__(self, *args, **kwargs):
        super(IncidentForm, self).__init__(*args, **kwargs)
        self.fields['att'].required = False
        self.fields['loss_amount'].required = False
        self.fields['comment'].required = False

    
    def clean_loss_amount(self):
        data = self.cleaned_data['loss_amount']
        if data<0:
            raise forms.ValidationError("Сумма ущерба не может быть отрицательной!")
        return data

    def clean_incident_date(self):
        data = self.cleaned_data['incident_date']
        cur_date = datetime.date.today()
        if data > cur_date:#incident_date should not be in a future
            raise forms.ValidationError("Дата начала инцидента не может быть больше текущей!")
        return data

    def clean(self):
        cleaned_data = super().clean()
        cur_date = datetime.date.today()
        incident_end_date = cleaned_data.get("incident_end_date")
        incident_date = cleaned_data.get("incident_date")
        incident_balance_date = cleaned_data.get("incident_balance_date")
        loss_amount = cleaned_data.get("loss_amount")
        subcategory = cleaned_data.get("subcategory")
        category = cleaned_data.get("category")
        if incident_end_date < incident_date:#incident_end_date should be more or equal to incident_date            
            self.add_error('incident_end_date', "Дата окончания инцидента не может быть меньше даты начала!")
        if loss_amount > 0 and incident_balance_date is None:
            self.add_error('incident_balance_date', "Необходимо указать дату отражения на балансе")
        if incident_balance_date is not None:
            if loss_amount == 0:
                self.add_error('incident_balance_date', "Дата отражения на балансе не должна быть заполнена, т.к. сумма ущерба = 0")
            if incident_balance_date > cur_date:#balance_date should not be in a future
                self.add_error('incident_balance_date', "Дата отражения на балансе не может быть больше текущей!")
            if incident_balance_date < incident_date:#balance_date should not be less than incident date
                self.add_error('incident_balance_date', "Дата отражения на балансе не может быть меньше даты начала инцидента!")
        if subcategory.category.id != category.id:#subcategory should belong to the category selected            
            self.add_error('subcategory', "Выберите подкатегорию корректно. Подкатегория должна относиться к выбранной категории!")

