from django.conf.urls import url
from reporte_ogx.views import openFechaUROGV,openFechaUROGE,openFechaUROGT


urlpatterns = [
    url(r'^open_ogv/$', openFechaUROGV),
    url(r'^open_oge/$', openFechaUROGE),
    url(r'^open_ogt/$', openFechaUROGT),

]