"""
Definition of urls for firma.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from django.conf.urls import include
from django.contrib import admin
import app.forms
import app.views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import RedirectView

admin.autodiscover()


# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Авторизация',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^links$', app.views.links, name='links'),
    url(r'^anketa$', app.views.anketa, name='anketa'),
    url(r'^registration$', app.views.registration, name='registration'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog$', app.views.blog, name='blog'),
    url(r'^(?P<parametr>\d+)/$', app.views.blogpost, name='blogpost'),
    url(r'^videopost$', app.views.videopost, name='videopost'),
    url(r'^newpost$', app.views.newpost, name='newpost'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/app/content/favicon.ico', permanent=True)),
    url(r'^tyr$', app.views.tyr, name='tyr'),
    url(r'^turkey$', app.views.turkey, name='turkey'),
    url(r'^russia$', app.views.russia, name='russia'),
    url(r'^tunisia$', app.views.tunisia, name='tunisia'),
    url(r'^greece$', app.views.greece, name='greece'),
    url(r'^spain$', app.views.spain, name='spain'),
    url(r'^cyprus$', app.views.cyprus, name='cyprus'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()