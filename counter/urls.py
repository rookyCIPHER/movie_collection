from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.request_count_view),
    path('/reset',views.reset_request_count)
    
]