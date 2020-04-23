# -*-coding:utf-8 -*-
#
# Created on 2019/4/2, by felix
#

"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve
from django.urls import include, path

admin.site.site_header = u'Stark Dashboard 后台管理'
admin.site.site_title = u'Stark Dashboard'
admin.site.index_title = u'Stark Dashboard'

urlpatterns = [
    url(r'^admin/management/', admin.site.urls),
    path('api/card/', include('apps.card.urls'), name="card"),
    path('api/tag/', include('apps.tag.urls'), name="tag")
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT}),
    ]
