from django.urls import path

from . import views

urlpatterns = [
    path('', views.writeup, name='writeup'),
    path('classify/', views.classify, name='classify'),
]
