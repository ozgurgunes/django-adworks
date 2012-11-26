# -*- coding: utf-8 -*-
from django.contrib import admin
from adworks.models import (Client, Campaign, Dimension, 
                                Attribute, Banner, Version)


def smart_truncate(content, length=100, suffix='...'):
    if len(str(content)) <= length:
        return content
    else:
        return content[:length].rsplit(' ', 1)[0]+suffix


class ClientAdmin(admin.ModelAdmin):
    def campaign_count(self, instance):
        return instance.campaign_set.count()

    list_display  = ('title', 'website', 'campaign_count')
    search_fields = ('title', 'about')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'logo', 'website', 'about')
    

class CampaignAdmin(admin.ModelAdmin):
    def banner_count(self, instance):
        return instance.banner_set.count()

    list_display  = ('title', 'client', 'banner_count')
    list_filter   = ('client__title',)
    search_fields = ('title', 'summary', 'client')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('client', 'title', 'slug', 'summary', 'attachment')


class VersionInline(admin.StackedInline):
    model=Version
    extra=1


class BannerAdmin(admin.ModelAdmin):
    def version_count(self, instance):
        return instance.version_set.count()

    list_display  = ('dimension', 'attribute', 'campaign', 'version_count')	
    list_filter   = ('dimension__width', 'dimension__height', 
                        'attribute__title', 'campaign__title', 'campaign__client__title')
    search_fields = ('description',)
    fields = ('campaign', ('dimension', 'attribute'), 'description')
    inlines         = [VersionInline,]


class AttributeAdmin(admin.ModelAdmin):    
    def summary(self, instance):
        return smart_truncate(instance.description)
        
    list_display  = ('title', 'summary')


class DimensionAdmin(admin.ModelAdmin):
    def dimension(self, instance):
        return u'%sx%s px' % (instance.width, instance.height)

    def summary(self, instance):
        return smart_truncate(instance.description)
        
    list_display  = ('dimension', 'summary')
    list_filter   = ('width', 'height')


admin.site.register(Client, ClientAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Dimension, DimensionAdmin)
admin.site.register(Attribute, AttributeAdmin)
