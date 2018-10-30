from django.db import models
from django.template.defaultfilters import slugify
import unidecode
from unidecode import unidecode
from django.contrib.auth.models import User, Group


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
    name = models.CharField(max_length=256,null=False)
    category_id = models.ForeignKey(Category,on_delete=models.PROTECT)
    incident_date = models.DateField(null=False)
    description = models.CharField(max_length=4096,null=False)
    loss_amount = models.FloatField(default=0,blank=True,null=True)
    measures_taken = models.CharField(max_length=2048,null=False)
    att = models.FileField(null=True,blank=True,upload_to='files_att/')
    created_by = models.ForeignKey(User,on_delete=models.PROTECT,null=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name



    #g_empl = Group.objects.get(name="employees")
    #g_empl.user_set.add(user)