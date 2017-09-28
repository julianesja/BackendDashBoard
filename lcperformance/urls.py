from django.conf.urls import url
from lcperformance.views import Comite, Semanas, Programas, OdStage, LcPerFormace


urlpatterns = [
    url(r'^comite/$', Comite),
    url(r'^weekly/$', Semanas),
    url(r'^product/$', Programas),
    url(r'^od_stage/$', OdStage),
    url(r'^lc_performance/$', LcPerFormace),
]