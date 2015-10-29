from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.http import HttpRequest

from .models import About
from .views import all_people


class PersonTest(TestCase):
    """ Unit tests for About model and views """
    fixtures = ['initial_data.json']
    
    def create_people(self, name="A", last_name="S", email="q@q.ua", jabber="-", skype="-"):
        return About.objects.create(name=name,
                                    last_name=last_name,
                                    email=email,
                                    jabber=jabber,
                                    skype=skype)

    def test_people_creation(self):
        a = self.create_people()
        self.assertTrue(isinstance(a, About))
        self.assertEqual(a.__str__(), a.last_name)

    def test_home_page_available(self):
        c = Client()
        response = c.get('/')
        self.assertEquals(response.status_code, 200)

    def test_home_page_contains_info(self):
        request = HttpRequest()
        response = all_people(request)
        self.assertContains(response, 'Volodymyr')
        self.assertTrue('<h2>42 Coffee Cups Test Assignment</h2>' in response.content)
        self.assertContains(response, '<a href="/request/">Request</a>')

    def test_home_page_use_about_template(self):
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'hello/about.html')
