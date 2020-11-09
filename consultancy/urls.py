"""consultancy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:heck/id=2/pj=1
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from appointments import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name=
         'templates/registration/logged_out.html'), name='logout1'),
    path('admin/', admin.site.urls),
    path('check/id=<int:id>', views.check, name='check'),
    path('check/id=<int:id>/pj=<int:pk>', views.check, name='check_pj'),
    path('check/', views.check, name='check'),
    path('delete/', views.delete, name='delete'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('new/', views.new, name='new'),
    path('', views.check, name='index'),  # Fix: route to real home page
    path('singup', views.singup, name='singup'),
    ]
