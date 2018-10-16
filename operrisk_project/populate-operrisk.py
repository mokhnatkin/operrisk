# a script to populate Operrisk APP
# the script reads a list of caterogies of incidents from xls file
# and puts the list into DB

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','operrisk_project.settings')
import django

django.setup()
from operrisk.models import Category, Incident

def populate():
    #create list of categories
    cats = [{"name":"категория 1","URL_name":"cat-1"},{"name":"категория 2","URL_name":"cat-2"}]
    for cat in cats:
        c = add_cat(cat["name"],cat["URL_name"])

def add_cat(name, URL_name):
    c = Category.objects.get_or_create(name=name,URL_name=URL_name)[0]
    #c.name = name
    #c.URL_name = URL_name
    c.save()
    return c


if __name__ == '__main__':
    print("Starting Operrisk population script...")
    populate()