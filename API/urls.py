from django.contrib import admin
from django.urls import path, include
# Huy 29/10/2022
from . import views

urlpatterns = [
    path('index', views.index, name = "index"),
    # Route is named as "index"
    path('search', views.search),
    path('add', views.add),
    path('delete', views.delete),
]
