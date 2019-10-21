from django.conf.urls import url
from .views import view_cached_users

urlpatterns = [
    url(r'^$', view_cached_users),
]
