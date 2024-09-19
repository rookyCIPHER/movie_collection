from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.handle_collections),
    path('/<collection_uuid>',views.handle_single_collection),
    path('/<collection_uuid>/<movie_uuid>',views.add_movie),
    
]