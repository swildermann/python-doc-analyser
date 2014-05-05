__author__ = 'sven'
from django.conf.urls import patterns, url, include
from django.views.generic import ListView
from extractor.models import DocumentationUnit, MappingUnitToUser
from extractor import views

urlpatterns = patterns('',
      (r'^list/$', ListView.as_view(model=DocumentationUnit)),
      url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
      url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
      url(r'^vote/$', views.vote, name='vote'),
      url(r'^parent/(?P<pk>\d+)/$', views.ParentView.as_view(), name='parent'),
      url(r'^myunits/$', ListView.as_view(model=MappingUnitToUser))

)

