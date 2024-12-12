from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='logout_user'),
    path('register', views.register, name='register'),

    path('home', views.home, name='home'),
    path('query_messages', views.query_messages, name='query_messages'),
    path('calculate', views.calculate, name='calculate'),
    path('electrical_theory', views.electrical_theory, name='electrical_theory'),
    path('about', views.about, name='about'),
    
    path('profile_view', views.profile_view, name='profile_view'),
    path('edit_profile', views.edit_profile, name='edit_profile'),

    path('power_triangle', views.power_triangle, name="power_triangle"),
    path('phasor_diagram', views.phasor_diagram, name="phasor_diagram"),
    path('save_calc', views.save_calc, name='save_calc'),
    
    path('user_calculations', views.user_calculations, name='user_calculations'),
    path('delete_previous_calc/<int:id>', views.delete_previous_calc, name='delete_previous_calc'),

    path('help_solve', views.help_solve, name='help_solve'),

    path('contacted_messages', views.contacted_messages, name='contacted_messages'),

]

