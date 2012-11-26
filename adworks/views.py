# -*- coding: utf-8 -*-
from django.views.generic import DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from django.http import Http404
from adworks.models import Client, Campaign, Banner, Version

class BaseDetail(DetailView):
    slug_field = 'token'
    slug_url_kwarg = 'token'
    
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        token = self.kwargs.get(self.slug_url_kwarg, None)

        if pk is not None and token is not None:
            queryset = queryset.filter(pk=pk, token=token)

        # If none of those are defined, it's an error.
        else:
            raise AttributeError("Generic detail view %s must be called with "
                                 "an object pk and a token both."
                                 % self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class ClientDetail(BaseDetail):
    model = Client
        

class CampaignDetail(BaseDetail):
    model = Campaign
        

class BannerDetail(BaseDetail):
    model = Banner
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(BaseDetail, self).get_context_data(**kwargs)
        versions = self.object.version_set.all().order_by('-revision') 
        revision = self.kwargs.get('revision')
        try:
            if revision:
                version = versions.get(revision=revision)
            else:
                version = versions[0]
        except:
            version = None
        self.version = version
        self.extra_context.update({'version': version})
        context.update(self.extra_context)
        return context
