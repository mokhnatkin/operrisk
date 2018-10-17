from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=256,unique=True,null=False)
    URL_name = models.CharField(max_length=256,unique=True,null=False,default=name)

    class Meta:
        verbose_name_plural = 'Categories'    

    def __str__(self):
        return self.name


class Incident(models.Model):
    name = models.CharField(max_length=256,null=False)
    caterogy_id = models.ForeignKey(Category,on_delete=models.PROTECT)
    incident_date = models.DateTimeField(null=False)
    description = models.CharField(max_length=4096,null=False)
    loss_amount = models.FloatField()
    measures_taken = models.CharField(max_length=2048)

    def __str__(self):
        return self.name    
