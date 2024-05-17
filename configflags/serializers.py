from .models import FeatureFlag, FeatureFlagMetaData
from rest_framework import serializers


class FeatureFlagSerializer(serializers.ModelSerializer):
    """
    Decription: Serializer for FeatureFlag model
    """
    class Meta:
        model = FeatureFlag
        fields = "__all__"


class FeatureFlagMetaDataSerializer(serializers.ModelSerializer):
    """
    Decription: Serializer for FeatureFlagMetaData model
    """
    class Meta:
        model = FeatureFlagMetaData
        fields = "__all__"
