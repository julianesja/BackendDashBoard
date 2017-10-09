from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from Expa.ExpaToken import ExpaToken
from lcperformance.models import user_register
# Create your views here.

@csrf_exempt
def getToken (request):
    if request.method == "GET":
        resultado = {}
        correo = request.GET.get('correo', None)
        passworrd = request.GET.get('passworrd', None)
        objExpaToken = ExpaToken(correo, passworrd)
        Token = objExpaToken.getToken()
        if Token == None:
            resultado = {'resultado' : False}
        else:
            resultado = {'resultado': True, "token": Token}
        return HttpResponse(json.dumps(resultado), content_type="application/json")

@csrf_exempt
def getTokenAdmin(request):
    if request.method == "GET":
        objUserRegister = user_register.objects.filter(user_expa='dev.colombia@ai.aiesec.org')[0]
        objExpaToken = ExpaToken(objUserRegister.user_expa, objUserRegister.password_expa)
        Token = objExpaToken.getToken()
        if Token == None:
            resultado = {'resultado': False}
        else:
            resultado = {'resultado': True, "token": Token}
        return HttpResponse(json.dumps(resultado), content_type="application/json")

