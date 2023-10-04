from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('location/', views.location, name='location'),
    path('set_region/', views.set_region, name='set_region'),
    path('set_region_certification/', views.set_region_certification, name='set_region_certification'),
    path('trade/', views.trade, name='trade'),
    path('trade_post/<int:pk>/', views.trade_post, name='trade_post'),
    path('alert/<str:alert_message>/', views.alert, name='alert'),
    path('write/', views.write, name='write'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('chat/', views.chat, name='chat'),
    path('index/', views.index, name='index'),
    path('create_form/', views.create_form, name='create_form'),
]
