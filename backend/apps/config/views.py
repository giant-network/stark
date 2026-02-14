# -*-coding:utf-8 -*-
#
# Created on 2026/02/13, by Kiro
#

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SiteConfig


@api_view(['GET'])
def get_footer_config(request):
    """
    获取页脚配置
    """
    # 获取配置，如果不存在则返回默认值
    link1_name = SiteConfig.get_config('footer_link1_name', '谷歌搜索')
    link1_url = SiteConfig.get_config('footer_link1_url', 'https://www.google.com/')
    link2_name = SiteConfig.get_config('footer_link2_name', 'ChatGPT')
    link2_url = SiteConfig.get_config('footer_link2_url', 'https://chatgpt.com/')
    copyright_text = SiteConfig.get_config('footer_copyright', '元气满满部出品')
    
    return Response({
        'link1': {
            'name': link1_name,
            'url': link1_url
        },
        'link2': {
            'name': link2_name,
            'url': link2_url
        },
        'copyright': copyright_text
    })


@api_view(['GET'])
def get_site_config(request):
    """
    获取网站配置（包括导航语、标题等）
    """
    # 获取配置
    site_title = SiteConfig.get_config('site_title', 'Stark')
    site_header = SiteConfig.get_config('site_header', 'Stark Dashboard')
    site_description = SiteConfig.get_config(
        'site_description', 
        'Stark 集合了众多站点的入口，提供一站式的便捷访问，快试试把他设为你的主页吧。'
    )
    
    return Response({
        'title': site_title,
        'header': site_header,
        'description': site_description
    })
