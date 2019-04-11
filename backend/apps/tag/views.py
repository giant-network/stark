# -*-coding:utf-8 -*-
#
# Created on 2019/3/29, by felix
#

from apps.tag.models import Tag

from base.views import BaseViewSet
from rest_framework.response import Response
from .serializers import TagSerializer, TagNestedSerializer
from rest_framework.decorators import detail_route, list_route


class TagViewSet(BaseViewSet):
    queryset = Tag.objects.filter(is_deleted=False).order_by('-weight')
    serializer_class = TagSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        """
        tag 列表
        """
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

    @detail_route(methods=['GET'], url_path="cards")
    def fetch_tag_related_cards(self, request, *args, **kwargs):
        """
        获取tag相关的card
        """
        instance = self.get_object()
        serializer = TagNestedSerializer(instance=instance, context={"request": request})
        return Response(serializer.data)
