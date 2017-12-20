from django.conf.urls import url
from standarsTools.views import index, iniciarSesion, seguimientoIndex, seguimientoConsulta, finishSinStandarIndex\
    , salir, finishSinStandarConsulta


urlpatterns = [
    url(r'^$', index),
    url(r'^iniciar_sesion/$', iniciarSesion),
    url(r'^seguimiento_index/$', seguimientoIndex),
    url(r'^seguimiento_consulta/$', seguimientoConsulta),
    url(r'^finish_sin_standar/$', finishSinStandarIndex),
    url(r'^finish_sin_standar_consulta/$', finishSinStandarConsulta),
    url(r'^salir/$', salir),
]