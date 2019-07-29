from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^register/?', views.register_api),
    url(r'^login/?', views.login_api),
    url(r'^heartbeat_smartphone/?', views.heartbeat_smartphone_api),
    url(r'^heartbeat/?', views.heartbeat_smartwatch_api),
    url(r'^get_user_stat/?', views.get_user_stat_api),
]
