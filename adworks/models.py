# -*- coding: utf-8 -*-
import re
from hashlib import md5
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template import defaultfilters


def get_upload_to(instance, filename):
    return '%s/%s/%s' % (str(instance._meta.app_label), 
                            str(instance._meta.module_name), 
                            re.sub('[^\.0-9a-zA-Z()_-]', '_', filename))


class Client(models.Model):
	title           = models.CharField(_(u'Title'), max_length=100, unique=True)
	slug            = models.CharField(_(u'Slug'), max_length=100)
	about           = models.TextField(_(u'About'), blank=True)
	website         = models.CharField(_(u'Website'), max_length=150)
	logo            = models.ImageField(_(u'Logo'), upload_to=get_upload_to, blank=True)
	token           = models.CharField(_(u'Token'), max_length=64, blank=True)
	created_date    = models.DateTimeField(_(u'Created date'), auto_now_add=True)	
	
	def __unicode__(self):
		return u'%s' % self.title

	@models.permalink
	def get_absolute_url(self):
		return ('client_detail',(), {
		    'client': self.slug,
   	        'token': self.token
   	    })

	def save(self):
		if not self.slug:
			self.slug=defaultfilters.slugify(self.title)
   		if not self.token:
			hash_str = md5(str(datetime.now())).hexdigest()
   			self.token = hash_str
   		super(Client, self).save()

		
class Campaign(models.Model):
	client           = models.ForeignKey(Client, blank=False, null=False)
	title            = models.CharField(_(u'Title'), max_length=100)
	slug             = models.CharField(_(u'Slug'), max_length=100)
	summary          = models.TextField(_(u'Summary'), blank=True)
	mediaplan        = models.FileField(_(u'Media plan'), upload_to=get_upload_to, blank=True)
	token            = models.CharField(_(u'Token'), max_length=64)
	created_date     = models.DateTimeField(_(u'Created date'), auto_now_add=True)	
	
	def __unicode__(self):
		return u'%s' % self.title

	@models.permalink
	def get_absolute_url(self):
		return ('campaign_detail',(), {
		    'client': self.client.slug,
		    'campaign': self.slug,
   	        'token': self.token
   	    })

	def save(self):
		if not self.slug:
			self.slug=defaultfilters.slugify(self.title)
   		if not self.token:
			hash_str = md5(str(datetime.now())).hexdigest()
   			self.token = hash_str
   		super(Campaign, self).save()

		
class Size(models.Model):
    """size model"""
    ATTRIBUTE_CHOICES = (
        (1, _(u'Normal')),
        (2, _(u'Floating')),
        (3, _(u'Pageskin')),
        (4, _(u'Rich')),
        (5, _(u'Widget')),
    )
    
    width           = models.IntegerField(_(u'Width'), default=0, blank=False, null=False)
    height          = models.IntegerField(_(u'Height'), default=0, blank=False, null=False)
    attribute       = models.IntegerField(_(u'Attribute'), choices=ATTRIBUTE_CHOICES, default=1)	

    def __unicode__(self):
        return u'%s x %s (%s)' % (self.width, self.height, self.get_attribute_display())

		
class Banner(models.Model):
	campaign           = models.ForeignKey(Campaign, blank=False, null=False)
	size           	   = models.ForeignKey(Size, blank=False, null=False)
	description        = models.TextField(_(u'Description'), blank=True)
	token              = models.CharField(_(u'Token'), max_length=64)
	created_date       = models.DateTimeField(_(u'Created date'), auto_now_add=True)	
	
	def __unicode__(self):
		return u'%s' % self.size
		
	@models.permalink
	def get_absolute_url(self):
		return ('banner_detail',(), {
		    'client': self.campaign.client.slug,
		    'campaign': self.campaign.slug,
   	        'id': self.id,
   	        'token': self.token
   	    })

   	@property
   	def client(self):
   	    return self.campaign.client
   
   	def save(self):
   		if not self.token:
			hash_str = md5(str(datetime.now())).hexdigest()
   			self.token = hash_str
   		super(Banner, self).save()

   		
class Version(models.Model):
	banner           = models.ForeignKey(Banner, blank=False, null=False)
	revision         = models.IntegerField(_(u'Revision'), blank=True, null=False)
	comment          = models.TextField(_(u'Comment'), blank=True)
	file             = models.FileField(_(u'File'), upload_to=get_upload_to, blank=False)
	alternative      = models.ImageField(_(u'Alternative'), upload_to=get_upload_to, blank=True)
	created_date     = models.DateTimeField(_(u'Created date'), auto_now_add=True)	
	
	def __unicode__(self):
		return u'Revizyon: %s' % self.revision

	@models.permalink
	def get_absolute_url(self):
		return ('banner_version',(), {
		    'client': self.banner.client.slug,
		    'campaign': self.banner.campaign.slug,
   	        'id': self.banner.id,
   	        'token': self.banner.token,
   	        'revision': self.revision
   	    })

	def save(self):
   		if not self.revision:
			versions=self.banner.version_set.order_by('-revision')
			if not versions:
				self.revision=1
			else:
				self.revision=versions[0].revision+1	
   		super(Version, self).save()
		
