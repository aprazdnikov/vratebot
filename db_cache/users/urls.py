from django.conf.urls import url
from .views import view_cached_users, get_users, create_users

urlpatterns = [
    url(r'^$', view_cached_users),
    url('get', get_users),
    url('create', create_users)
]
