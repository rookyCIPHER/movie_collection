from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt

def request_count_view(request):
    if(request.method=='GET'):
        count = cache.get('request_count', 0)
        return JsonResponse({'requests': count})
    else:
        return JsonResponse({'error': 'Invalid request type'},status=500)

@csrf_exempt
def reset_request_count(request):
    if(request.method=='POST'):
        cache.set('request_count', 0, timeout=None)
        return JsonResponse({'message': 'request count reset successfully'},status=200)
    else:
        return JsonResponse({'error': 'Invalid request type'},status=500)