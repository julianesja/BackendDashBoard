from django.shortcuts import render
from django.http import HttpResponse
from reporte_ogx.proceso.ProcesoOGVPodio import ProcesoOGVPodio
from reporte_ogx.proceso.ProcesoOGEPodio import ProcesoOGEPodio
from reporte_ogx.proceso.ProcesoOGTPodio import ProcesoOGTPodio
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

@csrf_exempt
def openFechaUROGV(request):
    if request.method == "GET":
        fechaInicio = request.GET.get('fechaInicio', None)
        fechaFin = request.GET.get('fechaFin', None)
        comite = request.GET.get('comite', None)
        objProcesoOGVPodio = ProcesoOGVPodio()
        lstOpen = objProcesoOGVPodio.consultarMes(comite, fechaInicio, fechaFin)
        return HttpResponse(json.dumps(lstOpen), content_type="application/json")

@csrf_exempt
def openFechaUROGE(request):
    if request.method == "GET":
        fechaInicio = request.GET.get('fechaInicio', None)
        fechaFin  = request.GET.get('fechaFin', None)
        comite = request.GET.get('comite', None)
        objProcesoOGEPodio = ProcesoOGEPodio()
        lstOpen = objProcesoOGEPodio.consultarMes(comite, fechaInicio, fechaFin)
        return HttpResponse(json.dumps(lstOpen), content_type="application/json")

@csrf_exempt
def openFechaUROGT(request):
    if request.method == "GET":
        fechaInicio = request.GET.get('fechaInicio', None)
        fechaFin  = request.GET.get('fechaFin', None)
        comite = request.GET.get('comite', None)
        objProcesoOGTPodio = ProcesoOGTPodio()
        lstOpen = objProcesoOGTPodio.consultarMes(comite, fechaInicio, fechaFin)
        return HttpResponse(json.dumps(lstOpen), content_type="application/json")
