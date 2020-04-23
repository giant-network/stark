# -*-coding:utf-8 -*-
#
# Created on 2019/3/28, by felix
#

from django.db.models import Q

from apps.card.models import Card, Menu

from base.views import BaseViewSet
from rest_framework.response import Response
from .serializers import CardSerializer, MenuSerializer
from rest_framework.decorators import detail_route, list_route


class CardViewSet(BaseViewSet):
    """
    card列表
    """

    queryset = Card.objects.filter(is_deleted=False).order_by('-weight', '-id')
    serializer_class = CardSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', None)
        if limit == '-1':
            serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response({'results': serializer.data, 'count': len(serializer.data)})
        else:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    @detail_route(methods=['GET'], url_path='menus')
    def fetch_card_menus(self, request, pk):
        """
        获取card相关的菜单项
        """
        instance = self.get_object()

        menus = instance.menus.filter(is_deleted=False).order_by('-weight', '-id')
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

    @list_route(methods=['GET'], url_path='search')
    def fetch_card_menus(self, request, *args, **kwargs):
        """
        搜索菜单项
        """

        q = request.query_params.get('q', '')

        cards = Card.objects.filter(Q(name__icontains=q) | Q(description__icontains=q), is_deleted=False).order_by('-weight', '-id')
        serializer = CardSerializer(cards, many=True, context={"request": request})
        return Response(serializer.data)

    @list_route(methods=['GET'], url_path='collect')
    def fetch_card_collected(self, request, *args, **kwargs):
        """
        根据ID搜索菜单项
        """
        ids = request.query_params.get('ids', '')
        ids_value = None

        try:
            ids_value = eval(ids)
        except Exception as e:
            ids_value = []
        finally:
            ids_list = ids_value if type(ids_value) == list else []

        cards = Card.objects.filter(id__in=ids_list, is_deleted=False).order_by('-weight', '-id')
        serializer = CardSerializer(cards, many=True, context={"request": request})
        return Response(serializer.data)


class MenuViewSet(BaseViewSet):
    """
    子菜单列表
    """

    queryset = Menu.objects.filter(is_deleted=False).order_by('-weight', '-id')
    serializer_class = MenuSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', None)
        if limit == '-1':
            serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response({'results': serializer.data, 'count': len(serializer.data)})
        else:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)