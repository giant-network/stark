# -*-coding:utf-8 -*-
#
# Created on 2019/3/28, by felix
#

from rest_framework.routers import DefaultRouter

from apps.card.views import CardViewSet, MenuViewSet

router = DefaultRouter()
router.register(r'', CardViewSet, base_name='card')
router.register(r'menu', MenuViewSet, base_name='card_menu')
urlpatterns = router.urls
