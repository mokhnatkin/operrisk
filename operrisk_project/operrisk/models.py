from django.db import models
from django.template.defaultfilters import slugify
import unidecode
from unidecode import unidecode

# Create your models here.
class Category(models.Model):#class for category of incident
    name = models.CharField(max_length=256,unique=True)
    URL_name = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.URL_name = slugify(unidecode(self.name))
        super(Category,self).save(*args, **kwargs)

    class Meta:#plural form for admin interface
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Incident(models.Model):#incident class
    name = models.CharField(max_length=256,null=False)
    category_id = models.ForeignKey(Category,on_delete=models.PROTECT)
    incident_date = models.DateTimeField(null=False)
    description = models.CharField(max_length=4096,null=False)
    loss_amount = models.FloatField(default=0,blank=True,null=True)
    measures_taken = models.CharField(default="",max_length=2048,null=False)

    def __str__(self):
        return self.name    
