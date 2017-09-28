from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from Expa.ExpaToken import ExpaToken
# Create your views here.

@csrf_exempt
def getToken (request):
    if request.method == "GET":
        correo = request.GET.get('correo', None)
        passworrd = request.GET.get('passworrd', None)
        objExpaToken = ExpaToken(correo, passworrd)
        return HttpResponse(json.dumps({"token": objExpaToken.getToken()}), content_type="application/json")
