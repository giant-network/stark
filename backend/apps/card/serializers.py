# -*-coding:utf-8 -*-
#
# Created on 2019/3/29, by felix
#

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.card.models import Card, Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'name', 'link')


class CardSerializer(serializers.ModelSerializer):
    menus = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ('id', 'name', 'menus', 'avatar', 'description', 'tag', 'weight', 'numbers')

    def get_menus(self, obj):
        """
        只返回未删除的菜单
        """
        menus = obj.menus.filter(is_deleted=False).order_by('-weight', '-id')
        return MenuSerializer(menus, many=True).data

    def get_avatar(self, obj):
        """
        返回图片 URL，处理空值情况
        """
        if not obj.picture:
            return None
        
        avatar_url = obj.picture.url
        request = self.context.get('request')
        
        # 如果有 request 上下文，返回完整 URL；否则返回相对路径
        if request:
            return request.build_absolute_uri(avatar_url)
        return avatar_url

