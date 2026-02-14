# -*-coding:utf-8 -*-
#
# Created on 2026/02/13, by Kiro
#

from django.urls import path
from .views import get_footer_config, get_site_config

urlpatterns = [
    path('footer/', get_footer_config, name='footer_config'),
    path('site/', get_site_config, name='site_config'),
]
