from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from lcperformance.models import  comite, weekly, product, od_stage
from lcperformance.serializers import ComiteSerializer, WeeklySerializer, ProgramSerializer, OdStageSerializer
from lcperformance.Process.ConsultaLCPerformance import ConsultaLCPerformance
import json
from django.views.decorators.csrf import ensure_csrf_cookie

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def Comite(request):
    if request.method == "GET":
        lstComite = comite.objects.all()
        serializer = ComiteSerializer(lstComite, many=True)
        return JSONResponse(serializer.data)
        #return HttpResponse(json.dumps({"nombre" : Comite, "Area" : Area}), content_type="application/json")

@csrf_exempt
def Semanas(request):
    if request.method == "GET":
        year = request.GET.get('year', None)
        if year == None:
            lstWeekly = weekly.objects.all().order_by('init_date')
        else:
            lstWeekly = weekly.objects.filter(init_date__year__gte=year).order_by('init_date')
        serializer = WeeklySerializer(lstWeekly, many=True)
        return JSONResponse(serializer.data)

@csrf_exempt
def Programas(request):
    if request.method == "GET":
        lstProduct = product.objects.all()
        serializer = ProgramSerializer(lstProduct, many=True)
        return JSONResponse(serializer.data)

@csrf_exempt
def ProgramasOgx(request):
    if request.method == "GET":
        lstProduct = product.objects.filter(type_expa='person')
        serializer = ProgramSerializer(lstProduct, many=True)
        return JSONResponse(serializer.data)

@csrf_exempt
def ProgramasIcx(request):
    if request.method == "GET":
        lstProduct = product.objects.filter(type_expa='opportunity')
        serializer = ProgramSerializer(lstProduct, many=True)
        return JSONResponse(serializer.data)

@csrf_exempt
def OdStage(request):
    if request.method == "GET":
        lstOdStage = od_stage.objects.all()
        serializer = OdStageSerializer(lstOdStage, many=True)
        return JSONResponse(serializer.data)

def LcPerFormace(request):
    if request.method == "GET":
        date_initial = request.GET.get('date_initial', None)
        date_final = request.GET.get('date_final', None)
        programs = str(request.GET.get('programs', None))
        objConsultaLCPerformance = ConsultaLCPerformance()
        lstResultad = objConsultaLCPerformance.consultaNueva(date_initial, date_final, [programs])
        return HttpResponse(json.dumps(lstResultad), content_type="application/json")
