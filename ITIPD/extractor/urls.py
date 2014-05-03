__author__ = 'sven'
from django.conf.urls import patterns, url, include
from django.views.generic import ListView
from extractor.models import DocumentationUnit
from extractor import views

urlpatterns = patterns('',
     # url(r'example', IndexView.as_view()),
      url(r'^example/([0-9]{4})/$', 'extractor.views.testing'),
      #url(r'^example/', AboutView.as_view()),
      (r'^example/$', ListView.as_view(model=DocumentationUnit)),
      url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
      # url(r'^(?P<doc_id>\d+)/vote/$', views.vote, name='vote'),
      url(r'^vote/$', views.vote, name='vote')
)

