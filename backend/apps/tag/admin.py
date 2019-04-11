# -*-coding:utf-8 -*-
#
# Created on 2019/3/28, by felix
#

from django.contrib import admin
from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'is_deleted', 'created_time')
    ordering = ['-created_time']


admin.site.register(Tag, TagAdmin)
