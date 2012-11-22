# -*- coding: utf-8 -*-
import re
import hashlib
import datetime
from django.test import TestCase
from adworks.models import (get_upload_to, Client, Campaign, Dimension, 
                                Attribute, Banner, Version)


class AdworksTestCase(TestCase):
    fixtures = ['test']
    
class ClientModelTest(AdworksTestCase):
        
    def test_stringification(self):
        client = Client.objects.get(pk=1)
        self.failUnlessEqual(client.__unicode__(), '%s' % client.title)

    def test_upload_logo(self):
        client = Client.objects.get(pk=1)
        filename = 'logo.png'
        path = get_upload_to(client, filename)
        self.failIfEqual(filename, path)
        FILE_RE = re.compile('^%(filepath)s/[a-f0-9]{5}.png$' %
                            {'filepath': '%s/%s' % (
                                    str(client._meta.app_label), 
                                    str(client._meta.module_name))})

        self.failUnless(FILE_RE.search(path))

        

class CampaignModelTest(AdworksTestCase):
    
    def test_stringification(self):
        campaign = Campaign.objects.get(pk=1)
        self.failUnlessEqual(campaign.__unicode__(), '%s' % campaign.title)

    def test_upload_mediaplan(self):
        campaign = Campaign.objects.get(pk=1)
        filename = 'mediaplan.xls'
        path = get_upload_to(campaign, filename)
        self.failIfEqual(filename, path)
        FILE_RE = re.compile('^%s/%s/[a-f0-9]{10}.xls$' % (
                                    str(campaign._meta.app_label), 
                                    str(campaign._meta.module_name)))
        self.failUnless(FILE_RE.search(path))
        

class DimensionModelTest(AdworksTestCase):
    
    def test_stringification(self):
        pass


class AttributeModelTest(AdworksTestCase):
    
    def test_stringification(self):
        pass


class BannerModelTest(AdworksTestCase):
    
    def test_stringification(self):
        pass


class VersionModelTest(AdworksTestCase):
    
    def test_stringification(self):
        pass

