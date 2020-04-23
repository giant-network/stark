# -*-coding:utf-8 -*-
#
# Created on 2019/3/28, by felix
#

from django.db import models
from base.models import BaseModel

from apps.tag.models import Tag


class Card(BaseModel):
    name = models.CharField(verbose_name="卡片名称", max_length=50)
    picture = models.ImageField(verbose_name="图标", upload_to='card')
    description = models.CharField(verbose_name="描述", max_length=500, null=True, blank=True)
    tag = models.ManyToManyField(Tag, verbose_name="卡片标签", related_name='cards')
    weight = models.IntegerField(verbose_name="权重", default=0, help_text="数值越大越靠前")
    numbers = models.BigIntegerField(verbose_name="点击量", default=0, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "导航卡片"
        verbose_name_plural = verbose_name
        ordering = ['-weight', '-id']


class Menu(BaseModel):
    name = models.CharField(verbose_name="菜单名", max_length=10)
    weight = models.IntegerField(verbose_name="权重", default=0, help_text="数值越大越靠前")
    link = models.URLField(verbose_name="超链接")
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, verbose_name="卡片", null=True, related_name='menus')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "卡片底部菜单"
        verbose_name_plural = verbose_name
        ordering = ['-weight']