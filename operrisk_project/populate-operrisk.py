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
    cats = [
                {"name":"Внутреннее мошенничество"},
                {"name":"Внешнее мошенничество"},
                {"name":"Клиенты, продукты и деловая практика"},
                {"name":"Сбой ведения бизнеса и работы систем"},
                {"name":"Исполнение, доставка и управление процессом"},
                {"name":"Производственные отношения и безопасность труда"},
                {"name":"Стихийные бедствия и безопасность"}
            ]
    for cat in cats:
        c = add_cat(cat["name"])

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c


if __name__ == '__main__':
    print("Starting Operrisk population script...")
    populate()