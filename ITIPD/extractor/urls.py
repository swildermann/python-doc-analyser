__author__ = 'sven'
from django.conf.urls import patterns, url
from extractor.models import DocumentationUnit, MappingUnitToUser
from extractor import views

urlpatterns = patterns('',
      url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
      url(r'^(?P<pk>\d+)/$', views.view_unit, name='detail'),
      url(r'^vote/$', views.vote, name='vote'),
      url(r'^parent/(?P<pk>\d+)/$', views.show_parent, name='parent'),
      url(r'^file/(?P<pk>\d+)/$', views.show_file, name='file'),
      url(r'^myunits/$', views.show_next_unit, name='show_next'),
      url(r'^markedunits/$', views.marked_units, name='marked_units'),
      url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/pydoc/login'}),
      url(r'^randomunit/$', views.random_mapping, name = 'random_mapping'),
)
