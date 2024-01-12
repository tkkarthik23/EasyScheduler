"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
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
from django.urls import path
from . import views
from . import helpers

urlpatterns = [
    path('', views.index, name='index'),
    path('sprintPage/', views.sprintsini, name='sprintPage'),
    path('selectedSprint/', views.renderSprint, name='renderSprint'),
    path('addSprint/', views.createSprint, name='createSprint'),
    path('addUser/', views.addUser, name='addUser'),
    path('userAddition/', views.userAddition, name='userAddition'),
    path('addTask/', views.addTask, name='addTask'),
    path('createTask/', views.createTask, name='createTask'),
    path('planSprint/', views.planSprint, name='planSprint'),
    path('deleteTask/', views.deleteTask, name='deleteTask'),
    path('deleteUser/', views.deleteUser, name='deleteUser'),
    path('plannedSprint/', views.plannedSprint, name='plannedSprint'),
]
