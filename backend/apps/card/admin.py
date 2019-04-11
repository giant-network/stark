# -*-coding:utf-8 -*-
#
# Created on 2019/3/28, by felix
#

from django.contrib import admin
from .models import Card, Menu


class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_tag_name', 'weight', 'picture', 'created_time')
    list_filter = ('tag',)
    readonly_fields = ('numbers',)
    search_fields = ['tag__name', 'name']
    ordering = ['-created_time']

    def get_tag_name(self, obj):
        return '，'.join([obj['name'] for obj in obj.tag.filter(is_deleted=False).values('name')])

    get_tag_name.short_description = '关联的标签'


class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_card_name', 'weight', 'link', 'is_deleted', 'created_time')
    search_fields = ['card__name', 'name']
    ordering = ['-created_time']

    def get_card_name(self, obj):
        return obj.card.name


admin.site.register(Menu, MenuAdmin)
admin.site.register(Card, CardAdmin)
