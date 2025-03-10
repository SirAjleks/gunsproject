from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('guns/', views.gun_list, name='guns_list'),
    path('guns/add/', views.gun_add, name='gun_add'),
    path('people/', views.person_list, name='people_list'),
    path('people/add/', views.person_add, name='person_add'),
    path('guns/assign/', views.assign_gun, name='assign_gun'),
    path('guns/return/<int:gun_id>/', views.return_gun, name='return_gun'),
]
