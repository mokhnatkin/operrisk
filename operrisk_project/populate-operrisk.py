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
                {"name":"Внутреннее мошенничество","URL_name":"internal-fraud"},
                {"name":"Внешнее мошенничество","URL_name":"external-fraud"},
                {"name":"Клиенты, продукты и деловая практика","URL_name":"clients-products-practice"},
                {"name":"Сбой ведения бизнеса и работы систем","URL_name":"system-failure"},
                {"name":"Исполнение, доставка и управление процессом","URL_name":"process-management"},
                {"name":"Производственные отношения и безопасность труда","URL_name":"labor-safety"},
                {"name":"Стихийные бедствия и безопасность","URL_name":"natural-disasters"}
            ]
    for cat in cats:
        c = add_cat(cat["name"],cat["URL_name"])

def add_cat(name, URL_name):
    c = Category.objects.get_or_create(name=name,URL_name=URL_name)[0]
    c.save()
    return c


if __name__ == '__main__':
    print("Starting Operrisk population script...")
    populate()