from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.core.urlresolvers import reverse_lazy


urlpatterns = patterns(
    '',
    url(r'^$', 'hello.views.all_people', name='about'),
    url(r'^request/$', 'hello.views.request_list', name='request_list'),
    url(r'^request/ajax_request_list$', 'hello.views.ajax_request_list',
        name='ajax_list'),
    url(r'^edit/(?P<pk>[0-9]+)/$', 'hello.views.edit_person', name='edit'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {"template_name": "hello/login.html"}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {"next_page": reverse_lazy('about')}, name="logout"),
    url(r'^edit_request/(?P<pk>[0-9]+)/$', 'hello.views.edit_request',
        name='edit_request'),
    url(r'^request/priority/$', 'hello.views.request_list_priority',
        name='request_priority'),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
