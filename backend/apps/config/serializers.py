# -*-coding:utf-8 -*-
#
# Created on 2026/02/13, by Kiro
#

from rest_framework import serializers
from .models import SiteConfig


class SiteConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfig
        fields = ('key', 'value')
