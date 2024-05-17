from django.db import models
from django.contrib.auth.models import User

class FeatureFlag(models.Model):
    id = models.CharField(max_length=10, unique=True, primary_key=True)
    description = models.CharField(max_length=100, unique=True)
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.id


class FeatureFlagMetaData(models.Model):

    feature_flag = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - created by - {}".format(self.feature_flag.id, self.created_by)
