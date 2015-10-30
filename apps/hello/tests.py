import json
from tempfile import NamedTemporaryFile
from PIL import Image

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.template.loader import render_to_string

from .models import About, AllRequest
from .views import all_people, request_list
from hello.forms import EditPersonForm


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


class LoginTest(TestCase):
    """ Unit tests for Login """
    def test_login_page_available(self):
        c = Client()
        response = c.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

    def test_login_page_use_login_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'hello/login.html')

    def test_login_page_contains_info(self):
        c = Client()
        response = c.get(reverse('login'))
        self.assertTrue('<h1>Login</h1>' in response.content)


class EditPersonTest(TestCase):
    """ Unit tests for edit person info"""
    fixtures = ['initial_data.json']
    
    def test_edit_page_available(self):
        self.client.login(username='admin', password='1')
        response = self.client.get(reverse('edit', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_edit_page_not_available(self):
        response = self.client.get(reverse('edit', kwargs={'pk': 1}))
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)

    def test_edit_page_not_available_after_logout(self):
        self.client.login(username='admin', password='1')
        response = self.client.get(reverse('logout'))
        response = self.client.get(reverse('edit', kwargs={'pk': 1}))
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)

    def get_edit_page_contains_info(self):
        self.client.login(username='admin', password='1')
        request = HttpRequest()
        response = edit_person(request)
        self.assertTrue('Edit information about peson' in response.content)
        self.assertContains(response, '<a href="/request/">Request</a>')

    def test_edit_page_use_edit_template(self):
        self.client.login(username='admin', password='1')
        response = self.client.get(reverse('edit', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'hello/edit.html')

    def test_edit_page_info_about_person(self):
        self.client.login(username='admin', password='1')
        response = self.client.get(reverse('edit', kwargs={'pk': 1}))
        person = About.objects.get(pk=1)
        self.assertContains(response, person.name)
        self.assertContains(response, person.last_name)
        self.assertContains(response, person.date)
        self.assertContains(response, person.bio)
        self.assertContains(response, person.email)
        self.assertContains(response, person.skype)
        self.assertContains(response, person.other_contact)

    def test_edit_page_uses_edit_form(self):
        self.client.login(username='admin', password='1')
        response = self.client.get(reverse('edit', kwargs={'pk': 1}))
        self.assertIsInstance(response.context['form'], EditPersonForm)

    def test_edit_page_form_success_submit(self):
        self.client.login(username='admin', password='1')
        image = Image.new('RGB', (100, 100))
        tmp_file = NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        response = self.client.post(reverse('edit', kwargs={'pk': 1}),
                                    {'name': 'Somebody',
                                     'last_name': 'Unknown',
                                     'date': '2015-01-01',
                                     'image': tmp_file,
                                     'bio': '-',
                                     'email': 'q@q.ua',
                                     'jabber': '-',
                                     'other_contact': '-',
                                     'skype': '-',},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(About.objects.get(pk=1).name, 'Somebody')
        self.assertEqual(About.objects.get(pk=1).email, 'q@q.ua')
