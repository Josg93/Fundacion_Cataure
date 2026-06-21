from django.urls import path
from . import views

urlpatterns = [
    path('', views.galeria , name='inicio'),
    path('galeria/', views.galeria , name='galeria'),
]