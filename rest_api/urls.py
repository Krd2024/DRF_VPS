from rest_api.views import ServerSerializerSet
from rest_framework.routers import DefaultRouter
from django.urls import include, path


router = DefaultRouter()
router.register(r"server", ServerSerializerSet, basename="item")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
