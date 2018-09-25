# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.conf.urls import include, url


class TaigaContribFanAppConfig(AppConfig):
    name = "taiga_contrib_fan"
    verbose_name = "Taiga contrib fan App Config"

    def ready(self):
        from taiga.base import routers
        from taiga.urls import urlpatterns
        from .api import FanViewSet

        router = routers.DefaultRouter(trailing_slash=False)
        router.register(r"fan", FanViewSet, base_name="fan")
        urlpatterns.append(url(r'^api/v1/', include(router.urls)))

