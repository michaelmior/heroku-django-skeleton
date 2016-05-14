from django.conf import settings as django_settings
from django.contrib.sites.shortcuts import get_current_site


def settings(request):
    return {'settings': django_settings}


def site(request):
    return {'site': get_current_site(request)}
