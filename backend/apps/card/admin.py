# -*-coding:utf-8 -*-
#
# Created on 2019/3/28, by felix
#

from django.contrib import admin
from django.contrib import messages
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
    
    def delete_model(self, request, obj):
        """
        删除单个 Card 时的逻辑闭环检查
        """
        # 检查是否有关联的 Menu
        related_menus = obj.menus.filter(is_deleted=False)
        if related_menus.exists():
            menu_count = related_menus.count()
            messages.warning(
                request,
                f'警告：该卡片还有 {menu_count} 个关联的菜单。建议先删除或转移这些菜单。'
            )
        
        # 执行软删除
        super().delete_model(request, obj)
    
    def delete_queryset(self, request, queryset):
        """
        批量删除 Card 时的逻辑闭环检查
        """
        # 统计关联的 Menu 数量
        total_menus = 0
        for card in queryset:
            total_menus += card.menus.filter(is_deleted=False).count()
        
        if total_menus > 0:
            messages.warning(
                request,
                f'警告：这些卡片共有 {total_menus} 个关联的菜单。建议先删除或转移这些菜单。'
            )
        
        # 执行批量软删除
        super().delete_queryset(request, queryset)


class MenuAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_card_name', 'weight', 'link', 'is_deleted', 'created_time')
    search_fields = ['card__name', 'name']
    ordering = ['-created_time']
    list_filter = ('is_deleted',)

    def get_name(self, obj):
        # 防御性编程：检查 card 是否存在且未删除
        if obj.card and not obj.card.is_deleted:
            return obj.card.name + '-' + obj.name
        return obj.name + ' (卡片已删除)'
    
    get_name.short_description = '菜单名称'

    def get_card_name(self, obj):
        # 防御性编程：检查 card 是否存在且未删除
        if obj.card and not obj.card.is_deleted:
            return obj.card.name
        return '(已删除)'
    
    get_card_name.short_description = '关联的卡片'
    
    def get_queryset(self, request):
        """
        重写查询集，默认只显示未删除的数据
        可以通过筛选器查看已删除的数据
        """
        qs = super().get_queryset(request)
        # 如果没有筛选 is_deleted，默认只显示未删除的
        if not request.GET.get('is_deleted__exact'):
            return qs.filter(is_deleted=False)
        return qs


admin.site.register(Menu, MenuAdmin)
admin.site.register(Card, CardAdmin)

