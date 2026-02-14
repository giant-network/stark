# -*-coding:utf-8 -*-
#
# Created on 2026/02/13, by Kiro
#

from django.contrib import admin
from .models import SiteConfig


class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description', 'is_deleted', 'updated_time')
    search_fields = ['key', 'value', 'description']
    list_filter = ('is_deleted',)
    ordering = ['key']
    
    # 只读字段
    readonly_fields = ('created_time', 'updated_time')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('key', 'value', 'description')
        }),
        ('状态信息', {
            'fields': ('is_deleted', 'created_time', 'updated_time'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(SiteConfig, SiteConfigAdmin)
