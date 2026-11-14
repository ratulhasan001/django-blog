from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('author/', include('author.urls')),
    path('profile/', include('profiles.urls')),
    path('post/', include('posts.urls')),
    path('category/', include('categories.urls')),
    path('', views.home, name='homepage'),
]
