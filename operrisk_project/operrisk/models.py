from django.db import models
from django.template.defaultfilters import slugify
import unidecode
from unidecode import unidecode
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
import datetime
#from operrisk.emailing import send_email



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


class Incident(models.Model):#incident class
    STATUSES = (
        ('1', 'Черновик'),#incident.status for '1' #incident.get_status_display() for 'Черновик'
        ('2', 'Создан'),
        ('3', 'Утвержден'),
        ('4', 'Помечен как ошибка'),
    )
    name = models.CharField(max_length=256,null=False)
    status = models.CharField(max_length=1,choices=STATUSES,blank=False,null=False,default='1')
    category_id = models.ForeignKey(Category,on_delete=models.PROTECT)
    incident_date = models.DateField(null=False)
    description = models.CharField(max_length=4096,null=False)
    loss_amount = models.FloatField(default=0,blank=True,null=True)
    measures_taken = models.CharField(max_length=2048,null=False)
    att = models.FileField(null=True,blank=True,upload_to='files_att/')
    created_by = models.ForeignKey(User,on_delete=models.PROTECT,null=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True)


    def save(self, *args, **kwargs):        
        if self.loss_amount < 0:#loss_amount should not be less than 0
            self.loss_amount = 0            
        cur_date = datetime.date.today()
        if self.incident_date > cur_date:#incident_date should not be in a future
            self.incident_date = cur_date            
        super(Incident,self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(models.signals.post_save, sender=User)#adds each new user to "employees" group automatically
def post_save_user_signal_handler(sender, instance, created, **kwargs):
    if created:
        try:
            group = Group.objects.get(name='employees')
            instance.groups.add(group)
            instance.save()
        except:
            quit()


"""
@receiver(models.signals.post_save, sender=Incident)#sends email to all risk-managers when incident is added
def post_save_incident_signal_handler(sender, instance, created, **kwargs):
    if created:
        try:
            inc_name = instance.name
            inc_created_by = instance.created_by.username
            inc_id = instance.id            
            msg_subject = 'База опер.рисков - создан новый инцидент'            
            msg_body = 'В базе опер.рисков пользователем ' + inc_created_by + ' был создан новый инцидент: ' + inc_name + '. ID инцидента: ' + inc_id
            msg_recipient_email = 'a.mokhnatkin@a-i.kz'
            send_email(msg_subject,msg_body,msg_recipient_email)
        except:
            quit()

"""