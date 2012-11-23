# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from adworks import views

urlpatterns = patterns('',

    url(r'^client/(?P<pk>\d+)/(?P<token>[-\w]+)/',
        views.ClientDetail.as_view(), name='client_detail'),

    url(r'^campaign/(?P<pk>\d+)/(?P<token>[-\w]+)/',
        views.CampaignDetail.as_view(), name='campaign_detail'),

    url(r'^banner/(?P<pk>\d+)/(?P<token>[-\w]+)/(?P<revision>\d+)/',
        views.BannerDetail.as_view(), name='version_detail'),

    url(r'^banner/(?P<pk>\d+)/(?P<token>[-\w]+)/',
        views.BannerDetail.as_view(), name='banner_detail'),

)