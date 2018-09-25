# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from django.conf import settings
from django.utils import timezone

from taiga.base.api import ModelListViewSet
from taiga.base.api.utils import get_object_or_404
from taiga.base.decorators import list_route
from taiga.base import exceptions as exc
from taiga.base import response

from taiga.projects import models

from taiga.projects import filters as project_filters
from taiga.projects import permissions
from taiga.projects import serializers
from taiga.projects import validators
from taiga.projects import services
from taiga.projects import utils as project_utils

class FanViewSet(ModelListViewSet):
    validator_class = validators.ProjectValidator
    queryset = models.Project.objects.all()
    permission_classes = (permissions.ProjectPermission, )
    filter_backends = (project_filters.UserOrderFilterBackend,
                       project_filters.QFilterBackend,
                       project_filters.CanViewProjectObjFilterBackend,
                       project_filters.DiscoverModeFilterBackend)

    filter_fields = (("member", "members"),
                     "is_looking_for_people",
                     "is_featured",
                     "is_backlog_activated",
                     "is_kanban_activated")

    ordering = ("name", "id")
    order_by_fields = ("total_fans",
                       "total_fans_last_week",
                       "total_fans_last_month",
                       "total_fans_last_year",
                       "total_activity",
                       "total_activity_last_week",
                       "total_activity_last_month",
                       "total_activity_last_year")

    def is_blocked(self, obj):
        return obj.blocked_code is not None

    def _get_order_by_field_name(self):
        order_by_query_param = project_filters.CanViewProjectObjFilterBackend.order_by_query_param
        order_by = self.request.QUERY_PARAMS.get(order_by_query_param, None)
        if order_by is not None and order_by.startswith("-"):
            return order_by[1:]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("owner")
        if self.request.QUERY_PARAMS.get('discover_mode', False):
            qs = project_utils.attach_members(qs)
            qs = project_utils.attach_notify_policies(qs)
            qs = project_utils.attach_is_fan(qs, user=self.request.user)
            qs = project_utils.attach_my_role_permissions(qs, user=self.request.user)
            qs = project_utils.attach_my_role_permissions(qs, user=self.request.user)
            qs = project_utils.attach_closed_milestones(qs)
        else:
            qs = project_utils.attach_extra_info(qs, user=self.request.user)

        # If filtering an activity period we must exclude the activities not updated recently enough
        now = timezone.now()
        order_by_field_name = self._get_order_by_field_name()
        if order_by_field_name == "total_fans_last_week":
            qs = qs.filter(totals_updated_datetime__gte=now - relativedelta(weeks=1))
        elif order_by_field_name == "total_fans_last_month":
            qs = qs.filter(totals_updated_datetime__gte=now - relativedelta(months=1))
        elif order_by_field_name == "total_fans_last_year":
            qs = qs.filter(totals_updated_datetime__gte=now - relativedelta(years=1))
        elif order_by_field_name == "total_activity_last_week":
            qs = qs.filter(totals_updated_datetime__gte=now - relativedelta(weeks=1))
        elif order_by_field_name == "total_activity_last_month":
            qs = qs.filter(totals_updated_datetime__gte=now - relativedelta(months=1))
        elif order_by_field_name == "total_activity_last_year":
            qs = qs.filter(totals_updated_datetime__gte=now - relativedelta(years=1))

        return qs

    def filter_queryset(self, qs):
        object_list = super().filter_queryset(qs)
        object_list = [o for o in object_list if o.is_fan_attr == True]
        return object_list

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.ProjectSerializer

        return serializers.ProjectDetailSerializer

