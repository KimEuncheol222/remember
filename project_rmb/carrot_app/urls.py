from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('location/', views.location, name='location'),
    path('trade/', views.trade, name='trade'),
    path('trade_post/', views.trade_post, name='trade_post'),
    path('write/', views.write, name='write'),
    path('chat/', views.chat, name='chat'),
    path('index/', views.index, name='index'),
    path('create_form/', views.create_form, name='create_form'),
]
