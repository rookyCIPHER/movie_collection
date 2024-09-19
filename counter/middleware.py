from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

class RequestCountingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        count = cache.get('request_count', 0)
        count += 1
        cache.set('request_count', count, timeout=None)
