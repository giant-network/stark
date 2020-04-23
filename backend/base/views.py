# -*-coding:utf-8 -*-
#
# Created on 2019/3/29, by felix
#

from django_filters.rest_framework import DjangoFilterBackend
from collections import OrderedDict
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework.decorators import list_route
from rest_framework.pagination import (LimitOffsetPagination,
                                       _positive_int)


class CustomLimitOffsetPagination(LimitOffsetPagination):
    limit = None

    def get_limit(self, request):
        if self.limit_query_param:
            try:
                value = request.query_params[self.limit_query_param]
                if int(value) == -1:
                    return int(value)
                else:
                    return _positive_int(
                        value,
                        strict=True,
                        cutoff=self.max_limit
                    )
            except (KeyError, ValueError):
                pass
        return self.default_limit

    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)
        if self.limit == -1:
            self.count = self.get_count(queryset)
            return list(queryset)
        return super().paginate_queryset(queryset, request, view=None)

    def get_paginated_response(self, data):
        if self.limit == -1:
            return Response(OrderedDict([
                ('count', self.count),
                ('next', None),
                ('previous', None),
                ('results', data)
            ]))
        return super().get_paginated_response(data)


class BaseViewSet(ModelViewSet):
    pagination_class = CustomLimitOffsetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    # @list_route(methods=['post'], url_path='find')
    # def find(self, request, *args, **kwargs):
    #     """
    #     批量查询，支持id与name字段的批量查询
    #     :param request:
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     data = request.data
    #     filter_data = {}
    #     for field in self.filter_fields:
    #         value = data.pop(field, None)
    #         if value:
    #             filter_data[field] = value
    #
    #     ids = data.pop('id', None)
    #     if ids:
    #         self.queryset = self.get_queryset().filter(id__in=ids)
    #
    #     names = data.pop('name', None)
    #     if names:
    #         self.queryset = self.get_queryset().filter(name__in=names)
    #
    #     return self.list(request, *args, **kwargs)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def update(self, request, *args, **kwargs):
        """
        put /entity/{pk}/
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        delete /entity/{pk}/
        """
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)