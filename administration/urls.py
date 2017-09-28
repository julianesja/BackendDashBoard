from django.conf.urls import url
from administration.views import getToken


urlpatterns = [
    url(r'^token/$', getToken),
]