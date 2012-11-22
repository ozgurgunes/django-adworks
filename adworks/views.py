# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from adworks.models import *


def client_detail(request,client,token):
	client = Client.objects.get(slug=client)
	campaigns= client.campaign_set.all()
	extra_context = {
        'client': client,
	    'campaigns': campaigns,
        }
	if client.token==token:
		return render_to_response('adworks/client_detail.html',extra_context,context_instance=RequestContext(request))
	else:
		return render_to_response('error.html')
	
def campaign_detail(request,client,campaign,token):
	campaign = Campaign.objects.get(slug=campaign)
	banners = campaign.banner_set.all()
	extra_context = {
        'campaign': campaign,
	    'banners': banners
        }
	if campaign.token==token:
		return render_to_response('adworks/campaign_detail.html',extra_context,context_instance=RequestContext(request))
	else:
		return render_to_response('error.html')

def banner_detail(request,client,campaign,id,token):
	banner=Banner.objects.get(id=id)
	versions=banner.version_set.all().order_by('-revision')
	version = versions[0]
	extra_context = {
        'banner': banner,
        'versions': versions,
        'version': version
        }
	if banner.token==token:
		return render_to_response('adworks/show_banner_detail.html',extra_context,context_instance=RequestContext(request))
	else:
		return render_to_response('error.html')

def banner_version(request,client,campaign,id,token,revision):
	banner=Banner.objects.get(id=id)
	versions=banner.version_set.all().order_by('-revision')
	version=versions.get(revision=revision)
	extra_context = {
        'banner': banner,
        'versions': versions,
	    'version': version
        }
	if banner.token==token:
		return render_to_response('adworks/show_banner_detail.html',extra_context,context_instance=RequestContext(request))
	else:
		return render_to_response('error.html')
	
   
	
