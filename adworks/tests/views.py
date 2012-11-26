# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from adworks.models import (get_upload_to, Client, Campaign, Dimension, 
                                Attribute, Banner, Version)


class AdworksViewsTestCase(TestCase):
    fixtures = ['test']

    def test_client_detail_view(self):
        client = Client.objects.get(pk=1)
        response = self.client.get(reverse('client_detail', kwargs={
                            'pk': client.id, 'token':client.token}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adworks/client_detail.html')

    def test_campaign_detail_view(self):
        campaign = Campaign.objects.get(pk=1)
        response = self.client.get(reverse('campaign_detail', kwargs={
                            'pk': campaign.id, 'token':campaign.token}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adworks/campaign_detail.html')

    def test_banner_detail_view(self):
        banner = Banner.objects.get(pk=1)
        response = self.client.get(reverse('banner_detail', kwargs={
                            'pk': banner.id, 'token':banner.token}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adworks/banner_detail.html')

    def test_version_detail_view(self):
        banner = Banner.objects.get(pk=1)
        version = banner.version_set.all()[0]
        response = self.client.get(reverse('version_detail', kwargs={
                            'pk': banner.id, 'token':banner.token, 'revision': version.revision}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adworks/banner_detail.html')

    def test_invalid_client_token(self):
        client = Client.objects.get(pk=1)
        response = self.client.get(reverse('client_detail', kwargs={
                            'pk': client.id, 'token':'invalidtoken'}))
        self.assertEqual(response.status_code, 404)

    def test_invalid_campaign_token(self):
        campaign = Campaign.objects.get(pk=1)
        response = self.client.get(reverse('campaign_detail', kwargs={
                            'pk': campaign.id, 'token':'invalidtoken'}))
        self.assertEqual(response.status_code, 404)

    def test_invalid_banner_token(self):
        banner = Banner.objects.get(pk=1)
        response = self.client.get(reverse('banner_detail', kwargs={
                            'pk': banner.id, 'token':'invalidtoken'}))
        self.assertEqual(response.status_code, 404)
