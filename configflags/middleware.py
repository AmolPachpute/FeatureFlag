from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FeatureFlag


class FeatureFlagMiddleware:
    """
    Description: Middleware to cache feature flags and attach i to request object so that there's
    no need to go to database for each request to check feature flags
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.cache_key = 'feature_flags'

    def __call__(self, request):
        request.feature_flags = self._get_feature_flags()
        response = self.get_response(request)
        return response

    def _get_feature_flags(self):
        flags = cache.get(self.cache_key)
        if flags is None:
            flags = self._fetch_and_cache_flags()
        return flags

    def _fetch_and_cache_flags(self):
        flags = {}
        all_flags = FeatureFlag.objects.all()
        for flag in all_flags:
            flags[flag.id] = flag.is_enabled
        # Cache the flags for 1 hour (you can adjust the timeout as needed)
        cache.set(self.cache_key, flags, timeout=3600)
        return flags


# invalidate the cache if the user updates the feature flag using post save signal
@receiver(post_save, sender=FeatureFlag)
def invalidate_feature_flag_cache(sender, instance, **kwargs):
    cache.delete('feature_flags')