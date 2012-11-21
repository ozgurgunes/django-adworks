# -*- coding: utf-8 -*-
from django.contrib import admin
from adworks.models import *

class ClientAdmin(admin.ModelAdmin):
    list_display  = ('title', 'website', 'created_date')
    search_fields = ('title', 'about')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
      (None,                {'fields':  ['title', 'slug', 'about', 'website', 'logo']}),
    ]
admin.site.register(Client, ClientAdmin)

class CampaignAdmin(admin.ModelAdmin):
    list_display  = ('title', 'client', 'created_date')
    list_filter   = ('client',)
    search_fields = ('title', 'summary', 'client')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
      (None,                {'fields':  ['client', 'title', 'slug', 'summary', 'mediaplan']}),
    ]
admin.site.register(Campaign, CampaignAdmin)

class VersionInline(admin.StackedInline):
    model=Version
    extra=1

class BannerAdmin(admin.ModelAdmin):
    list_display  = ('size', 'campaign')	
    list_filter   = ('size', 'campaign')
    search_fields = ('description',)
    fieldsets = [
      (None,                {'fields':  ['campaign', 'size', 'description']}),
    ]
    inlines         = [VersionInline,]

admin.site.register(Banner, BannerAdmin)

class SizeAdmin(admin.ModelAdmin):
    list_display  = ('width', 'height', 'attribute')	
    list_filter   = ('attribute',)
admin.site.register(Size, SizeAdmin)
