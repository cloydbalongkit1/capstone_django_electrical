from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='logout_user'),
    path('register', views.register, name='register'),

    path('home', views.home, name='home'),
    path('calculate', views.calculate, name='calculate'),

    path('power_triangle', views.power_triangle, name="power_triangle"),


]
