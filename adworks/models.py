# -*- coding: utf-8 -*-
import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template import defaultfilters

from uuidfield import UUIDField


def get_upload_to(instance, filename):
    return '%s/%s/%s' % (str(instance._meta.app_label), 
                            str(instance._meta.module_name), 
                            re.sub('[^\.0-9a-zA-Z()_-]', '_', filename))


class Client(models.Model):
    title           = models.CharField(_(u'Title'), max_length=100, unique=True)
    slug            = models.CharField(_(u'Slug'), max_length=100, unique=True)
    about           = models.TextField(_(u'About'), blank=True)
    website         = models.CharField(_(u'Website'), max_length=150)
    logo            = models.ImageField(_(u'Logo'), upload_to=get_upload_to, blank=True)
    token           = UUIDField(auto=True)

    class Meta: 
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

    def __unicode__(self):
    	return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
    	return ('client_detail',(), {
    	    'pk': self.pk,
            'token': self.token
        })

    def save(self, *args, **kwargs):
    	if not self.slug:
    		self.slug=defaultfilters.slugify(self.title)
    	super(Client, self).save(*args, **kwargs)

		
class Campaign(models.Model):
    client          = models.ForeignKey(Client)
    title           = models.CharField(_(u'Title'), max_length=100)
    slug            = models.CharField(_(u'Slug'), max_length=100)
    summary         = models.TextField(_(u'Summary'), blank=True)
    attachment      = models.FileField(_(u'Attachment'), 
                                upload_to=get_upload_to, blank=True,
                                help_text=_('Upload campaign documents (brief, media plan, etc.)'))
    token           = UUIDField(auto=True)
	
    class Meta:
        verbose_name = _('Campaign')
        verbose_name_plural = _('Campaigns')

    def __unicode__(self):
    	return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
    	return ('campaign_detail',(), {
    	    'pk': self.pk,
            'token': self.token
        })

    def save(self, *args, **kwargs):
    	if not self.slug:
    		self.slug=defaultfilters.slugify(self.title)
    	super(Campaign, self).save(*args, **kwargs)

		
class Attribute(models.Model):
    title            = models.CharField(_(u'Title'), max_length=32)
    description      = models.TextField(_(u'Description'), blank=True)

    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')

    def __unicode__(self):
        return u'%s' % self.title

		
class Dimension(models.Model):
    width           = models.IntegerField(_(u'Width'), default=0, blank=False)
    height          = models.IntegerField(_(u'Height'), default=0, blank=False)
    description      = models.TextField(_(u'Description'), blank=True)

    class Meta:
        verbose_name = _('Dimension')
        verbose_name_plural = _('Dimensions')

    def __unicode__(self):
        return u'%sx%s' % (self.width, self.height)

		
class Banner(models.Model):
    campaign        = models.ForeignKey(Campaign)
    dimension       = models.ForeignKey(Dimension)
    attribute       = models.ForeignKey(Attribute)
    clicktag        = models.URLField(_('Click Tag'), blank=True)
    description     = models.TextField(_(u'Description'), blank=True)
    token           = UUIDField(auto=True)
	
    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')

    def __unicode__(self):
        return u'%s - %s' % (self.dimension, self.attribute)
		
    @models.permalink
    def get_absolute_url(self):
    	return ('banner_detail',(), {
            'pk': self.pk,
            'token': self.token
        })

    @property
    def client(self):
        return self.campaign.client
   

class Version(models.Model):
    banner          = models.ForeignKey(Banner)
    revision        = models.IntegerField(_(u'Revision'), blank=True)
    note            = models.TextField(_(u'Note'), blank=True)
    file            = models.FileField(_(u'File'), upload_to=get_upload_to, 
                                 blank=False, null=False)
    alternative     = models.ImageField(_(u'Alternative'), upload_to=get_upload_to, 
                                 blank=True)
    created_date    = models.DateTimeField(_(u'Created date'), auto_now_add=True)	
	
    class Meta:
        verbose_name = _('Version')
        verbose_name_plural = _('Versions')

    def __unicode__(self):
    	return u'%s: %s' % (_('Revision'), self.revision)

    @models.permalink
    def get_absolute_url(self):
    	return ('version_detail',(), {
            'pk': self.banner.pk,
            'token': self.banner.token,
            'revision': self.revision
        })

    def save(self, *args, **kwargs):
    	if not self.revision:
    		versions=self.banner.version_set.order_by('-revision')
    		if not versions:
    			self.revision=1
    		else:
    			self.revision=versions[0].revision+1	
    	super(Version, self).save(*args, **kwargs)
		