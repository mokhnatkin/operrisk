# a script to populate Operrisk APP
# the script creates categories in DB
# it also create groups and permissions

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','operrisk_project.settings')
import django

django.setup()
from operrisk.models import Category, Subcategory, Incident
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType



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
    print("--categories created")

    #list of subcategories
    subcats = [    
                {"name" : "Внутр. мошен. подкатегория 1",
                        "category": Category.objects.get_or_create(name="Внутреннее мошенничество")[0]
                },                
                {"name" : "Внутр. мошен. подкатегория 2",
                        "category": Category.objects.get_or_create(name="Внутреннее мошенничество")[0]
                },
                {"name" : "Внеш. мошен. подкатегория 1",
                        "category": Category.objects.get_or_create(name="Внешнее мошенничество")[0]
                },                
                {"name" : "Внеш. мошен. подкатегория 2",
                        "category": Category.objects.get_or_create(name="Внешнее мошенничество")[0]
                },
                {"name" : "Клиенты, продукты подкатегория 1",
                        "category": Category.objects.get_or_create(name="Клиенты, продукты и деловая практика")[0]
                },                
                {"name" : "Клиенты, продукты подкатегория 2",
                        "category": Category.objects.get_or_create(name="Клиенты, продукты и деловая практика")[0]
                },
                {"name" : "Сбой ведения бизнеса подкатегория 1",
                        "category": Category.objects.get_or_create(name="Сбой ведения бизнеса и работы систем")[0]
                },                
                {"name" : "Сбой ведения бизнеса подкатегория 2",
                        "category": Category.objects.get_or_create(name="Сбой ведения бизнеса и работы систем")[0]
                },
                {"name" : "Управление процессом подкатегория 1",
                        "category": Category.objects.get_or_create(name="Исполнение, доставка и управление процессом")[0]
                },                
                {"name" : "Управление процессом подкатегория 2",
                        "category": Category.objects.get_or_create(name="Исполнение, доставка и управление процессом")[0]
                },
                {"name" : "Производственные отношения подкатегория 1",
                        "category": Category.objects.get_or_create(name="Производственные отношения и безопасность труда")[0]
                },                
                {"name" : "Производственные отношения подкатегория 2",
                        "category": Category.objects.get_or_create(name="Производственные отношения и безопасность труда")[0]
                },
                {"name" : "Стихийные бедствия подкатегория 1",
                        "category": Category.objects.get_or_create(name="Стихийные бедствия и безопасность")[0]
                },                
                {"name" : "Стихийные бедствия подкатегория 2",
                        "category": Category.objects.get_or_create(name="Стихийные бедствия и безопасность")[0]
                }
            ]

    for subcat in subcats:
        sc = add_subcat(subcat["name"],subcat["category"])
    print("--subcategories created")    
    
    #below is the list of all permissions needed
    perm_view_incident = {"codename": "view_incident",
            "name" : "Can view incident",
            "content_type": ContentType.objects.get_for_model(Incident)
        }
    
    perm_view_category = {"codename": "view_category",
            "name" : "Can view category",
            "content_type": ContentType.objects.get_for_model(Category)
        }

    perm_view_user = {"codename": "view_user",
            "name" : "Can view user",
            "content_type": ContentType.objects.get_for_model(User)
        }

    perm_add_incident = {"codename": "add_incident",
            "name" : "Can add incident",
            "content_type": ContentType.objects.get_for_model(Incident)
        }

    perm_add_category = {"codename": "add_category",
            "name" : "Can add category",
            "content_type": ContentType.objects.get_for_model(Category)
        }

    perm_approve_incident = {"codename": "approve_incident",
            "name" : "Can approve incident",
            "content_type": ContentType.objects.get_for_model(Incident)
        }

    #set of permissions for each group
    auditor_perms = [ perm_view_incident, perm_view_category, perm_view_user ]
    employee_perms = [ perm_add_incident ]
    risk_manager_perms = [ perm_view_user, perm_add_category, perm_view_category, perm_add_incident, perm_view_incident, perm_approve_incident ]

    #groups and corresponding permissions 
    groups = {
        "auditors": {"perms": auditor_perms},
        "employees": {"perms": employee_perms},
        "risk-managers": {"perms": risk_manager_perms},
    }

    #add groups and permissions
    for group, group_data in groups.items():
        g = add_group(group)
        for p in group_data["perms"]:
            add_perm(group,p["codename"],p["name"],p["content_type"])
        
    print('--groups created; permissions set')

    #now assign all users to "employees" group
    g_empl = Group.objects.get(name="employees")
    users = User.objects.all()
    for user in users:
        g_empl.user_set.add(user)
    
    print('--all local users added to Employees group with minimum permissions')




    
def add_cat(name):#creates category
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

def add_subcat(name,category):#creates category
    sc = Subcategory.objects.get_or_create(name=name,category=category)[0]
    sc.save()
    return sc

def add_group(name):#creates group
    g = Group.objects.get_or_create(name=name)[0]
    g.save()
    return g    

def add_perm(group_name,perm_codename,perm_name,perm_ct):#adds permissions to a group
    new_group = Group.objects.get_or_create(name=group_name)[0]    
    p = Permission.objects.get(codename=perm_codename, name=perm_name, content_type=perm_ct)
    new_group.permissions.add(p)
    p.save()
    return p




if __name__ == '__main__':
    print("Starting Operrisk population script...")
    populate()
    print("Population completed")