from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('reviews/', views.reviews_view, name='reviews'),
]