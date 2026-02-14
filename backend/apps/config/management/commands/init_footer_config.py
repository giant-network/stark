# -*-coding:utf-8 -*-
#
# Created on 2026/02/13, by Kiro
#

from django.core.management.base import BaseCommand
from apps.config.models import SiteConfig


class Command(BaseCommand):
    help = '初始化网站配置（页脚、导航语等）'

    def handle(self, *args, **options):
        # 初始化默认配置
        configs = [
            # 网站标题配置
            {
                'key': 'site_title',
                'value': 'Stark',
                'description': '网站主标题'
            },
            {
                'key': 'site_header',
                'value': 'Stark Dashboard',
                'description': '网站顶部标题'
            },
            {
                'key': 'site_description',
                'value': 'Stark 集合了众多站点的入口，提供一站式的便捷访问，快试试把他设为你的主页吧。',
                'description': '网站首页导航语'
            },
            # 页脚配置
            {
                'key': 'footer_link1_name',
                'value': '谷歌搜索',
                'description': '页脚第一个链接的名称'
            },
            {
                'key': 'footer_link1_url',
                'value': 'https://www.google.com/',
                'description': '页脚第一个链接的URL'
            },
            {
                'key': 'footer_link2_name',
                'value': 'ChatGPT',
                'description': '页脚第二个链接的名称'
            },
            {
                'key': 'footer_link2_url',
                'value': 'https://chatgpt.com/',
                'description': '页脚第二个链接的URL'
            },
            {
                'key': 'footer_copyright',
                'value': '元气满满部出品',
                'description': '页脚版权信息'
            },
        ]

        for config_data in configs:
            config, created = SiteConfig.objects.get_or_create(
                key=config_data['key'],
                defaults={
                    'value': config_data['value'],
                    'description': config_data['description']
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ 创建配置: {config_data["key"]} = {config_data["value"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- 配置已存在: {config_data["key"]}')
                )

        self.stdout.write(self.style.SUCCESS('\n网站配置初始化完成！'))
