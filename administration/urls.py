from django.conf.urls import url
from administration.views import getToken, getTokenAdmin


urlpatterns = [
    url(r'^token/$', getToken),
    url(r'^tokenadmin/$', getTokenAdmin),
]