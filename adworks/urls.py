# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from adworks import views

urlpatterns = patterns('',

    url(r'^(?P<client>[-\w]+)/(?P<campaign>[-\w]+)/(?P<id>\d+)/(?P<token>[-\w]+)/(?P<revision>[-\d]+)/',
        views.banner_version, name='banner_version'),

    url(r'^(?P<client>[-\w]+)/(?P<campaign>[-\w]+)/(?P<id>\d+)/(?P<token>[-\w]+)/',
        views.banner_detail, name='banner_detail'),

    url(r'^(?P<client>[-\w]+)/(?P<campaign>[-\w]+)/(?P<token>[-\w]+)/',
        views.campaign_detail, name='campaign_detail'),

    url(r'^(?P<client>[-\w]+)/(?P<token>[-\w]+)/',
        views.client_detail, name='client_detail'),

)