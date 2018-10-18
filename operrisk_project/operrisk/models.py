from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Category(models.Model):#class for category of incident
    name = models.CharField(max_length=256,unique=True,null=False)
    URL_name = models.SlugField(unique=True,null=False)
    #URL_name = models.CharField(max_length=256,unique=True,null=False,default=name)

    def save(self, *args, **kwargs):
        self.URL_name = slugify(self.name)
        super(Category,self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Incident(models.Model):#incident class
    name = models.CharField(max_length=256,null=False)
    caterogy_id = models.ForeignKey(Category,on_delete=models.PROTECT)
    incident_date = models.DateTimeField(null=False)
    description = models.CharField(max_length=4096,null=False)
    loss_amount = models.FloatField(default=0,blank=True,null=True)
    measures_taken = models.CharField(default="",max_length=2048,null=False)

    def __str__(self):
        return self.name    
