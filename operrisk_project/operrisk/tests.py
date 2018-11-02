from django.test import TestCase
from operrisk.models import Category, Incident
from django.contrib.auth.models import User, Group
from django.urls import reverse
import datetime
import populate_operrisk
from populate_operrisk import populate

populate()#let's create categories, groups and permissions

#########################################################################################################
def add_cat(name):#creates category (helpier function)
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

def add_inc(name,loss_amount,incident_date,category_id,description,measures_taken):#creates incident (helpier function)
    inc = Incident.objects.get_or_create(name=name,loss_amount=loss_amount,incident_date=incident_date,category_id=category_id,description=description,measures_taken=measures_taken)
    inc.save()
    return inc
#########################################################################################################

class CategoryTests(TestCase):
    def test_category_URL_name(self):
        cat = Category(name='Test category 2')
        cat.save()
        self.assertEqual(cat.URL_name, 'test-category-2')


class IncidentTests(TestCase):
    def test_ensure_loss_amount_is_positive(self):
        cur_date = datetime.date.today()
        cat = Category(name='Test category 2')
        cat.save()        
        inc = Incident(name='test',loss_amount=-10,incident_date=cur_date,category_id=cat,description='test desc',measures_taken='test measures')
        inc.save()        
        self.assertEqual((inc.loss_amount >=0), True)

    def test_ensure_incident_date_is_not_in_future(self):
        cur_date = datetime.date.today()
        incident_date = cur_date + datetime.timedelta(days=10)
        cat = Category(name='Test category 2')
        cat.save()
        inc = Incident(name='test',loss_amount=0,incident_date=incident_date,category_id=cat,description='test desc',measures_taken='test measures')
        inc.save()        
        self.assertEqual((inc.incident_date > cur_date),False)

"""
class UserTests(TestCase):
    def test_new_user_is_added_to_employees_group(self):
        user = User.objects.create_user(username='test_user',password='Test123!@#')
        user.save()
        is_member_of_employees = user.groups.filter(name='employees').exists()
        self.assertEqual(is_member_of_employees,True)



class Show_all_incidents_pViewTest(TestCase):
    def test_show_all_incidents_p_with_no_incidents(self):
        response = self.client.get(reverse('show_all_incidents_p'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Инцидентов нет")
        self.assertQuerysetEqual(response.context['incidents'],[])

    def test_show_all_incidents_p_with_incidents(self):
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
        cur_date = datetime.date.today()
        cat = Category(name='Внутреннее мошенничество')
        cat.save()
        add_inc('test_inc-1',0,cur_date,cat,'test inc-1 desc','test inc-1 measures')
        add_inc('test_inc-2',0,cur_date,cat,'test inc-2 desc','test inc-2 measures')
        add_inc('test_inc-3',0,cur_date,cat,'test inc-3 desc','test inc-3 measures')
        response = self.client.get(reverse('show_all_incidents_p'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"test_inc-1 test_inc-2 test_inc-3")
        num_inc = len(response.context['incidents'])
        self.assertEqual(num_inc,3)
        
        
"""