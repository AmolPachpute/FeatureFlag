from functools import wraps
from .models import FeatureFlag, FeatureFlagMetaData
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import FeatureFlagSerializer, FeatureFlagMetaDataSerializer
from rest_framework.decorators import api_view


class FeatureFlagViewSet(viewsets.ModelViewSet):
    """
    Description Inheriting ModelViewSet for GET, PUT,PATCH, DELETE operations for feature flags
    """
    queryset = FeatureFlag.objects.all()
    serializer_class = FeatureFlagSerializer


class FeatureFlagMetaDataViewSet(viewsets.ModelViewSet):
    """
    Description Inheriting ModelViewSet for GET, PUT,PATCH, DELETE operations for feature flags meta data
    """
    queryset = FeatureFlagMetaData.objects.all()
    serializer_class = FeatureFlagMetaDataSerializer


def feature_flag_enabled(flag_name):
    """
        Description: Decorator to check whether a feature is enabled or not.
        Returns: 403 if flag is disabled
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if flag_name in request.feature_flags and request.feature_flags[flag_name]:
                return view_func(request, *args, **kwargs)
            else:
                return Response({"error": "Feature not enabled"}, status=status.HTTP_403_FORBIDDEN)
        return _wrapped_view
    return decorator


@api_view(('GET',))
@feature_flag_enabled("stage_enabled")
def stage_environment_operations(request):
    # The feature is enabled, do something
    return Response("Feature flag for stage server is enabled.", status=status.HTTP_200_OK)


@api_view(('GET',))
@feature_flag_enabled("qa_enabled")
def qa_environment_operations(request):
    # The feature is enabled, do something
    return Response("Feature flag for qa server is enabled.", status=status.HTTP_200_OK)


@api_view(('GET',))
@feature_flag_enabled("production_enabled")
def prod_environment_operations(request):
    # The feature is enabled, do something
    return Response("Feature flag for production server is enabled.", status=status.HTTP_200_OK)
