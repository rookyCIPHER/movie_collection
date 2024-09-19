from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict
import json
from .models import Collection, MoviesInCollection
from django.contrib.auth import get_user_model
import uuid
import requests

User = get_user_model()

@csrf_exempt
def handle_collections(request):
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization', None)

        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Authorization token required'}, status=401)

        token = str(auth_header.split(' ')[1])

        try:
            user = User.objects.get(token=token)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Users correct token should be in the header with the key as Authorization and starting with Bearer '}, status=401)
        
        collections = user.collections.all()

        top_genres = defaultdict(int)

        for collection in collections:
            for movie in collection.movies.all():
                samp_list=str(movie.genre).split(',')
                for genre in samp_list:
                    top_genres[genre] += 1

        sorted_keys_desc = sorted(top_genres, key=top_genres.get, reverse=True)
        

        top_three_genres = sorted_keys_desc[:3]

        collections_data = []
        for collection in collections:
            collections_data.append({
                'title': collection.title,
                'uuid': str(collection.uuid),
                'description': collection.description
            })
        
        return JsonResponse({
            'top_three_genres': top_three_genres,
            'collections': collections_data
        })
    
    elif request.method=="POST":
        try:
            auth_header = request.headers.get('Authorization', None)
            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse({'error': 'Authorization token required'}, status=401)


            token = str(auth_header.split(' ')[1])

            try:
                user = User.objects.get(token=token)
            except ReferenceError as e:
                return JsonResponse({'error': f'Users correct token should be in the header with the key as Authorization and starting with Bearer {e}'}, status=401)


            data = json.loads(request.body)

            title = data.get('title')
            description = data.get('description')


            if not title or not description:
                return JsonResponse({'error': 'Title and description are required.'}, status=400)

            new_collection = Collection.objects.create(
                title=title,
                description=description,
                user=user,
                uuid=str(uuid.uuid4()) 
            )


            return JsonResponse({
                'collection_uuid': str(new_collection.uuid)

            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)







@csrf_exempt
def handle_single_collection(request,collection_uuid):
    if request.method=="GET":
        try:
            coll=Collection.objects.get(uuid=str(collection_uuid))
            movies=coll.movies.all()
            lst_movies=[]
            for i in movies:
                lst_movies.append(i.title)
            return JsonResponse({
                'title': coll.title,
                'description': coll.description,
                'movies':str(lst_movies)
            },status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    if request.method=="DELETE":
        try:
            coll=Collection.objects.get(uuid=str(collection_uuid))
            coll.delete()
            return JsonResponse({'msg':"Collection Deleted Successfully"},status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)        
        
@csrf_exempt
def add_movie(request,collection_uuid,movie_uuid):
    try:
        coll=Collection.objects.get(uuid=str(collection_uuid))
        response = requests.get('http://127.0.0.1:8000/movie',verify=False).json()
        req_movie={}

        while response["next"]!='null':
            flag=False
            for movie in response['results']:
                if str(movie['uuid'])==str(movie_uuid):
                    req_movie=movie
                    flag=True
                    break
            if(flag):
                break
            response = requests.get(response['next'],verify=False).json()

        new_movie=MoviesInCollection.objects.create(
                collection=coll,
                movie_id=str(req_movie['uuid']),
                title=str(req_movie['title']),
                description=str(req_movie['description']),
                genre=str(req_movie['genres'])
            )
        
        return HttpResponse(status=200)
        


    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
