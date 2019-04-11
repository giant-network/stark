# -*-coding:utf-8 -*-
#
# Created on 2019/3/28, by felix
#

from rest_framework.routers import DefaultRouter

from apps.tag.views import TagViewSet

router = DefaultRouter()
router.register(r'', TagViewSet, base_name='tag')
urlpatterns = router.urls
