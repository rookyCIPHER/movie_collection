import requests
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
import os,time


def get_movies(request):
    url = os.getenv('THIRD_PARTY_url')
    username = os.getenv('THIRD_PARTY_username')
    password = os.getenv('THIRD_PARTY_password')

    while True:
        try:
            response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)
            if(response.status_code==200):
                data = response.json()
                return JsonResponse(data)
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}. Retrying...")

        time.sleep(2)

        
