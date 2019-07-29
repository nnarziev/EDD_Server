from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^submit/?', views.submit_api),
]
