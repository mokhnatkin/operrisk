from django.db import models
from django.template.defaultfilters import slugify
import unidecode
from unidecode import unidecode
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
import datetime

##################################################################################################

class Category(models.Model):#class for category of incident
    name = models.CharField(max_length=128,unique=True)
    URL_name = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.URL_name = slugify(unidecode(self.name)) #slugify URL address (converts to eng letters, removes spaces)
        super(Category,self).save(*args, **kwargs)

    class Meta:#plural form for admin interface
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

##################################################################################################

class Subcategory(models.Model):#class for subcategory of incident
    name = models.CharField(max_length=128,null=False)
    URL_name = models.SlugField()
    category = models.ForeignKey(Category,on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        self.URL_name = slugify(unidecode(self.name)) #slugify URL address (converts to eng letters, removes spaces)
        super(Subcategory,self).save(*args, **kwargs)

    class Meta:#plural form for admin interface
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return self.name        

##################################################################################################

class Incident(models.Model):#incident class    
    DRAFT_STATUS = '1'
    CREATED_STATUS = '2'
    APPROVED_STATUS = '3'
    CANCELED_STATUS = '4'

    INCIDENT_STATUSES = (
                (DRAFT_STATUS, 'Черновик'),
                (CREATED_STATUS, 'Создан'),
                (APPROVED_STATUS, 'Утвержден'),
                (CANCELED_STATUS, 'Помечен как ошибка'),
            )

    name = models.CharField(max_length=256,null=False)
    status = models.CharField(max_length=1,choices=INCIDENT_STATUSES,blank=False,null=False,default=DRAFT_STATUS)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.PROTECT)
    incident_date = models.DateField(null=False,default=datetime.date.today())
    incident_end_date = models.DateField(null=False,default=datetime.date.today())
    incident_balance_date = models.DateField(null=True,blank=True,default=None)
    description = models.CharField(max_length=4096,null=False)
    loss_amount = models.FloatField(default=0,blank=True,null=True)
    measures_taken = models.CharField(max_length=2048,null=False)
    att = models.FileField(null=True,blank=True,upload_to='files_att/')
    created_by = models.ForeignKey(User,on_delete=models.PROTECT,null=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    comment = models.CharField(max_length=2048,null=True,blank=True,default='')

    def save(self, *args, **kwargs):        
        if self.loss_amount < 0:#loss_amount should not be less than 0
            self.loss_amount = 0            
        cur_date = datetime.date.today()
        if self.incident_date > cur_date:#incident_date should not be in a future
            self.incident_date = cur_date
        if self.incident_end_date < self.incident_date:#incident_end_date should be more or equal to incident_date
            self.incident_end_date = self.incident_date
        if (self.incident_balance_date is not None) and (self.incident_balance_date > cur_date):#incident_balance_date should not be in a future
            self.incident_balance_date = cur_date            
        super(Incident,self).save(*args, **kwargs)

    def __str__(self):
        return self.name

##################################################################################################

@receiver(models.signals.post_save, sender=User)#adds each new user to "employees" group automatically
def post_save_user_signal_handler(sender, instance, created, **kwargs):
    if created:
        try:
            group = Group.objects.get(name='employees')
            instance.groups.add(group)
            instance.save()
        except:
            quit()
