# -*- coding: utf-8 -*-
import json
from StringIO import StringIO
from tempfile import NamedTemporaryFile
from PIL import Image

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.core.management import call_command

from .models import About, AllRequest, SignalData
from .views import request_list
from hello.forms import EditPersonForm, EditRequestForm


class PersonTest(TestCase):
    """ Unit tests for About model and views """
    fixtures = ['initial_data.json']

    def create_people(self, name="A", last_name="S", email="q@q.ua",
                      jabber="-", skype="-"):
        return About.objects.create(name=name,
                                    last_name=last_name,
                                    email=email,
                                    jabber=jabber,
                                    skype=skype)

    def test_people_creation(self):
        """ Test for create person """
        a = self.create_people()
        self.assertTrue(isinstance(a, About))
        self.assertEqual(a.__str__(), a.last_name)

    def test_home_page_doesnt_contain_info(self):
        """ Test home page doesnt contain info """
        About.objects.all().delete()
        response = self.client.get(reverse('about'))
        self.assertNotContains(response, 'Name')

    def test_db_contains_two_records(self):
        """ Test db contains two records """
        About.objects.all().delete()
        self.create_people('GoodName', 'StrangeLastName')
        self.create_people()
        response = self.client.get(reverse('about'))
        self.assertContains(response, 'GoodName')

    def test_home_page_contains_cyrillic(self):
        """ Test home page contains cyrillic """
        About.objects.all().delete()
        self.create_people(u"Петя")
        response = self.client.get(reverse('about'))
        self.assertContains(response, u"Петя")

    def test_home_page_available(self):
        """ Test home page available """
        response = self.client.get(reverse('about'))
        self.assertEquals(response.status_code, 200)

    def test_home_page_contains_info(self):
        """ Test home page contains info """
        response = self.client.get(reverse('about'))
        self.assertTrue(response.context['people'], 'Melnychuk')

    def test_home_page_use_about_template(self):
        """ Test home page use template """
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'hello/about.html')


class AllRequestTest(TestCase):
    """ Unit tests for Request model and views"""
    def test_last_request_page_available(self):
        """ Test last request page available """
        response = self.client.get(reverse('request_list'))
        self.assertEquals(response.status_code, 200)

    def test_request_works(self):
        """ Test requests """
        AllRequest.objects.all().delete()
        self.client.get(reverse('about'))
        self.assertEqual(AllRequest.objects.count(), 1)
        self.assertEqual(AllRequest.objects.get(pk=1).priority, 0)
        self.assertEqual(AllRequest.objects.get(pk=1).__str__(), "Request - 1")

    def test_last_request_page_contains_info(self):
        """ Test last request page available """
        response = self.client.get(reverse('request_list'))
        self.assertTrue('<h2>Last 10 Requests</h2>' in response.content)

    def test_last_request_page_use_request_template(self):
        """ Test last request use template """
        response = self.client.get(reverse('request_list'))
        self.assertTemplateUsed(response, 'hello/request.html')

    def test_priority_request_page_available(self):
        """ Test priority page available """
        response = self.client.get(reverse('request_priority'))
        self.assertEquals(response.status_code, 200)

    def test_edit_request_page_available(self):
        """ Test edit page available """
        response = self.client.get(reverse('edit_request', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, 200)

    def test_priority_request_page_use_request_template(self):
        """ Test priority page use template """
        response = self.client.get(reverse('request_priority'))
        self.assertTemplateUsed(response, 'hello/request_priority.html')

    def test_edt_request_page_use_edit_template(self):
        """ Test edit page use template """
        response = self.client.get(reverse('edit_request', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'hello/edit_request.html')

    def test_edit_request_page_info_about_request(self):
        """ Test edit page contains info """
        response = self.client.get(reverse('edit_request', kwargs={'pk': 1}))
        req = AllRequest.objects.get(pk=1)
        self.assertContains(response, req.priority)
        self.assertContains(response, req.method)
        self.assertContains(response, req.path)

    def test_edit_request_page_uses_edit_form(self):
        """ Test edit page uses form """
        response = self.client.get(reverse('edit_request', kwargs={'pk': 1}))
        self.assertIsInstance(response.context['form'], EditRequestForm)

    def test_priority_request_page_contains_info(self):
        """ Test priority page contains info """
        response = self.client.get(reverse('request_priority'))
        self.assertTrue('Requests with priority' in response.content)

    def test_request_priority_page_order(self):
        """ Test priority page order """
        AllRequest.objects.all().delete()
        self.client.get(reverse('about'))
        self.client.get(reverse('request_list'))
        req = AllRequest.objects.get(pk=1)
        req.priority = 9
        req.save()
        response = self.client.get(reverse('request_priority'))
        self.assertEqual(response.context['requests'][0].priority, 9)
        self.assertEqual(response.context['requests'][1].priority, 0)

    def test_request_date_page_order(self):
        """ Test request page order """
        AllRequest.objects.all().delete()
        self.client.get(reverse('about'))
        response = self.client.get(reverse('request_list'))
        self.assertEqual(response.context['requests'][0].path, '/request/')
        self.assertEqual(response.context['requests'][1].path, '/')

    def test_edit_page_has_default_priority(self):
        """ Test edit page has default priority """
        AllRequest.objects.all().delete()
        self.client.get(reverse('request_list'))
        self.assertEqual(AllRequest.objects.get(pk=1).priority, 0)

    def test_edit_request_form_success_submit(self):
        """ Test edit page form success submit """
        self.client.get(reverse('request_list'))
        data = {'priority': 1}
        response = self.client.post(reverse('edit_request',
                                            kwargs={'pk': 1}), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(AllRequest.objects.get(pk=1).priority, 1)

    def test_edit_request_form_with_no_data(self):
        """ Test edit page form with no data """
        self.client.get(reverse('request_list'))
        data = {}
        response = self.client.post(reverse('edit_request',
                                            kwargs={'pk': 1}), data)
        self.assertTrue('This field is required' in response.content)
        self.assertEqual(response.status_code, 200)

    def test_edit_request_form_with_bad_data(self):
        """ Test edit page form with bad data """
        self.client.get(reverse('about'))
        data = {'priority': 111}
        response = self.client.post(reverse('edit_request',
                                            kwargs={'pk': 1}), data)
        self.assertTrue('value is less than or equal to 9' in response.content)
        self.assertEqual(response.status_code, 200)

    def test_last_request_ajax_list_json(self):
        """ Test json """
        self.client.get(reverse('request_list'))
        response = self.client.get(reverse('ajax_list'))
        readable_json = json.loads(response.content)
        self.assertEqual(readable_json[0]["req_path"], '/request/')


class LoginTest(TestCase):
    """ Unit tests for Login """
    def test_login_page_available(self):
        """ Test login page available """
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

    def test_login_page_use_login_template(self):
        """ Test login page use template """
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'hello/login.html')

    def test_login_page_contains_info(self):
        """ Test login page contains info """
        response = self.client.get(reverse('login'))
        self.assertTrue('<h1>Login</h1>' in response.content)

    def test_login_page_form_with_no_data(self):
        """ Test login page with no data """
        data = {}
        response = self.client.post(reverse('login'), data)
        self.assertTrue('This field is required' in response.content)

    def test_login_page_form_with_bad_data(self):
        """ Test login page with bad data """
        data = {'username': 'admin', 'password': 111}
        response = self.client.post(reverse('login'), data)
        self.assertTrue('Please enter a correct username' in response.content)


class EditPersonTest(TestCase):
    """ Unit tests for edit person info"""
    fixtures = ['initial_data.json']

    def test_edit_page_available(self):
        """ Test edit page available """
        self.client.login(username='admin', password='1')
        response = self.client.get(reverse('edit', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_edit_page_not_available(self):
        """ Test edit page doesnt available """
        response = self.client.get(reverse('edit', kwargs={'pk': 1}))
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)

    def test_edit_page_not_available_after_logout(self):
        """ Test edit page doesnt available after logout"""
        self.client.login(username='admin', password='1')
        self.client.get(reverse('logout'))
        response = self.client.get(reverse('edit', kwargs={'pk': 1}))
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)

    def get_edit_page_contains_info(self):
        """ Test edit page contains info """
        self.client.login(username='admin', password='1')
        response = self.client.get(reverse('edit', kwargs={'pk': 1}))
        self.assertTrue('Edit information about peson' in response.content)
        self.assertContains(response, '<a href="/request/">Request</a>')

    def test_edit_page_uses_edit_template(self):
        """ Test edit page uses template """
        self.client.login(username='admin', password='1')
        response = self.client.get(reverse('edit', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'hello/edit.html')

    def test_edit_page_info_about_person(self):
        """ Test edit page has info about person """
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
        """ Test edit page uses form """
        self.client.login(username='admin', password='1')
        response = self.client.get(reverse('edit', kwargs={'pk': 1}))
        self.assertIsInstance(response.context['form'], EditPersonForm)

    def test_edit_page_form_success_submit(self):
        """ Test edit page with correct data """
        self.client.login(username='admin', password='1')
        image = Image.new('RGB', (100, 100))
        tmp_file = NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        self.client.post(reverse('edit', kwargs={'pk': 1}),
                         {'name': 'Somebody',
                          'last_name': 'Unknown',
                          'date': '2015-01-01',
                          'image': tmp_file,
                          'bio': '-',
                          'email': 'q@q.ua',
                          'jabber': '-',
                          'other_contact': '-',
                          'skype': '-'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(About.objects.get(pk=1).name, 'Somebody')
        self.assertEqual(About.objects.get(pk=1).email, 'q@q.ua')

    def test_edit_page_form_with_bad_data(self):
        """ Test edit page with bad data """
        self.client.login(username='admin', password='1')
        image = Image.new('RGB', (100, 100))
        tmp_file = NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        response = self.client.post(reverse('edit', kwargs={'pk': 1}),
                                    {'name': 'Somebody',
                                     'last_name': 'Unknown',
                                     'date': '2015-99-99',
                                     'image': tmp_file,
                                     'bio': '-',
                                     'email': 'q@q.ua',
                                     'jabber': '-',
                                     'other_contact': '-',
                                     'skype': '-'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue('Enter a valid date' in response.content)

    def test_edit_page_form_with_no_data(self):
        """ Test edit page with no data """
        self.client.login(username='admin', password='1')
        response = self.client.post(reverse('edit', kwargs={'pk': 1}),
                                    {'name': 'Somebody',
                                     'last_name': 'Unknown',
                                     'date': '2015-01-01'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue('This field is required' in response.content)


class TagTest(TestCase):
    """ Unit tests for own tag"""
    fixtures = ['initial_data.json']

    def test_admin_tag_with_user1(self):
        """ Test admin tag """
        self.client.login(username='admin', password='1')
        response = self.client.get(reverse('edit', kwargs={'pk': 1}))
        self.assertContains(response,
                            '<a href="/admin/hello/about/1/">(admin)</a>')


class OwnCommandTest(TestCase):
    """ Unit tests for own management command - count_objects"""
    fixtures = ['initial_data.json']

    def test_command_style(self):
        """ Test own command """
        out = StringIO()
        call_command('count_objects', stderr=out)
        self.assertIn("Error: Model About has 1 objects", out.getvalue())
        self.assertIn("Error: Model User has 1 objects", out.getvalue())


class SignalDataTest(TestCase):
    """ Unit tests for SignalData"""

    def test_post_create(self):
        """ Test create signal """
        SignalData.objects.all().delete()
        self.client.get(reverse('about'))
        self.assertEqual(SignalData.objects.count(), 1)
        log_info = SignalData.objects.get(pk=1).message
        self.assertEqual(log_info, "Create row with id 1 in AllRequest")

    def test_post_update(self):
        """ Test update signal """
        SignalData.objects.all().delete()
        self.client.get(reverse('request_list'))
        data = {'priority': 1}
        self.client.post(reverse('edit_request',
                                 kwargs={'pk': 1}), data)
        log_info = SignalData.objects.get(pk=3).message
        self.assertEqual(log_info, "Update row with id 1 in AllRequest")

    def test_post_delete(self):
        """ Test delete signal """
        SignalData.objects.all().delete()
        self.client.get(reverse('about'))
        AllRequest.objects.all().delete()
        self.assertEqual(SignalData.objects.count(), 2)
        log_info = SignalData.objects.get(pk=2).message
        self.assertEqual(log_info, "Delete row with id 1 in AllRequest")
