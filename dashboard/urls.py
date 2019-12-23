from . import views
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    path('<str:user_id>/', views.ema_per_person),
    url(r'^main/?', views.index),
    url(r'^data/?', views.extract_data, {"exportCSV": False}, name="data"),
    url(r'^csv/?', views.extract_data, {"exportCSV": True}, name="export"),
]
