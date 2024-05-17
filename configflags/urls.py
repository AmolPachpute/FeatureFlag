from django.urls import path
from .views import (FeatureFlagViewSet, qa_environment_operations, stage_environment_operations,
                    prod_environment_operations)

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'flags', FeatureFlagViewSet)

# NOTE: Below urls are for env wise just for testing and not an ideal case in realtime.
urlpatterns = [
    path("qa", qa_environment_operations, name="qa_environment_operations"),
    path("stage", stage_environment_operations, name="stage_environment_operations"),
    path("prod", prod_environment_operations, name="prod_environment_operations"),
] + router.urls