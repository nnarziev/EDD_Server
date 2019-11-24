"""YouNoOne_Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import os
from django.urls import re_path
from django.urls import include
from YouNoOne_Server import views

if not os.path.exists('audio/'):
    os.mkdir('audio')
    print('directory "audio/" has been created')

urlpatterns = [
    re_path(r'user/', include('user.urls')),
    re_path(r'ema/', include('ema.urls')),
    re_path(r'sensor_data/', include('sensor_data.urls')),
    re_path(r'dashboard/', include('dashboard.urls')),
    re_path(r'submit_audio', views.submit_audio)
]
