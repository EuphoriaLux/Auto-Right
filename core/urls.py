from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.homepage, name='homepage'),
    path('', views.index, name='index'),
]
