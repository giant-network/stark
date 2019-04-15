# -*-coding:utf-8 -*-
#
# Created on 2019/3/29, by felix
#

from rest_framework import serializers

from apps.card.models import Card, Menu
from apps.tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'weight')


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('name', 'link', 'weight')


class CardSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(read_only=True, many=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ('id', 'name', 'avatar', 'description', 'menus', 'weight')

    def get_avatar(self, obj):
        request = self.context.get('request')
        avatar_url = obj.picture.url
        # return request.build_absolute_uri(avatar_url)
        return avatar_url


class TagNestedSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ('name', 'cards')
