# -*-coding:utf-8 -*-
#
# Created on 2019/3/28, by felix
#

from django.db import models
from base.models import BaseModel


class Tag(BaseModel):
    name = models.CharField(verbose_name="标签名称", max_length=10)
    weight = models.IntegerField(verbose_name="权重", default=0, help_text="数值越大越靠前")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name
        ordering = ['-weight']
