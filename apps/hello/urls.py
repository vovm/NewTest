from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static


urlpatterns = patterns(
    '',
    url(r'^$', 'hello.views.all_people', name='about'),
    url(r'^request/$', 'hello.views.request_list', name='request_list'),
    url(r'^request/ajax_request_list$', 'hello.views.ajax_request_list', name='ajax_list'),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
