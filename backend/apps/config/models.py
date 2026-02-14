# -*-coding:utf-8 -*-
#
# Created on 2026/02/13, by Kiro
#

from django.db import models
from base.models import BaseModel


class SiteConfig(BaseModel):
    """
    网站配置模型
    """
    # 配置键（唯一标识）
    key = models.CharField(verbose_name="配置键", max_length=50, unique=True, db_index=True)
    # 配置值
    value = models.TextField(verbose_name="配置值")
    # 配置描述
    description = models.CharField(verbose_name="描述", max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.key}: {self.value}"
    
    class Meta:
        verbose_name = "网站配置"
        verbose_name_plural = verbose_name
        ordering = ['key']
    
    @classmethod
    def get_config(cls, key, default=''):
        """
        获取配置值
        """
        try:
            config = cls.objects.get(key=key, is_deleted=False)
            return config.value
        except cls.DoesNotExist:
            return default
    
    @classmethod
    def set_config(cls, key, value, description=''):
        """
        设置配置值
        """
        config, created = cls.objects.get_or_create(
            key=key,
            defaults={'value': value, 'description': description}
        )
        if not created:
            config.value = value
            if description:
                config.description = description
            config.save()
        return config
