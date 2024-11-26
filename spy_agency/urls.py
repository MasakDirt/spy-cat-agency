from django.urls import path, include
from rest_framework.routers import DefaultRouter

from spy_agency.views import SpyCatViewSet, MissionViewSet


router = DefaultRouter()
router.register("spy_cats", SpyCatViewSet, "spy_cat")
router.register("missions", MissionViewSet, "mission")

urlpatterns = [path("", include(router.urls))]

app_name = "spy_agency"
