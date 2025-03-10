from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('guns/', views.gun_list, name='guns_list'),
    path('guns/add/', views.gun_add, name='gun_add'),
    path('people/', views.person_list, name='people_list'),
    path('people/add/', views.person_add, name='person_add'),
    path('guns/assign/', views.assign_gun, name='assign_gun'),
    path('guns/return/<int:gun_id>/', views.return_gun, name='return_gun'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('soldier_dashboard/', views.soldier_dashboard, name='soldier_dashboard'),
    path('soldier_dashboard/', views.soldier_dashboard, name='soldier_dashboard'),
    path('assigned_guns/', views.view_all_assigned_guns, name='view_all_assigned_guns'),
    path('issued_guns/', views.issued_guns_list, name='issued_guns_list'),
    path('my_assigned_guns/', views.view_assigned_guns, name='view_assigned_guns'),
    path('request_gun/', views.request_gun, name='request_gun'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('guns/add/', views.gun_add, name='gun_add'),
    path('soldiers/add/', views.person_add, name='person_add'),
    path('assign/', views.assign_gun, name='assign_gun'),
]
