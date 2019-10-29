from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^submit/?', views.submit_api),
    url(r'^locations_submit/?', views.submit_geofencing_api),
    url(r'^app_usage_stats/?', views.handle_usage_stats_submit)
]
