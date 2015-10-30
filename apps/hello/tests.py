import json

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.template.loader import render_to_string

from .models import About, AllRequest
from .views import all_people, request_list


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

    def test_home_page_use_about_template(self):
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'hello/about.html')


class AllRequestTest(TestCase):
    """ Unit tests for Request model and views"""
    def test_all_request_page_available(self):
        c = Client()
        response = c.get(reverse('request_list'))
        self.assertEquals(response.status_code, 200)

    def test_request_page_returns_correct_html(self):
        request = HttpRequest()
        response = request_list(request)
        expected_content = render_to_string('hello/request.html')
        self.assertEqual(response.content.decode('utf8'), expected_content)

    def test_request_works(self):
        AllRequest.objects.all().delete()
        c = Client()
        response = c.get('/')
        self.assertEqual(AllRequest.objects.count(), 1)
        self.assertEqual(AllRequest.objects.get(pk=1).__str__(), "Request - 1")

    def test_all_request_page_contains_info(self):
        request = HttpRequest()
        response = request_list(request)
        self.assertTrue('<h2>Last 10 Requests</h2>' in response.content)

    def test_all_request_page_use_request_template(self):
        response = self.client.get(reverse('request_list'))
        self.assertTemplateUsed(response, 'hello/request.html')

    def test_all_request_ajax_list_json(self):
        response = self.client.get(reverse('request_list'))
        response = self.client.get(reverse('ajax_list'))
        readable_json = json.loads(response.content)
        self.assertEqual(readable_json[0]["req_path"], '/request/')
