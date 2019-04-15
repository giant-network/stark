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
    menus = MenuSerializer(read_only=True, many=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ('id', 'name', 'menus', 'avatar', 'description', 'tag', 'weight',
                                                   'numbers')

    def get_avatar(self, obj):
        request = self.context.get('request')
        avatar_url = obj.picture.url
        # return request.build_absolute_uri(avatar_url)
        return avatar_url

