# a script to populate Operrisk APP
# the script creates categories in DB
# it also create groups and permissions

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','operrisk_project.settings')
import django

django.setup()
from operrisk.models import Category

def populate():
    #list of categories
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

#def add_group(name):


if __name__ == '__main__':
    print("Starting Operrisk population script...")
    populate()