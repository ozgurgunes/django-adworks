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
        FILE_RE = re.compile('^%(filepath)s/logo.png$' %
                            {'filepath': '%s/%s' % (
                                    str(client._meta.app_label), 
                                    str(client._meta.module_name))})

        self.failUnless(FILE_RE.search(path))
        
        
    def test_token(self):
        client = Client.objects.create(title='test client')
        self.failUnlessEqual(len(client.token), 32)
        

class CampaignModelTest(AdworksTestCase):
    
    def test_stringification(self):
        campaign = Campaign.objects.get(pk=1)
        self.failUnlessEqual(campaign.__unicode__(), '%s' % campaign.title)

    def test_upload_mediaplan(self):
        campaign = Campaign.objects.get(pk=1)
        filename = 'attachment.xls'
        path = get_upload_to(campaign, filename)
        self.failIfEqual(filename, path)
        FILE_RE = re.compile('^%s/%s/attachment.xls$' % (
                                    str(campaign._meta.app_label), 
                                    str(campaign._meta.module_name)))
        self.failUnless(FILE_RE.search(path))

    def test_token(self):
        client = Client.objects.create(title='test client')
        campaign = client.campaign_set.create(title='test campaign')
        self.failUnlessEqual(len(campaign.token), 32)
        

class DimensionModelTest(AdworksTestCase):
    
    def test_stringification(self):
        dimension = Dimension.objects.get(pk=1)
        self.failUnlessEqual(dimension.__unicode__(), 
                '%sx%s' % (dimension.width, dimension.height))


class AttributeModelTest(AdworksTestCase):
    
    def test_stringification(self):
        attribute = Attribute.objects.get(pk=1)
        self.failUnlessEqual(attribute.__unicode__(), '%s' % attribute.title)


class BannerModelTest(AdworksTestCase):
    
    def test_stringification(self):
        banner = Banner.objects.get(pk=1)
        self.failUnlessEqual(banner.__unicode__(), 
                '%s - %s' % (banner.dimension, banner.attribute))

    def test_token(self):
        dimension = Dimension.objects.create(width=300, height=250)
        attribute = Attribute.objects.create(title='test attribute')
        client = Client.objects.create(title='test client')
        campaign = client.campaign_set.create(title='test campaign')
        banner = campaign.banner_set.create(dimension=dimension, attribute=attribute)
        self.failUnlessEqual(len(campaign.token), 32)


class VersionModelTest(AdworksTestCase):
    
    def get_form(self):
        
        class VersionForm(ModelForm):
            class Meta:
                model = Version
            
        return VersionForm
    
    def test_stringification(self):
        version = Version.objects.get(pk=1)
        self.failUnlessEqual(version.__unicode__(), 
                'Revision: %s' % version.revision)
                
    def test_upload_file(self):
        version = Version.objects.get(pk=1)
        filename = 'banner.swf'
        path = get_upload_to(version, filename)
        self.failIfEqual(filename, path)
        FILE_RE = re.compile('^%(filepath)s/banner.swf$' %
                            {'filepath': '%s/%s' % (
                                    str(version._meta.app_label), 
                                    str(version._meta.module_name))})

        self.failUnless(FILE_RE.search(path))
        
    def test_revision(self):
        banner = Banner.objects.get(pk=1)
        version = banner.version_set.create()
        self.failUnlessEqual(version.revision, 2)
